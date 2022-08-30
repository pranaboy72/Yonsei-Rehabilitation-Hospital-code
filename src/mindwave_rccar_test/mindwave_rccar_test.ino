#include <SoftwareSerial.h>
SoftwareSerial BT(9,10); //Rx/Tx
#include <AFMotor.h>

AF_DCMotor motor_L(1);
AF_DCMotor motor_R(4);

#define LED 13
#define BAUDRATE 57600
#define DEBUGOUTPUT 0

// checksum variables
byte generatedChecksum = 0;
byte checksum = 0; 
int payloadLength = 0;
byte payloadData[64] = {0};
byte poorQuality = 0;
byte attention = 0;
byte meditation = 0;

// system variables
long lastReceivedPacket = 0;
boolean bigPacket = false;
// char stall;

int Speed = 130;  

//////////////////////////
// Microprocessor Setup //
//////////////////////////
void setup() {
  // put your setup code here, to run once
  motor_L.setSpeed(200);
  motor_L.run(RELEASE);
  motor_R.setSpeed(200);
  motor_R.run(RELEASE);
  
  pinMode(LED, OUTPUT); 
  BT.begin(BAUDRATE);
  Serial.begin(BAUDRATE);          
  // USB
}

////////////////////////////////
// Read data from Serial UART //
////////////////////////////////
byte ReadOneByte() 

{
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
  //   stall = Serial.read();
  //   if (stall == 'c')  Stop();
  // Look for sync bytes
  if(ReadOneByte() == 170){
    if(ReadOneByte() == 170){
        payloadLength = ReadOneByte();
        if (payloadLength!=4){
          Serial.print("payloadLength:");
          Serial.println(payloadLength);
          delay(500);
        }
      
        if(payloadLength > 169)                      //Payload length can not be greater than 169
        return;
      
        generatedChecksum = 0;        
        for(int i = 0; i < payloadLength; i++){  
          payloadData[i] = ReadOneByte();            //Read payload into memory
          generatedChecksum += payloadData[i];
        }   

        checksum = ReadOneByte();                      //Read checksum byte from stream      
        generatedChecksum = 255 - generatedChecksum;   //Take one's compliment of generated checksum

        if(checksum == generatedChecksum) 
        {    
          poorQuality = 200;
          attention = 0;
          meditation = 0;

          for(int i = 0; i < payloadLength; i++) 
          {                                          // Parse the payload
            if (payloadLength!=4){
            Serial.print(i);
            Serial.print(":");
            Serial.print(payloadData[i]);
            Serial.print("\t");
            delay(500);
          }
          switch (payloadData[i]) 
          {
          case 2:
            i++;            
            poorQuality = payloadData[i];
            bigPacket = true;
            if (payloadLength!=4){
            Serial.print("<case 2>"); 
            Serial.print("\n");  
            delay(500);}            
            break;
          case 4:
            i++;
            attention = payloadData[i]; 
            if (payloadLength!=4){
            Serial.print("<case 4>");  
            Serial.print("\n");   
            delay(500);}                       
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

        if(bigPacket) 
        {
          if(poorQuality == 0)
             digitalWrite(LED, HIGH);
          else
            digitalWrite(LED, LOW);
          
          Serial.print("PoorQuality: ");
          Serial.print(poorQuality, DEC);
          Serial.print(" Attention: ");
          Serial.print(attention, DEC);
          Serial.print(" Time since last packet: ");
          Serial.print(millis() - lastReceivedPacket, DEC);
          lastReceivedPacket = millis();
          Serial.print("\n");
          delay(1000);
        }
        
        if(attention>50){
        forword(); 
        Serial.println("forward!");        
        }

        if(attention>10 && attention<50){
        backword();
        }

        else{
        Stop();
        Serial.println("Stop!");            
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



void forword(){  //forword
  motor_L.run(FORWARD);
  motor_R.run(FORWARD);
  delay(1000);
}

void backword(){ //backword
  motor_L.run(BACKWARD);
  motor_R.run(BACKWARD);
  delay(1000);
}

void Stop(){ //stop
  motor_L.run(RELEASE);
  motor_R.run(RELEASE);
  delay(1000);
}
