#!/usr/bin/python

import datetime
import math
import thread
import TLC5940

def millis():
   dt = datetime.datetime.now()
   ms = (dt.second) * 1000 + dt.microsecond / 1000.0
   return ms


######################################
# led functions
######################################

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

###################################
# led mode mixers
###################################

def setmixer(ledid,newmode,newmodesettings,mixer,mixersettings):
	oldmode=ledmode[ledid]
	oldsettings=ledsettings[ledid]
	ledmode[ledid]=mixer
	ledsettings[ledid]=(oldmode,oldsettings,newmode,(newmodesettings),(mixersettings),ledid)

def clearmixer(ledid,new):
	print "clearing " + str(ledid)
	if new==1:
		ledmode[ledid]=ledsettings[ledid][2]
		ledsettings[ledid]=ledsettings[ledid][3]
	else:
		ledmode[ledid]=ledsettings[ledid][0]
		ledsettings[ledid]=ledsettings[ledid][1]

def pulse(settings):
	#settings(mode0,mode0settings,mode1,mode1settings,pulsesettings,ledid)
	#pulsesettings(endtime)

	now=millis()
	if now >= settings[4][0]:
		clearmixer(settings[5],0)
		return settings[0](settings[1])
	else:
		return settings[2](settings[3])

def modeblend(settings):
	#settings(mode0,mode0settings,mode1,mode1settings,blendsettings,ledid)
	#blendsettings(starttime,endtime)

	now=millis()
	if now <= settings[4][0]:
		return settings[0](settings[1])
	else:
		if now >= settings[4][1]:	
			clearmixer(settings[5],1)
			return settings[2](settings[3])
		else:
			progress=(now-settings[4][0])/(settings[4][1]-settings[4][0])
			outgoing=(1-progress)*settings[0](settings[1])
			incoming=progress*settings[2](settings[3])
			return int(outgoing+incoming)



###################################
# led processing commands
###################################

def startledcontroler():
	thread.start_new_thread(ledcontroler,())

def ledcontroler():
	while(1):
		for i in range(len(ledmode)):
			Brightness[i]=ledmode[i](ledsettings[i])
		TLC5940.setTLCvalue(TLC5940.buildvalue(Brightness,TLC5940.regPWM),TLC5940.regPWM)

####################################
# default values
####################################

Brightness=[]
ledmode=[]
ledsettings=[]


if __name__ == "__main__":
	# run a simple test of breathe animation
	import time
	TLC5940.resetTLC()
	
	Brightness=[0]*16
	ledmode=[breathe]*16
	ledsettings=[(10000,3000)]*16	
	
	startledcontroler()
	time.sleep(20)
	ledsettings=[(2000,3000)]*16
	time.sleep(1000)
