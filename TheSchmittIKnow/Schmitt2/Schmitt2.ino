/* 
 * Servo Sketch 
 *   Last edit 13h30 March 8, 2016
 */
void register_variable(double *address, const char *name, int record, const char *units);
#define RECORD(X,UNITS) register_variable(&X,#X, 1, UNITS)
#define INITIALIZE(X,VALUE,UNITS) X = VALUE; register_variable(&X,#X, 0, UNITS)

/* These are the global variables used in the controller */

double dt;
double temperature;
double e_temperature;
double error;
double dacVal; 
double prevError;
double Tset;
double band;
double out;
double integralsum;
double outbeforeroot; 
double proportional; 
double derivative; 
double integral; 
double deltaT; 
double power; 
double count = 0;

//Three doubles corresponding to the tuning constants on the proportional, integral, and derivative 
//#terms of the control function
double cb = 0;
double iat = 8;

//#takes the current error, last last error, the existing sum of the integral
//#and the change in time between each two points of the integral
double integration (double currentval, double lastval, double sum, double deltat) 
{
 //#calculate distance between current and set value (e.g the height of the function)
 //# think we should absolute value this, but that can be done afterwards
 //#takes the average height of the riemann rectangle
 double height = ((currentval+lastval)/2);
 
 double area = height*deltat;
 deltaT = deltat; 
 
 return (area+sum);
}

double differentiate (double currentval, double lastval, double distance) 
{
 return ((currentval-lastval)/distance);
}

void userSetup() {
  /* 
   * this function is called at program startup.  There are two useful things to do here
   *
   * RECORD(variableName,units)
   *   This will register a variable to be sent back to the computer at each time step
   *   The variable should be a globaly defined double precision variable (see temperature above)
   *   Units is a string used for labels
   *
   * INITIALIZE(variableName,value,units)
   *   This will register a variable which can be set from the computer
   *   The variable should be a globably defined double
   *   The value is used as the default value
   *   Units is a string used for labels
   */
  RECORD(temperature,"K");
  RECORD(e_temperature,"K");
  RECORD(error,"");
  RECORD(count,""); 
  RECORD(dacVal,"");
  RECORD(integralsum,""); 
  RECORD(derivative,""); 
 
 
//  RECORD(derivative,"s<sup>-1</sup>"); /* you can use HTML, this will disp[ay a super-script */
  RECORD(out,"DAC units");
  INITIALIZE(dt,0.1,"s");
  INITIALIZE(Tset,350,"K");
  INITIALIZE(band,5,"K");
  INITIALIZE(cb,1,"arb"); 
  INITIALIZE(iat,8,"s");
}

void userAction() {
  /*
   * This function will be called each time step
   */
  long sum = 0, sumsq = 0;
  int value;
  const int N = 16; /* number of samples measured per time step */
  for (int i = 0; i < N; i++) { /* record N samples */
    value = analogRead(0);
    sum += value; /* used to calculate mean */
    sumsq += value*(long)value; /* used to calulate variance, need to type cast to long because int is 16 bit */
  }
  double mu, sigma;
  mu = sum / (double) N;
  sigma = sqrt((sumsq - sum*mu)/N); /* expansion of definition of variance */
  const double ADCslope = 4.888e-3; /* 4.888mV / bit */
  const double ADCoffset = 1.02e-3; /* 1.02 mV */
  double vThermo, eVThermo;
  vThermo = ADCslope * mu + ADCoffset; /* convert means in ADC units to voltages */
  eVThermo = ADCslope * sigma;
  const double thermoSlope = 100; /* K/V */
  const double thermoOffset = 273; /* K */
  temperature = thermoSlope * vThermo + thermoOffset;
  e_temperature = eVThermo * vThermo;
  prevError = error;
  error = (temperature - Tset) / band;

  /*
  if ((out > 0) && (temperature > Toff)) {
    out = 0;
  } else if ((out == 0) && (temperature < Ton)) {
    out = 255;
  }
  int dacVal = out;
  */
  /*
  Serial.print("DEBUG\tdacVal = ");
  Serial.print(dacVal);
  Serial.print("\n");
  */
  //#analogWrite(11, dacVal);
  
  //#Proportional output
  //#(Why is the thing in the manual referred to as error?)
  //#Think we can have constants on the integral and derivative response, and leave proportional fixed(?)
  //#Think we may have to go up to where error is defined and flip it

  
  derivative = (cb*differentiate(error, prevError, dt));
  integralsum = (1/iat*(integration(error,prevError,integralsum,dt)));

  integral = integral+integralsum; 

  power = 0.5 - error - derivative - integral;
  if (power > 1) power = 1;
  if (power < 0) power = 0;
  if (fabs(error) > 0.5) integral = 0;
  out = sqrt(power)*255;
  
  
  int dacVal = out;
    
  analogWrite(11, dacVal);
  
}

void userStart() {
/*
 * This function is called when the algorithm is started
 */

  out = 0;
}

void userStop() {
/*
 * This function is called when the algorithm is stopped
 * - Good place to turn off the power :)
 */
 analogWrite(11, 0); /* turn off power */
}







































/**********************************************
 * Don't worry about the code below this line *
 * Unless you are curious, but be forewarned  *
 * comments are used very sparingly           *
 **********************************************/

//storage variables
int counter = 0, oc = 0;
int running = 0;
const int N = 16;
unsigned long bytes = 0;
char command[64];
int commandIndex = 0;

struct dataNode {
  double *address;
  const char *name, *units;
  double *values; // points to an array used as a circular queue for recorded values, NULL for initialized values
  struct dataNode *next;
} *data = NULL; // data points to the head of the list of nodes, initially the list is empty
int nodeCount = 0; // this value is redundant, but makes debugging easier

void register_variable(double *address, const char *name, int record, const char *units) {
  struct dataNode *ptr = (struct dataNode *) malloc(sizeof(struct dataNode)); // create storage for new variable
  if (!ptr) for (;;delay(1000)) {
    Serial.print("ERROR\tregister_variable(): Unable to malloc dataNode, nodeCount = ");
    Serial.print(nodeCount);
    Serial.print(", variable = ");
    Serial.print(name);
    Serial.print("\n");
    Serial.flush();
  }
  if (record) {
    ptr->values = (double *) malloc(N*sizeof(double)); // create storage for recorded values
    if (!ptr->values) for (;;delay(1000)) {
      Serial.print("ERROR\tregister_variable(): Unable to malloc values array, nodeCount = ");
      Serial.print(nodeCount);
      Serial.print(", variable = ");
      Serial.print(name);
      Serial.print("\n");
      Serial.flush();
    }
  } else ptr->values = NULL;
  nodeCount++; // increment counter
  ptr->address = address; // fill in values
  ptr->name = name;
  ptr->units = units;
  ptr->next = data; // this new node will become the head of the list, it points to the original list
  data = ptr; // now pointer to head of list points to new node
}

void setPeriod (int period) { // period in ms
  const double tick = 1024000 / 16e6; // clock tick in ms
  int number = floor(period / tick) - 1;
  char buf[256];
  sprintf(buf,"DEBUG\tsetPeriod(%d): number = %d, tick = %ld us, actual period = %ld us\n", period, number, (long)(1e3*tick), (long)(1e3*tick*(number+1)));
  Serial.print(buf);
  cli();//stop interrupts
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  OCR1A = number; // = (16*10^6) / (1*1024) - 1 (must be <65536) originally 15624
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  sei();//allow interrupts
}

void setup() {
  Serial.begin(115200);
  Serial.print("\nBOOT\n");
  Serial.flush();
  Serial.print("DEBUG\tHello World!\n");
  Serial.flush();
#ifdef DEBUG
  analogWrite(3, 127);
  analogWrite(5, 127);
  analogWrite(6, 127);
  analogWrite(9, 127);
  analogWrite(10, 127);
  analogWrite(11, 127);
#endif
  TCCR2B = TCCR2B & 0b11111000 | 0x01;
  pinMode(13,OUTPUT);
  userSetup();
}

ISR(TIMER1_COMPA_vect){//timer1 interrupt 1Hz toggles pin 13 (LED)
//generates pulse wave of frequency 1Hz/2 = 0.5kHz (takes two cycles for full wave- toggle high then toggle low)
  if (!running) return;
  if (counter % 2){
    digitalWrite(13,HIGH);
  }
  else{
    digitalWrite(13,LOW);
  }
  userAction();
  for(struct dataNode *ptr = data; ptr; ptr = ptr->next) if (ptr->values) ptr->values[counter % N] = *ptr->address;
  counter++;
}

void parseCommand(void) {
  char *ptr;
#ifdef DEBUG
  Serial.print("DEBUG\tparseCommand(): Command = '");
  Serial.print(command);
  Serial.print("'\n");
  Serial.flush();
#endif
  ptr = strtok(command," ");
  if (!ptr) {
#ifdef DEBUG
    Serial.print("DEBUG\tparseCommand(): Verb is NULL\n");
    Serial.flush();
#endif
    return;
  }
  switch(strlen(ptr)) {
  case 3:
    if (!strcmp(ptr,"SET")) {
      ptr = strtok(NULL," ");
      if (!ptr) {
#ifdef DEBUG
        Serial.print("DEBUG\tparseCommand(): Variable is NULL\n");
        Serial.flush();
#endif
        return;
      }
#ifdef DEBUG
      Serial.print("DEBUG\tparseCommand(): Variable is ");
      Serial.print(ptr);
      Serial.print("\n");
      Serial.flush();
#endif
      for(struct dataNode *dptr = data; dptr; dptr = dptr->next) if (!strcmp(dptr->name,ptr)) {
        ptr = strtok(NULL," ");
        if (!ptr) {
#ifdef DEBUG
          Serial.print("DEBUG\tparseCommand(): ivalue is NULL\n");
          Serial.flush();
#endif
          return;
        }
#ifdef DEBUG
        Serial.print("DEBUG\tparseCommand(): ivalue is ");
        Serial.print(ptr);
        Serial.print("\n");
        Serial.flush();
#endif
        long int ivalue;
        int exponent;
        sscanf(ptr,"%ld",&ivalue);
        if (ivalue == 0) {
          *dptr->address = 0;
        } else {
          ptr = strtok(NULL," ");
          if (!ptr) {
#ifdef DEBUG
            Serial.print("DEBUG\tparseCommand(): Exponent is NULL\n");
            Serial.flush();
#endif
            return;
          }
#ifdef DEBUG
          Serial.print("DEBUG\tparseCommand(): Exponent is ");
          Serial.print(ptr);
          Serial.print("\n");
          Serial.flush();
#endif
          sscanf(ptr,"%d",&exponent);
          *dptr->address = ivalue * pow(2,exponent);
        }
#ifdef DEBUG
        Serial.print("DEBUG\tparseCommand(): value set to ");
        Serial.print(*dptr->address);
        Serial.print("\n");
        Serial.flush();
#endif
        return;
      }
    }
  case 4:
    if (!strcmp(ptr,"STOP")) {
      running = 0;
      userStop();
      return;
    }
  case 5:
    if (!strcmp(ptr,"START")) {
      setPeriod(1000*dt);
      counter = 0;
      oc = 0;
      userStart();
      running = 1;
      return;
    }
  case 9:
    if (!strcmp(ptr,"HANDSHAKE")) {
      ptr = strtok(NULL," ");
      Serial.print("HANDSHAKE\t");
      Serial.print(ptr);
      Serial.print("\n");
      Serial.flush();
      for(struct dataNode *ptr = data; ptr; ptr = ptr->next) if (!ptr->values) {
        Serial.print("INIT\t");
        Serial.print(ptr->name);
        Serial.print ("\t=\t");
        Serial.print(*((long *)ptr->address),HEX);
        //Serial.print(*ptr->address);
        Serial.print("\t");
        Serial.print(ptr->units);
        Serial.print("\n");
        Serial.flush();
      }
      Serial.print("\nREADY\n");
      Serial.flush();
      return;
    }
  }
#ifdef DEBUG
  Serial.print("DEBUG\tparseCommand(): Unhandled command\n");
  Serial.flush();
#endif
  return;
}

void getCommand() {
  static unsigned char ch;
  static int discard = 0;
  Serial.readBytes(&ch,1);
  Serial.print("DEBUG\tgetCommand() : ch = ");
  Serial.print(ch,BIN);
  Serial.print("\n");
  Serial.flush();
  if (discard && (ch == '\n')) { // reached end of garbage (hopefully \n was not garbage?!
    discard = 0;
    return;
  }
  if (discard) return;
  if (ch & 0x80) {
    command[commandIndex] = 0;
    Serial.print("ERROR\tMSB set in input stream, command so far = \"");
    Serial.print(command);
    Serial.print("\"\n");
    Serial.flush();
    commandIndex = 0;
    discard = 1;
    return;
  }
  Serial.write(ch | 0x80);
  if (ch == '\n') {
    command[commandIndex] = 0;
    parseCommand();
    commandIndex = 0;
    return;
  }
  command[commandIndex++] = ch;
}

void loop() {
  char buf[256];
  if (Serial.available()) getCommand();

  if ((counter - oc) > N) {
    Serial.print("ERROR\tInternal buffer overrun\n");
  }  
  while (oc < counter) {
    Serial.print("INDEX\t");
    Serial.print(oc);
    Serial.print("\t");
    Serial.print(counter);
    Serial.print("\n");
    Serial.flush();
    for(struct dataNode *ptr = data; ptr; ptr = ptr->next) if (ptr->values) {
      Serial.print("VALUE\t");
      Serial.print(ptr->name);
      Serial.print("\t=\t");
      Serial.print(*((long *)&(ptr->values[oc % N])),HEX);
      Serial.print("\t");
      Serial.print(ptr->units);
      Serial.print("\n");
      Serial.flush();
    }
    oc++;
  }
}

