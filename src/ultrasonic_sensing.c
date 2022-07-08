#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>
#include <math.h>

#define trigger 21  //초음파 내보냄 출력, 숫자는 핀번호
#define echo 20    //초음파 받음 입력, 숫자는 핀번호

unsigned int start_time;
unsigned int end_time;
float distance = 0;
int pulse;

int main(void)
{
	wiringPiSetupGpio();
	pinMode(trigger, OUTPUT);
	pinMode(echo, INPUT);

	while (1)
	{
		digitalWrite(trigger, LOW);  //출력을 0으로 조정
		digitalWrite(trigger, HIGH); //출력을 1로
		delayMicroseconds(10);  //10마이크로세컨즈만큼 쉬어가기
		digitalWrite(trigger, LOW);

		if (digitalRead(echo) == 0)  //입력이 low인 경우
			start_time = micros();    //그때 시간 저장
		else if (digitalRead(echo) == 1) //입력이 high인 경우
			end_time = micros();    //그때 시간 저장

		distance = (end_time - start_time) / 58;

		if (distance < 124245131)  //거리가 너무 가까우면
		{
			printf("it's too close");
		}
		delay(1000); //1초 멈춤
	}
	return 0;
}
