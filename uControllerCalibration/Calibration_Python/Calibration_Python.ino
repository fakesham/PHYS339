/* The variables are global to avoid real time allocation */
char *buffer; // buffer accessed as 8-bit entities
//unsigned short *s_buffer; // buffer accessed as 16-bit entities
short rc; // return 16-bit variable
unsigned short count; // entities in buffer
unsigned short index; // position in buffer
unsigned short iterations; // how many iterations
unsigned char pages; // 8-byte pages available in buffer
unsigned char ch; // command byte
unsigned char ipin, opin; // input / output pins

void setup() {
  Serial.begin(115200);
  ipin = 0;
  opin = 13;
  count = 1;
  index = 0;
  TCCR1B = TCCR1B & 0b11111000 | 0x01; // Boost PWM frequency of pin 10
  for (size_t s = 2048; s; s -= 8)
    if (buffer = (char*)malloc(s)) {
//      s_buffer = (unsigned short*)buffer; // point to same location
      pages = s >> 3; // divide by 8
      sprintf(buffer,"pages = %d, s = %d",pages,s);
      Serial.println(buffer);
      Serial.flush();
      return;
    }
}

void loop() {
  if (Serial.available()) {
    ch = Serial.read();
    switch (ch) {
    case 1:
      Serial.print('A'); // this performance is to avoid
      Serial.print('R'); // creating a string "ARDUINO" which
      Serial.print('D'); // would use up valuable dynamic memory
      Serial.print('U'); // it "wastes" program memory, of which
      Serial.print('I'); // there are 32KB, whereas only 2KB of
      Serial.print('N'); // dynamic memory
      Serial.print('O');    
      break;
    case 2: // get_pages
      Serial.write((char*)&pages,1);
      break;
    case 3: // get_sampling_period
      Serial.readBytes((char*)&iterations,2);
      ((unsigned long *)buffer)[1] = micros();
      while (iterations--) rc = analogRead(0);
      ((unsigned long *)buffer)[0] = micros() - ((unsigned long *)buffer)[1];      
      Serial.write(buffer,4);
      break;
    case 4:
      Serial.readBytes(&ipin,1);
      rc = analogRead(ipin+A0);
      Serial.write((char*)&rc,2);
      break;
    case 5:
      Serial.readBytes(&opin,1);
      Serial.readBytes((char*)&rc,2);
      analogWrite(opin,rc);
      Serial.write((char*)&rc,2);
      break;
    case 6:
      Serial.readBytes(&ipin,1);
      Serial.readBytes((char*)&count,2);
      Serial.write((char*)&count,2);
      ipin += A0;
      for (index = 0; index < count; index++) ((unsigned short*)buffer)[index] = analogRead(ipin);
      Serial.write(buffer,count<<1);
      break;
    case 7:
      Serial.readBytes(&opin,1);
      Serial.readBytes((char*)&count,2);
      for (index = 0; index < count; index++) Serial.readBytes(&buffer[index],1);
      index = 0;
      ch |= 0x80;
      Serial.write((char*)&count,2);
      break;
    case 8:
      Serial.readBytes(&opin,1);
      Serial.readBytes(&ipin,1);
      Serial.readBytes((char*)&iterations,2);
      Serial.readBytes((char*)&count,2);
      Serial.readBytes(buffer,count);
      ipin += A0;
      index = 0;
      ch |= 0xc0;
      Serial.write((char*)&count,2);
      break;
    }
  }
  if (ch & 0x80) {
    analogWrite(opin,buffer[index]);
    rc = analogRead(ipin);
    if (ch & 0x40) {
      if (!iterations) buffer[index] = rc >> 2;
    }
    index++;
    index %= count;
    if ((ch & 0x40) && !index && !iterations--) { // iterations only decrements if index == 0
      Serial.write(buffer,count);
      Serial.flush();
      ch = 0;
    }
  }
}
