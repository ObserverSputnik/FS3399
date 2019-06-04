this is project FS3399. A part of FlashSnail project.
this project runs on nanoPi NEO4, with RK3399 CPU.

file structure:
	      FS.py
	    /   |   \
	   /thread.py\
	  /   /   \   \
      Vision.py   MotionControl.py
	  |     X  	 |
          |    / \ 	 |
lowLevelCom.cpp   lowLevelMath.cpp
  
Hardware structure:
 
			    ---battery ADC
       USB	  UART	   /      PWM
camera-----RK3399------STM32F103------Motors
		\	   \
		 ---LED     ---buttons
							 
							 
before you use the code:
	1. you need a RK3399 based board to run the control code.
	2. STM32 codes are here: https://github.com/ObserverSputnik/Flashsnail
	3. compile lowLevelCom.cpp and lowLevelMath.cpp first. magic.sh would do them for you if you running linux.
  


