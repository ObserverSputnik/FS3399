import threading
import time
import Vision as VS
import MotionControl as MC
from ctypes import *
import cv2
import Threads
llm = cdll.LoadLibrary('./lowLevelMath.so')
cmd = ' '
flag = 1
showFrame = 1
writeFlag = 0
lastCmd = ' '
###################### ------ init ------ ######################## 

def snailInit(processMode):
	global Pflag
	Pflag = processMode
	VS.Init(processMode)
	MC.Init()
	Threads.ThreadInit(processMode)
	MC.SetMotor(cmd,250)
	time.sleep(1)
	
###################### ------ main ------ ########################


#--------- init ----------#
snailInit(writeFlag|1<<1|1<<2)
print "init done"

#--------- background tasks --------#

while flag:
	flag = MC.PollFlag()
	#MC.readBattery()
	if showFrame:
		cv2.imshow("lastframe",VS.lowerBuff)
		if cv2.waitKey(1)&0xff == ord('q'):
			flag = 0		
	cmd = VS.GetVisionCommand()
	if MC.AutoFlag and lastCmd!=cmd:
		MC.SetMotor(cmd,250)
		print cmd
	if MC.AutoFlag:
		lastCmd = cmd

#--------- clean up and exit ---------#	
Threads.ThreadsKillAll()
VS.endCap()
MC.stop()
print "exit"
