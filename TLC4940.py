#!/usr/bin/python

import RPi.GPIO as GPIO
import spidev
import time

XLAT=4
VPRG=17

# setup rpi.gpio pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(XLAT, GPIO.OUT)
GPIO.setup(VPRG, GPIO.OUT)

# setup serial

spi = spidev.SpiDev()
spi.open(0,0)

#constants

# VPRG settings for registers
regDC=1
regPWM=0

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
		print str(output) + " = " + str(values[output])
		print bin(values[output])
		for char in bin(values[output])[2:].zfill(reglength)[::-1]:
			if char=="1":
				bitstream.append(1)
			elif char =="0":
				bitstream.append(0)
	#print bitstream
	print bitstream[::-1]
	for bitoffset in range(0,len(bitstream),8):
		outbyte=0
		for bit in range(8):
			if bitstream[::-1][bitoffset+bit]==1:
				outbyte+=2**(7-bit)
		print outbyte
		out.append(outbyte)

	print out
	return out			
				
def setTLCvalue(data,DCMode):

	# put the chip into DC mode	
	GPIO.output(VPRG, DCMode)
	
	print spi.xfer2(data)

	# latch data
	GPIO.output(XLAT, GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(XLAT, GPIO.LOW)

	GPIO.output(VPRG, GPIO.LOW)


def resetTLC():
	# resets the chip to its default state
	setTLCvalue([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255],regPWM)
	setTLCvalue([255,255,255,255,255,255,255,255,255,255,255,255],regDC)	


if __name__ == "__main__":

	resetTLC()
	import math

	i=0
	# pulsate by changeing brightness
	while(1):
		val = int(63*(math.sin(float(i))+1)/2)
		i+=0.1
		print val
		setTLCvalue(buildvalue([val,val,val,val,val,val,val,val,val,val,val,val,val,val,val,val],regDC),regDC)	
		time.sleep(0.1)

