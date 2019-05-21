from ctypes import *
import time
import keyboard
lc = cdll.LoadLibrary('./lowLevelCom.so')
llm = cdll.LoadLibrary('./lowLevelMath.so')

State = ord(' ')
Speed = 0
data = 0       # data buffer with no -1
thisData = -1  # actuall data from UART.avail()
flag = 1   
TrackFlag = 0
width = 0
height = 0
AutoFlag = 1
#---- pass param flag ----#

def PollFlag():
	return flag 
	
#------------- Init --------------#

def Init():
	keyboard.on_press(checkKey,False)
	lc.setup()

	
def setFrameParam(param1,param2):
	global width,height
	width = param1
	height = param2

#------------ check key press --------------#

def checkKey(e):
	global flag, TrackFlag, AutoFlag 
	global State, Speed
	if keyboard.is_pressed('w'):
		Speed=255
		lc.setCommand(ord('w'),Speed,0,0)
		State = ord('w')

#	elif keyboard.is_pressed('s'):
#		Speed=255
#		lc.setCommand(ord('s'),Speed,0,0)
#		State = ord('s')
#
#	elif keyboard.is_pressed('a'):
#		Speed=255
#		lc.setCommand(ord('a'),Speed,0,0)
#		State = ord('a')
#	
#	elif keyboard.is_pressed('d'):
#		Speed=255
#		lc.setCommand(ord('d'),Speed,0,0)
#		State = ord('d')

	elif keyboard.is_pressed(' '):
		Speed=0
		lc.setCommand(ord(' '),Speed,0,0)
		State = ord(' ')
		TrackFlag = 0
		AutoFlag = 0
	if keyboard.is_pressed('q'):
		flag = 0
		Speed=0
		lc.setCommand(ord(' '),Speed,0,0)
		State = ord(' ')
		TrackFlag = 0
		AutoFlag = 0
		
#	elif keyboard.is_pressed('e'):
#		TrackFlag = 1
#		
	elif keyboard.is_pressed('f'):
		AutoFlag = 1
	
#------ communication codes with STM32 via UART ------# 

def readBattery():
	global State
	global Speed
	global data
	lc.setCommand(State,Speed,4,0)
	pollUart()
	if data>0:
		data = (7*float(data)/255)
		if data <= 6.2:
			lc.TurnLED1(1)
		return data
	else:
		return -1


def pollUart():
	global data,thisData
	if thisData>=0:
		data = thisData
	thisData = lc.readFromSTM()


def Track(target):
	global width
	diff = 0
	if target:
		diff = (width/2)-target;
		lc.trackLoc(diff, width/8);
	else:
		diff = 0;
		lc.trackLoc(diff, width/8);
	return diff

def SetMotor(mode, speed):
	lc.setCommand(mode,speed,0,0)
	State = mode
