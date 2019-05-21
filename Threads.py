import threading
import time
import Vision as VS
import MotionControl as MC
from ctypes import *
import cv2
llm = cdll.LoadLibrary('./lowLevelMath.so')
x = 0
y = 0
Pflag = 0
flag = 1
TrackFlag = 0
trackDoneFlag = 1
outFlag = 0
NavDoneFlag = 1


###########-------- thread def ---------############

class capThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		global flag,trackDoneFlag,NavDoneFlag,Pflag
		while flag:
			VS.getFrame()
			VS.frameBufUpdate(Pflag)
			if trackDoneFlag:
				trackDoneFlag = 0
			if NavDoneFlag:
				NavDoneFlag = 0
			
		print "stop Cap"
					
					
class faceTrackThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		global flag,trackDoneFlag,x,y,face
		while flag:
			if ~trackDoneFlag:
				x,y = VS.getFaceLoc()
				trackDoneFlag = 1
				if MC.TrackFlag == 1:
					MC.Track(x)
		print "Stop Face Cap"
		
##########--------- NavThread not yet used ---------################
	
class NavThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		global NavDoneFlag,flag
		while flag:
			if ~NavDoneFlag:
				VS.runNav()
				NavDoneFlag = 1
		print "quit navThread"
	
	
###################### ------ init ------ ######################## 	
		
def ThreadInit(processFlag):
	global Pflag
	Pflag = processFlag
	getcap = capThread()
	getcap.start()
	if llm.CheckBit(processFlag,1):
		Nav = NavThread()
		Nav.start()
		print "start navThread"
		pass
	if llm.CheckBit(processFlag,2):
		getFace = faceTrackThread()
		getFace.start()	

def ThreadsKillAll():
	global flag
	flag = 0
