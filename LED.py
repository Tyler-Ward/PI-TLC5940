#!/usr/bin/python

LEDLocation= {}
LEDLocation["R-1"] = 7
LEDLocation["R0"] = 15
LEDLocation["R1"] = 0
LEDLocation["R2"] = 1
LEDLocation["R3"] = 2
LEDLocation["R4"] = 3
LEDLocation["R5"] = 4
LEDLocation["R6"] = 5
LEDLocation["R7"] = 6

LEDLocation["R8"] = 9
LEDLocation["R9"] = 10

LEDLocation["Y0"] = 7
LEDLocation["Y1"] = 8
LEDLocation["Y3"] = 11

import datetime
import math

def millis():
   dt = datetime.datetime.now()
   ms = (dt.second) * 1000 + dt.microsecond / 1000.0
   return ms

# led functions

def breathe(settings):
	#settings=(period,brightness)
	rate=2*math.pi/settings[0]
	return int(settings[1]*(math.sin(float(millis()*rate))+1)/2)


def blink(settings):
	#settings=(period,ontime,offset,brightness)

	blinkprogress = (int(millis())+settings[2]) % settings[0]
	if blinkprogress >= settings[1]:
		return 0
	else:
		return settings[3]

def off(settings):
	return 0
	

Brightness=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
ledmode=[blink,blink,breathe,off,off,off,off,breathe,off,off,off,off,off,off,off,off]
ledsettings=[(10000,5000,0,4000),(10000,5000,5000,4000),(10000,4000),(0),(0),(0),(0),(5000,4000),(0),(0),(0),(0),(0),(0),(0),(0)]


if __name__ == "__main__":
	import TLC5940
	import time
	TLC5940.resetTLC()

	while(1):
		for i in range(len(ledmode)):
			Brightness[i]=ledmode[i](ledsettings[i])
		TLC5940.setTLCvalue(TLC5940.buildvalue(Brightness,TLC5940.regPWM),TLC5940.regPWM)

	


	#ledfunc=[("R1",3000,1),("R2",3000,0.01),("R1",0,1),("R3",3000,0.01),("R2",0,1),("R3",0,5)]
	#ledfunc=[]
	#for led in range(5):
	#	#ledfunc=[("R0",3000),("R1",3000),("R0",0)]
	#	ledfunc.append(("R"+str(led),3000,1))
	#	ledfunc.append(("R"+str(led-1),0,1))
	#while(1):
	#	for led in range(len(ledfunc)):
	#		loc=ledfunc[led][0]
	#		Brightness[LEDLocation[loc]]=ledfunc[led][1]
	#		time.sleep(ledfunc[led][2])
	#		TLC5940.setTLCvalue(TLC5940.buildvalue(Brightness,TLC5940.regPWM),TLC5940.regPWM)
	#
	#	print "done"
	
