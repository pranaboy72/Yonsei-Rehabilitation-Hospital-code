#include <SoftwareSerial.h>
SoftwareSerial BT(11,10);
//9807:2D:7ECC9C
void setup() {
  // put your setup code here, to run once:
  BT.begin(38400);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (BT.available()) Serial.write( BT.read());
  if (Serial.available()) BT.write( Serial.read());
}
