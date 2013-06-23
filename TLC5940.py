#!/usr/bin/python

import RPi.GPIO as GPIO
#import spidev
import spi
import time
from threading import Thread

XLAT=4
VPRG=17

BLANK=23
GSCLK=18

# setup rpi.gpio pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(XLAT, GPIO.OUT)
GPIO.setup(VPRG, GPIO.OUT)

GPIO.setup(BLANK, GPIO.OUT)
GPIO.setup(GSCLK, GPIO.OUT)

# setup serial

#spi = spidev.SpiDev()
#spi.open(0,0)

spi.openSPI(speed=25000)

#constants

# VPRG settings for registers
regDC=1
regPWM=0

def runGSCLK():
	i=0
	while(1):
		i+=1
		if i>=1096:
			print "reset"
			GPIO.output(BLANK,1)
			GPIO.output(BLANK,0)
			i=0
		else:
			GPIO.output(GSCLK,1)
			GPIO.output(GSCLK,0)

def buildvalue(values, register):

	# need to convert values in port order (0->16) into byte order MSB first (16->0)
	
	bitstream=[]
	out=[]
	
	if register==regDC:
		reglength=6
	elif register==regPWM:
		reglength=12
	else:
		print "error unrecognised register"
		return []
		

	# for every element in array 
	for output in range(len(values)):
		#print str(output) + " = " + str(values[output])
		#print bin(values[output])[2:].zfill(reglength)
		#print reglength
		for char in bin(values[output])[2:].zfill(reglength)[::-1]:
			if char=="1":
				bitstream.append(1)
			elif char =="0":
				bitstream.append(0)
	#print bitstream
	#print bitstream[::-1]
	for bitoffset in range(0,len(bitstream),8):
		outbyte=0
		for bit in range(8):
			if bitstream[::-1][bitoffset+bit]==1:
				outbyte+=2**(7-bit)
		#print outbyte
		out.append(outbyte)

	#print out
	return out			
				
def setTLCvalue(data,DCMode):

	# put the chip into DC mode	
	GPIO.output(VPRG, DCMode)
	#print tuple(data)
	spi.transfer(tuple(data))

	# latch data
	GPIO.output(XLAT, GPIO.HIGH)
	#time.sleep(0.25)
	GPIO.output(XLAT, GPIO.LOW)

	GPIO.output(VPRG, GPIO.LOW)


def resetTLC():
	# resets the chip to its default state
	setTLCvalue([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255],regPWM)
	setTLCvalue(buildvalue([33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33,33],regDC),regDC)	

if __name__ == "__main__":

	resetTLC()
	import math

	for id in range(0, 16*5, 1):
		val = [0]*id + [4000] + [0]*(16*5 - id - 1)
		print val
		setTLCvalue(buildvalue(val, regPWM), regPWM)
		time.sleep(5)
	exit()

#	i=0
#	for val in range(0,4096,100):
#		print val
#		red=val
#		green=val
#		blue=val
#		setTLCvalue(buildvalue([red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0,red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0,red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0],regPWM),regPWM)
#		time.sleep(0.5)	
#	exit()
#	for val in range(4096):
#		print val
#		setTLCvalue(buildvalue([0,0,val,0,0,val,0,0,val,0,0,val,0,0,val,0,0,0,val,0,0,val,0,0,val,0,0,val,0,0,val,0,0,0,val,0,0,val,0,0,val,0,0,val,0,0,val,0],regPWM),regPWM)
#		time.sleep(0.01)
#
#	# pulsate by changeing brightness
#	while(1):
#		val = int(4000*(math.sin(float(i))+1)/2)
#		i+=0.01
#		print val
#		red=val
#		green=val
#		blue=val
#		setTLCvalue(buildvalue([red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0,red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0,red,green,blue,red,green,blue,red,green,blue,red,green,blue,red,green,blue,0],regPWM),regPWM)
#		time.sleep(0.01)

