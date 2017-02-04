/*
 * Author: J Whitten
 * Name: AnalogStreamer
 * Description: Takes analog inputs and streams them in
 * a simple message structure that can be interpreted elsewhere
 */
 
//Globals
/* Structure
 *  0 - START BYTE (0xAA)
 *  1 - X1H
 *  2 - X1L
 *  3 - Y1H
 *  4 - Y1L
 *  5 - X2H
 *  6 - X2L
 *  7 - Y1H
 *  8 - Y1L
 *  3 - Y2H
 *  4 - Y2L
 *  5 - END BYTE (0x55)
 */
 
enum{ //for code read ease
  X1H = 1,
  X1L,
  Y1H,
  Y1L,
  X2H,
  X2L,
  Y2H,
  Y2L
};

int vals[] = {0xAA, 0, 0, 0, 0, 0, 0, 0, 0, 0x55};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

int temp = 0;
void loop() {
  //Sample analog inputs (10-bit) and 
  //place into 8-bit containers
  temp = analogRead(A0);
  vals[X1H] = (temp>>8)&0xff;
  vals[X1L] = temp&0xff;

  temp = analogRead(A1);
  vals[Y1H] = (temp>>8)&0xff;
  vals[Y1L] = temp&0xff;

  temp = analogRead(A2);
  vals[X2H] = (temp>>8)&0xff;
  vals[X2L] = temp&0xff;

  temp = analogRead(A3);
  vals[Y2H] = (temp>>8)&0xff;
  vals[Y2L] = temp&0xff;

  //Write the measured values to serial port
  Serial.write((uint8_t*) vals, 10);
  
  //Miniscule delay
  delay(25);
}
