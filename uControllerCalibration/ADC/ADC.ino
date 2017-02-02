unsigned char histo[1024];

void setup() {
  Serial.begin(115200);
  Serial.println("Getting analog ADC values!!!!!!!!"); 
  TCCR1B = TCCR1B & 0b11111000 | 1; // This does voodoo magic to set the period of the PWM to 32 us   
  for(int i = 0; i < 1024; i++){
    histo[i] = 0; 
  }
}
// zero histogram 


int value = -1;

int get_value(){
  value += 8; 
  return value; 
}

void printHisto(){
  for(int i = 0; i < 1024; i++){
         Serial.print(histo[i]); 
         Serial.print(","); 
  }
}
void loop() {
   
  int value = get_value();

  if(value>255){
    printHisto(); 
    exit(0);
  }
  
  // if we get this far, value is the number intended for the PWM
  Serial.print("Sending ");
  Serial.print(value);
  Serial.println(" to digital PWM output 9");
  analogWrite(9,value);
  delay(2000);
  Serial.print("Received ");
  int j = analogRead(A5); 
  Serial.println(j);
  Serial.println("--------------------------------------------");
  histo[j]+=1; 
}

