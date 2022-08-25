////////////////////////////////////////////////////////////////////////
// Arduino Bluetooth Interface with Mindwave
// 
// This is example code provided by NeuroSky, Inc. and is provided
// license free.
//
// This modification allows view data trough serial monitor
// Lozano Ramirez Angel Ivan
// Mexico  2.07.2021
////////////////////////////////////////////////////////////////////////

#include <SoftwareSerial.h>
SoftwareSerial BT(9,10); //Rx/Tx

#define LED 13
#define BAUDRATE 57600
#define DEBUGOUTPUT 0

// checksum variables
byte  generatedChecksum = 0;
byte  checksum = 0; 
int   payloadLength = 0;
byte  payloadData[64] = {0};
byte  poorQuality = 0;
byte  attention = 0;
byte  meditation = 0;

// system variables
long    lastReceivedPacket = 0;
boolean bigPacket = false;

//////////////////////////
// Microprocessor Setup //
//////////////////////////
void setup(){
  pinMode(LED, OUTPUT);
  BT.begin(BAUDRATE);           // Software serial port  (ATMEGA328P)
  Serial.begin(BAUDRATE);           // USB
}

////////////////////////////////
// Read data from Serial UART //
////////////////////////////////
byte ReadOneByte() {
  int ByteRead;
  while(!BT.available());
  ByteRead = BT.read();

  #if DEBUGOUTPUT  
    Serial.print((char)ByteRead);   // echo the same byte out the USB serial (for debug purposes)
  #endif

  return ByteRead;
}

/////////////
//MAIN LOOP//
/////////////
void loop() {
  // Look for sync bytes
  if(ReadOneByte() == 170) {
    if(ReadOneByte() == 170) {
      payloadLength = ReadOneByte();
      if (payloadLength!=4){
        Serial.print("payloadLength:");
        Serial.println(payloadLength);
        delay(500);
      }
      if(payloadLength > 169)                      //Payload length can not be greater than 169
      return;

      generatedChecksum = 0;        
      for(int i = 0; i < payloadLength; i++) {  
        payloadData[i] = ReadOneByte();            //Read payload into memory
        //Serial.println(payloadData[i]);
        generatedChecksum += payloadData[i];
      }   

      checksum = ReadOneByte();                      //Read checksum byte from stream      
      generatedChecksum = 255 - generatedChecksum;   //Take one's compliment of generated checksum

        if(checksum == generatedChecksum) {    
//        Serial.println("checksum same");
//        delay(500);
        poorQuality = 200;
        attention = 0;
        meditation = 0;

        for(int i = 0; i < payloadLength; i++) {    // Parse the payload
          if (payloadLength!=4){
            Serial.print(i);
            Serial.print(":");
            Serial.print(payloadData[i]);
            Serial.print("\t");
            delay(500);
          }
          switch (payloadData[i]) {
          case 2:
            i++;            
            poorQuality = payloadData[i];
            bigPacket = true; 
            if (payloadLength!=4){
            Serial.print("<case 2>"); 
            Serial.print("\n");  
            delay(500); 
            }       
            break;
          case 4:
            i++;
            attention = payloadData[i];  
            if (payloadLength!=4){
            Serial.print("<case 4>");  
            Serial.print("\n");   
            delay(500);
            }                 
            break;
          case 5:
            i++;
            meditation = payloadData[i];
            if (payloadLength!=4){
             Serial.print("<case 5>");
             Serial.print("\n");
             delay(500);
            }
            break;
          case 0x80:
            i = i + 3;
            if (payloadLength!=4){
             Serial.print("<case 0x80>");
             Serial.print("\n");
             delay(500);
            }
            break;
          case 0x83:
            i = i + 25;  
            if (payloadLength!=4){
             Serial.print("<case 0x83>"); 
             Serial.print("\n");
             delay(500);   
            }
            break;
          default:
            if (payloadLength!=4){
             Serial.print("<case default>");
             Serial.print("\n");
             delay(500);
            }
            break;
          } // switch
        } // for loop

#if !DEBUGOUTPUT
        // *** Add your code here ***
        if(bigPacket) {
          if(poorQuality == 0)  digitalWrite(LED, HIGH);
          else  digitalWrite(LED, LOW);
          Serial.print("Attention: ");
          Serial.print(attention);
          Serial.print("\t");
          Serial.print("Meditation: ");
          Serial.print(meditation);
          Serial.print("\n");
          delay(1000);
        }
#endif        
        bigPacket = false;        
      }
      else {
        // Checksum Error
      }  // end if else for checksum
    } // end if read 0xAA byte
  } // end if read 0xAA byte
}
