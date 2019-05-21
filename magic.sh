#!/bin/bash
g++ -Wall -c lowLevelCom.cpp -o lowLevelCom.o -fPIC -lpthread -lwiringPi -lrt -lm -lcrypt
g++ -Wall -shared -Wl,-soname,lowLevelCom.so -o lowLevelCom.so lowLevelCom.o -lpthread -lwiringPi -lrt -lm -lcrypt

g++ -Wall -c lowLevelMath.cpp -o lowLevelMath.o -fPIC -lpthread -lrt -lm -lcrypt
g++ -Wall -shared -Wl,-soname,lowLevelMath.so -o lowLevelMath.so lowLevelMath.o -lrt -lm -lcrypt
