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

def buildvalue(values):

	# need to convert values in port order (0->16) into byte order lsb first (16->0)
	
	bitstream=[]
	out=[]
	

	# for every element in array 
	for output in range(len(values)):
		print str(output) + " = " + str(values[output])
		print bin(values[output])
		for char in bin(values[output])[2:].zfill(6)[::-1]:
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
	
	spi.xfer2(data)

	# latch data
	GPIO.output(XLAT, GPIO.HIGH)
	time.sleep(0.025)
	GPIO.output(XLAT, GPIO.LOW)

	GPIO.output(VPRG, GPIO.LOW)


def resetTLC():
	setTLCvalue([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255],regPWM)
	setTLCvalue([255,255,255,255,255,255,255,255,255,255,255,255],regDC)	


if __name__ == "__main__":

	resetTLC()

	for val in range(0, 63):
		print val
		setTLCvalue(buildvalue([val,val,val,val,val,val,val,val,val,val,val,val,val,val,val,val]),regDC)	
		time.sleep(0.5)

