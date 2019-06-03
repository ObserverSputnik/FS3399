""" -----------------------  FS.py ------------------------ """
"""this is the top level file of the FS3399 project"""
import threading
import time
import Vision as VS
import MotionControl as MC
from ctypes import *
import cv2
import Threads
llm = cdll.LoadLibrary('./lowLevelMath.so')   #import lowLevelMath.so 

""" initialize variables """
cmd = ' '                         # command for STM32
flag = 1                           # flag for while loops
showFrame = 1          
writeFlag = 0               # write file or not
lastCmd = ' '
###################### ------ init ------ ######################## 
""" initialize the robot """
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
	flag = MC.PollFlag()        #check for break
	if showFrame:                                                            #
		cv2.imshow("lastframe",VS.lowerBuff)  # live stream if showFrame = 1
		if cv2.waitKey(1)&0xff == ord('q'):   	  # check key for break
			flag = 0		  						  #
			
	cmd = VS.GetVisionCommand()                       
	if MC.AutoFlag and lastCmd!=cmd:                  # if the robot is in auto mode and if the direction changes
		MC.SetMotor(cmd,250)                                  # change the motor output
		print cmd
	if MC.AutoFlag:                                                          # if the robot is in auto mode
		lastCmd = cmd							 # save command

#--------- clean up and exit ---------#	
Threads.ThreadsKillAll()                                               # exit all threads
VS.endCap()									 # release video writer and the camera
MC.stop()										 # stop the robot
print "exit"
