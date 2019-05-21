#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

extern "C"
{
	int CheckBit(int data, int bit) {return (data>>bit) & 0x01;}
	int setBit(int data, int bit, int state);
	int setMapBit(int data, int map, int state);
}

int setBit(int data, int bit, int state)
{
	int temp = 0;
	if(state){temp = data|(0x01<<bit);}
	else{temp = data&~((0x01<<bit));}
	return temp;}

int setMapBit(int data, int map, int state)
{
	int temp = 0;
	if(state){temp = data|map;}
	else{temp = data&~map;}
	return temp;}
