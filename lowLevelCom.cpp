#include <wiringPi.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringSerial.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#define EOS 'y'
#define LED1Pin 4
#define LED2Pin 5
extern "C"
{
	char UARTBuffer[10];
	int lastE = 0;
	int totE = 0;
    float Ki = 0.2;
    float Kp = 1.2;
    float Kd = 0.1;
	int fd;
	char command = 0;
	char Lang = 'C';
	int LED1State = 0;
	int LED2State = 0;
	int width = 0, height = 0;
	int UARTInit();
	void setup();
	void UARTSends(int len);
	void endCom();
	void setCommand(char dir, int speed, int stepNum, int flagReg);
	void ToggleLED1() {digitalWrite(LED1Pin,LED1State = !LED1State);}
	void ToggleLED2() {digitalWrite(LED2Pin,LED2State = !LED2State);}
	void initLED() 	  {digitalWrite(LED2Pin,0);digitalWrite(LED1Pin,0);}
	void TurnLED1(int state) {digitalWrite(LED1Pin,state);}
	void TurnLED2(int state) {digitalWrite(LED2Pin,state);}
	void trackLoc(int diff, int tol);
	int readFromSTM();
	void setCapParam(int Width, int Height);
}


    
int UARTInit()
{
  if ((fd = serialOpen ("/dev/ttyS4", 115200)) < 0)
  {
    fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
    return 1 ;
  }

  if (wiringPiSetup () == -1)
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
    return 1 ;
  }
  return 0;
}

void setup()
{
  wiringPiSetup();    
  pinMode(LED1Pin,OUTPUT);
  pinMode(LED2Pin,OUTPUT);
  delay(2000); 
  UARTInit();
  UARTBuffer[0] = ' ';
  UARTBuffer[1] = 250;
  printf("low level init finished. \n");
}

void UARTSends(int len)
{
    for(int ii=0;ii<=len;ii++)
    {serialPutchar(fd,UARTBuffer[ii]);}
    serialPutchar(fd,'y');
}

void endCom()
{
    UARTBuffer[0] = ' ';
    UARTBuffer[1] = 250;
    UARTSends(2);
    delay(1000);
}


/* 
 * * * * def for commandBuffer * * * *
 * buffer    |     func
 * ----------------------------------
 * buffer[0] |     D(forward) A(backward) W(right) S(left) ' '(stop) 
 * buffer[1] |     speed  
 * buffer[2] |     flagReg 
 * buffer[3] |     stepper_step_num
 * buffer[4] |
 * buffer[5] |
 * buffer[6] |
 * buffer[7] |    
 * ----------------------------------
 * 
 * 
 * * * * def for FlagReg * * * *
 * 
 * bit    |         flag
 * ----------------------------------
 * bit 0  | Auto Mode
 * bit 1  | read from IMU
 * bit 2  | read battery 
 * bit 3  | stepper_ready
 * bit 4  | stepper_dir
 * bit 5  | 
 * bit 6  | 
 * bit 7  | 
 */
 
void setCommand(char dir, int speed, int flagReg, int stepNum)
{
	UARTBuffer[0] = dir;
	UARTBuffer[1] = speed;
	UARTBuffer[2] = flagReg;
	UARTBuffer[3] = stepNum;
	UARTSends(4);
}

void trackLoc(int diff, int tol)
{
	float P = 2*255*diff/width;
	float DeDt = lastE-diff;
	float speed = P*Kp+DeDt*Kd;
	int absSpeed = int(abs(speed));
	if(absSpeed>255)              {absSpeed = 255;}
	if(absSpeed<100)               {absSpeed = 100;}
	if(speed<0 && abs(diff)>tol) {setCommand('d',char(absSpeed),0,0);}
	else if(speed>0 && diff>tol) {setCommand('a',char(absSpeed),0,0);}
	else                         {setCommand(' ',0,0,0);}
	printf("control output: %f\n", speed);
	if(diff!=0)  {lastE = diff;}
	if(abs(totE)<255) {totE+=diff;}
}

int readFromSTM()
{
	int byteIn = 0;
	if(serialDataAvail(fd))
	{
		byteIn = serialGetchar(fd);
		//printf("%i",byteIn);
		return byteIn;
	}
	else {return -1;}
}

void setCapParam(int Width, int Height)
{
	width = Width;
	height = Height;
}








