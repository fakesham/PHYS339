void setup() {
  Serial.begin(115200);
  Serial.println("HELLO ... PWM Calibration");
  Serial.println("This code will send a PWM wave to digital outputs 9 and 10");
  Serial.println("If an integer between 0 and 255 is entered, it will set the PWM duty cycle.");
  Serial.println("Empty lines will generate a histogram of values read from analog input 0");
  TCCR1B = TCCR1B & 0b11111000 | 1; // This does voodoo magic to set the period of the PWM to 32 us
}

int debug = 0;

int get_value() { // called when there is serial input available
  int result = 0;
  int digit_counter = 0;
  bool empty = true;
  bool non_digit = false;
  do {
    char ch = Serial.read();
    if (debug) {
      Serial.print("ch = ");
      Serial.println(ch,10);
    }
    switch(ch) {
    case '0':
      if (0 == result) {  // ignore leading zeros
        empty = false;
        break;
      }
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9': // ASCII character corresponding to a decimal
      result *= 10; // all previous digits get a promotion
      result += ch - '0'; // subtract ASCII value of '0' digit
      digit_counter++;
      break;
    case '\r': // ignore carriage-return
    case '\n': // new-line means do it
      if (non_digit) {
        Serial.println("Invalid characters were entered, ignoring entire line");
        return -2;
      }
      if ((result > 255) || (digit_counter > 3)) {
        Serial.println("Attempt to enter number larger then 255");
        return -2;
      }
      if ((0 == result) && empty) return -1; // empty line
      return result; // value is probably correct
    case '!': // Undocumented debugging switch
      debug++;
      break;
    default:
      non_digit = true; // you've been flagged
    }
/* Super cute bug :- Try commenting this line out, try with debug set on and off */
    while (!Serial.available()); // wait for next character to arrive
  } while (true);
}


void loop() {
  if (!Serial.available()) return; // no demands are the best demands
  int value = get_value(); // deal with customer
  if (-2 == value) return; // get_value() has already told the customer what's up
  if (-1 == value) { // customer wants a histogram
    unsigned char histo[1024];
    for (int i = 0; i < 1024; i++) histo[i] = 0; // zero histogram
    for (int i = 0; i < 32768; i++) { // this is pretty arbitrary
      int j = analogRead(A0); // get ADC(0) value
      if (debug > 1) {
        Serial.print("analogRead(A0) returned ");
        Serial.println(j);
      }
      if ((j < 0)||(j>1023)) { // this should never happen, it is a 10 bit number
        Serial.print("analogRead(A0) returned "); // so it would be REALLY exciting
        Serial.println(j);
        while (true); // no point proceeding, the universe is broken
      }
      if (255 == ++histo[j]) break; // unsigned char can not take a value larger than 255
    }
    Serial.println("---===### Histogram of values read from analog input 0 ###===---");
    for (int i = 0; i < 1024; i++) { // show non-zero histogram columns
      if (debug > 2) {
        Serial.print("histo[");
        Serial.print(i);
        Serial.print("] = ");
        Serial.println(histo[i]);
      }
      if (histo[i]) {
        Serial.print(i);
        Serial.print(" ");
        Serial.println(histo[i],10);
      }
    }
    return; // task complete
  }
  // if we get this far, value is the number intended for the PWM
  Serial.print("Sending ");
  Serial.print(value);
  Serial.println(" to digital PWM outputs 9 and 10");
  analogWrite(10,value);
  analogWrite(9,value);
}
