#include <stdlib.h>

const int SWITCH[4] ={};
const int BUTTON[4] ={};

int oldval[4]= {0,0,0,0};
int val[4]={0,0,0,0};
int state[4]={0,0,0,0};

void setup(){
    for (int i =0;i<4; i++){
        pinMode(SWITCH[i], OUTPUT);
        pinMode(BUTTON[i], INPUT);
    }
    Serial.begin(57600);
}

void loop(){
    for (int i=0;i<4;i++)   val[i]=digitalRead(BUTTON[i]); 

    state_chg(oldval,val,state);

    for (int i=0; i<4; i++) oldval[i]=val[i];

    for (int i=0; i<4; i++){
        if (state[i]==1){
            Serial.println("OFF") //send off message back to the computer
            digitalWrite(SWITCH[i], LOW); //turn off flow of electricity to magnet      
        }
        else {
            Serial.println("ON"); //send on message back to the computer
            digitalWrite(SWITCH[i], HIGH); //turn on flow of electricity to magnet
        }
    }
}

void state_chg(&oldval, &val, &state){
    for (int j;j<4;j++){
        if ((val[j] == HIGH) && (old_val[j] == LOW)){
            state[j]=1-state[j];
            delay(10);
        }
    }
}
