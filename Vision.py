""" ------------------Vision.py------------------- """
""" this is the vision part of FS399 project"""
import cv2
import numpy as np
import time
import MotionControl as MC
import math
from ctypes import *

lc = cdll.LoadLibrary('./lowLevelCom.so')         #import lowLevelCom.so 
llm = cdll.LoadLibrary('./lowLevelMath.so')     #import lowLevelMath.so 
outflag = 0                                                                       # for writing video file
lowerBuffHeight = 200                                               # trimed image height
AutoCom = ord(' ')                                                       # auto mode command
imgVar = 1000                                                                # image varience threshold
#-----------------------
#      ProcessFlag
#----- flag table ------
#bitNum |   func
#-------|---------------
#   0     |	FILE OUTPUT
#   1     |   none
#   2     |   FACE TRACK
#   3     |   
#   4     |
#   5     |
#   6     |
#   7     |

def GetVisionCommand():   #pass auto mode command
	return AutoCom

# ------------------- VS.Init --------------------
def Init(processFlag):
	# global var
	global cap,frame,face,frameBuff,NavFullBuff               # full image buffers
	global lastFrame,fDiff,lowerBuff,lowerGray,NavBuff,Kbuff  # trimed buffers
	global height,width,lowerBuffHeight,GNDColor,imgDeviation # buffer param
	global outFlag,Pflag                                # flags
	global lastSections
	lastSections = []
	# set up capture param
	cap = cv2.VideoCapture(0)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	ret,frame = cap.read()
	
	#pass image info
	height = np.size(frame, 0)
	width = np.size(frame, 1)
	
	# init buffer
	lowerBuff = frame[lowerBuffHeight:,:]
	lastFrame = lowerGray = cv2.cvtColor(lowerBuff,cv2.COLOR_RGB2GRAY)
	fDiff=cv2.subtract(lastFrame,lastFrame)
	NavBuff = fDiff
	face = frame
	frameBuff = frame
	NavFullBuff = frame
	LowerMean = np.mean(lowerBuff)
	for ii in range(3):
		lastSections.append(lowerBuff[:,(width*ii/3):(width*(ii+1)/3)])
	#pass frame param
	MC.setFrameParam(width,height)
	lc.setCapParam(width,height)
	
	#set sub modules
	if llm.CheckBit(processFlag,0):
		loadVideoWriter()
	if llm.CheckBit(processFlag,2):
		LoadFaceTrack()
	Pflag = processFlag
	
# -------------- capture buffer updating ---------------	
	
def getFrame():
	global cap, frame,lastFrame,fDiff,lowerBuff,lowerGray,NavBuff,imgVar 
	ret, frame = cap.read()  # Read an frame from the webcam.
	#imgVar = np.var(frame) 
	#print imgVar
	#print "image var is ",imgDeviation
	#update lower buffer
	lowerBuff = frame[lowerBuffHeight:,:]
	lowerGray = cv2.cvtColor(lowerBuff,cv2.COLOR_RGB2GRAY)
	lowerVar = np.var(lowerGray)
	#print " lower image var is ", lowerVar
	blur = cv2.medianBlur(lowerGray,3)
	#NavBuff = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,7,7)
	NavBuff = cv2.absdiff(lastFrame,blur)
	
	lastFrame = blur
	
	# flash LED
	lc.ToggleLED2()
	return frame
	

def frameBufUpdate(flag):
	global frame, frameBuff,NavFullBuff
	global lowerBuff,lastFrame,NavBuff
	global lowerBuffHeight

	if llm.CheckBit(flag,1):
		NavFullBuff = frame
	if llm.CheckBit(flag,2):
		frameBuff = frame
	if llm.CheckBit(flag,0):
		WriteVideo(frame)
	

def WriteVideo(imag):
	out.write(imag)

# ------------------ sub module init ---------------------	
def LoadFaceTrack():
	global face_cascade
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	
	
def loadVideoWriter():
	global outflag
	outflag = 1
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	global out
	out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width,height),True)


# ---------------- video runtime func ---------------------
def runNav():
	realContour = []
	global lowerGray,NavBuff,lowerBuff,Kbuff
	ObsDetect(lowerBuff)
	
	
def getFaceLoc():
	x = 0
	y = 0
	global frameBuff
	Gray = cv2.cvtColor(frameBuff, cv2.COLOR_RGB2GRAY)
	faces = face_cascade.detectMultiScale(Gray, 1.3, 5)
	for (x,y,w,h) in faces:
		cv2.rectangle(frameBuff,(x,y),(x+w,y+h),(255,0,0),2)
	return x,y


def getContor(img):
	image,contours,h = cv2.findContours(img,1,2)
	return contours,h

	
def endCap():
	global outflag,cap,out
	cap.release()
	if outflag:
		out.release()
	lc.initLED()


def ObsDetect(img):
	global AutoCom,imgVar,NavBuff,fDiffL
	lim = 1000
	secMeans = []
	secVars = []
	sectionBuff = []
	imgHeight = np.size(img, 0)
	imgWidth = np.size(img, 1)
	for ii in range(3):
		section = (img[:,(imgWidth*ii/3):(imgWidth*(ii+1)/3)])
		secMeans.append(np.mean(section))
		secVars.append(np.var(section))
		sectionBuff.append(section)
	#print "secVar: ",secVars
	midSec = sectionBuff[1]
	secMeans[1] = np.mean(midSec[np.size(midSec, 1):,:])
	meanDiffL = abs(secMeans[0]-secMeans[1])
	meanDiffR = abs(secMeans[2]-secMeans[1])
	#print meanDiffL, "   ", meanDiffR

	fDiffL = NavBuff[:,:(imgWidth*1/3)]
	fDiffR = NavBuff[:,(imgWidth*2/3):imgWidth]
	ret,fDiffL = cv2.threshold(fDiffL, 20, 255, cv2.THRESH_BINARY)
	ret,fDiffR = cv2.threshold(fDiffL, 20, 255, cv2.THRESH_BINARY)
	contoursL,hL = getContor(fDiffL)
	contoursR,hR = getContor(fDiffR)
	contourNumL = len(contoursL)
	contourNumR = len(contoursR)
	
	####-------- decision making --------####
	if secVars[0]>lim and secVars[1]<lim and secVars[2]<lim or meanDiffL>40 or contourNumL>5:
		AutoCom = ord('d')
	elif secVars[2]>lim and secVars[1]<lim and secVars[0]<lim or meanDiffR>40 or contourNumR>5:
		AutoCom = ord('a')
	elif secVars[1]>lim or imgVar < 200:
		if meanDiffL>meanDiffR or contourNumR>contourNumL:
			AutoCom = ord('a')
		elif meanDiffR>meanDiffL or contourNumL>contourNumR:
			AutoCom = ord('d')
		else:
			AutoCom = ord('d')
	else:
		AutoCom = ord('w')
		
		
		
