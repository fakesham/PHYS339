#include <Wire.h>

#define ADDRESS 0x62

void setDAC(int word) {
  char cmd[3];
  word <<= 4;
  cmd[0] = 0x40;
  cmd[1] = word >> 8;
  cmd[2] = word & 0xff;
  Wire.beginTransmission(ADDRESS);
  if (3 != Wire.write(cmd,3)) {
    Serial.println("FOUL!");
  }
  Wire.endTransmission();
}

void setup() {
  Serial.begin(115200);
  Serial.println("LASER 2017");
  Wire.begin();
  for (int i = 12; i < 14; i++) pinMode(i,OUTPUT);
}

unsigned int counter = 0;
char buf[256]; // space to write strings to
int mode = 0;
unsigned steps = 1000;
unsigned delays = 20;

void parse_input() {
  long int start = millis();
  for (int i = 0; i < 255; i++) { // fill buffer
    while (!Serial.available()) {
      if ((millis() - start) > 1000) { // if a second passes before command
        Serial.println("Timeout!");    // completes give up and 
        return;                        // return to avoid waiting forever
      }
    }
    buf[i] = Serial.read();
    if ('\n' == buf[i]) {
      if (!strncmp("LASER",buf,5)) {
        parse_laser();
        return;
      } else if (!strncmp("STEPS",buf,5)) {
        parse_steps();
        return;
      } else if (!strncmp("DELAYS",buf,6)) {
        return;
        parse_delays();
      } else if (!strncmp("START",buf,5)) {
        if (mode) return;
        mode = 1;
        return;
      } else if (!strncmp("STOP",buf,4)) {
        if (!mode) return;
        mode = 2; // set flag to stop at end of loop
        return;
      } else if (!strncmp("ABORT",buf,5)) {
        mode = 0;
        counter = 0;
        return;
      }
    }
  }
}

void parse_laser(void) {
  int value;
  if (1 != sscanf(buf+6,"%d",&value)) {
    Serial.println("Syntax: LASER <number>\nwhere <number> is 0..4095");
    return;
  }
  if ((value < 0) || (value > 4095)) {
    Serial.println("LASER range error");
    return;
  }
  setDAC(value);
  return;
}

void parse_steps(void) {
  if (1 != sscanf(buf+6,"%ud",&steps)) {
    Serial.println("Syntax: STEPS <number>");
    return;
  }
  return;
}

void parse_delays(void){
  if (1 != sscanf(buf+7,"%ud",&steps)) {
    Serial.println("Syntax: DELAYS <number>");
  }
  return;
}

void loop() {
  if (Serial.available()) parse_input();
  if (!mode) return;
  for (int i = 0; i < delays; i++) analogRead(A0); // this is really just a delay
  sprintf(buf,"%04d:%04d",counter,analogRead(A0));
  digitalWrite(13,0);
  Serial.println(buf);
  Serial.flush();
  digitalWrite(13,1);
  counter++;
  if (steps == counter) counter = 0;
  if (!counter && (2 == mode)) mode = 0; // waiting to stop
}
