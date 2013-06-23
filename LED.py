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

def hueblend(settings):
	#settings=(period,offset,brightness,colour(r=1,g=2,b=3))
	# colour acts as angle offset

	if settings[3] == 1:
		coloffset = 0
	elif settings[3] == 2:
		coloffset = 120
	elif settings[3] == 3:
		coloffset = 240


	progress = (int(millis())+settings[1]) % settings[0]
	deg = (float(progress) / float(settings[0]) * float(360) + float(coloffset))%360
	#print deg

	# create blends
	if deg < 60:
    		val=settings[2]
   	elif ((deg >= 60) and (deg < 120)):
		val=settings[2] - (((deg - 60) * settings[2])/60) #drops
	elif ((deg >= 120) and (deg < 240)):
		val=0
	elif ((deg >= 240) and (deg < 300)):
		val=((deg - 240) * settings[2])/60 # rises
	elif (deg >= 300):
		val=settings[2] 

	return int(val)


def off(settings):
	return 0

def constant(settings):
	return settings[0]
	
#Brightness=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#ledmode=[hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,hueblend,off]

#ledsettings=[(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3),(0)]

count=5

Brightness=[0]*16*count
print Brightness
tempmode=[hueblend]*15
tempmode.append(off)
ledmode=tempmode*count
print ledmode
ledsettings=[(10000,0,4000,1),(10000,0,4000,2),(10000,0,4000,3)]*5
ledsettings.append(0)
ledsettings=ledsettings*count
print ledsettings

if __name__ == "__main__":
	import TLC5940
	import time
	TLC5940.resetTLC()

	while(1):
		for i in range(len(ledmode)):
			Brightness[i]=ledmode[i](ledsettings[i])
		TLC5940.setTLCvalue(TLC5940.buildvalue(Brightness,TLC5940.regPWM),TLC5940.regPWM)
#		time.sleep(0.25)

	


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
	
