#!/usr/bin/python

import datetime
import math
#import thread
import TLC5940
from multiprocessing import Process, Queue, Manager
import time

def millis():
   dt = datetime.datetime.now()
   ms = (dt.second) * 1000 + dt.microsecond / 1000.0
   return ms


######################################
# led functions
######################################

def breathe(period, maxbrightness, minbrightness=0, offset=0,  *other, **kwargs):
	rate=2*math.pi/period
	brightness=maxbrightness-minbrightness
	return int((brightness*(math.sin(float(millis()*rate)-offset)+1)/2)+minbrightness)


def blink(period,ontime,offset,brightness, *other, **kwargs):
	blinkprogress = (int(millis())-offset) % period 
	if blinkprogress >= ontime:
		return 0
	else:
		return brightness

def hueblend(period,offset,brightness,colour, *other, **kwargs):
	# colour acts as angle offset

	if colour == 1:
		coloffset = 0
	elif colour == 2:
		coloffset = 120
	elif colour == 3:
		coloffset = 240


	progress = (int(millis())+offset) % period 
	deg = (float(progress) / float(period) * float(360) + float(coloffset))%360
	#print deg

	# create blends
	if deg < 60:
		val=brightness
	elif ((deg >= 60) and (deg < 120)):
		val=brightness - (((deg - 60) * brightness)/60) #drops
	elif ((deg >= 120) and (deg < 240)):
		val=0
	elif ((deg >= 240) and (deg < 300)):
		val=((deg - 240) * brightness)/60 # rises
	elif (deg >= 300):
		val=brightness

	return int(val)


def off(*other, **kwargs):
	return 0

def constant(value, *other, **kwargs):
	return value 

###################################
# led mode mixers
###################################


	
def pulse(mode0,mode0settings,mode1,mode1settings,pulsesettings,ledid, instance, *other):
	endtime = pulsesettings[0]
	now=millis()
	if now >= endtime: 
		instance.clearmixer(ledid,0)
		return mode0(*mode0settings, instance=instance)
	else:
		return mode1(*mode1settings, instance=instance)

def modeblend(mode0,mode0settings,mode1,mode1settings,blendsettings,ledid, instance, *other):
	starttime = blendsettings[0]
	endtime = blendsettings[1]

	now=millis()
	if now <= starttime:
		return mode0(*mode0settings, instance=instance)
	else:
		if now >= endtime:
			instance.clearmixer(ledid,1)
			return mode1(*mode1settings, instance=instance)
		else:
			progress=(now-starttime)/(endtime-starttime)
			outgoing=(1-progress)*mode0(*mode0settings, instance=instance)
			incoming=progress*mode1(*mode1settings, instance=instance)
			return int(outgoing+incoming)

class LEDController:

	###################################
	# mixer mode helpers
	###################################

	def setmixer(self,ledid,newmode,newmodesettings,mixer,mixersettings):
		oldmode=self.mode[ledid]
		oldsettings=self.settings[ledid]
		self.mode[ledid]=mixer
		self.settings[ledid]=(oldmode,oldsettings,newmode,(newmodesettings),(mixersettings),ledid)
	
	def setmodemixer(self,data,mixer,mixersettings):
		for i in range(len(self.settings)):
			self.setmixer(i,data[0][i],data[1][i],mixer,mixersettings)
		self.setconfig(self.mode, self.settings)

	def clearmixer(self,ledid,new):
		if new==1:
			self.mode[ledid]=self.settings[ledid][2]
			self.settings[ledid]=self.settings[ledid][3]
		else:
			self.mode[ledid]=self.settings[ledid][0]
			self.settings[ledid]=self.settings[ledid][1]
		self.setconfig(self.mode, self.settings)


	###################################
	# led processing commands
	###################################

	def __init__(self, count):
		self.count = count
		self.brightness = [0]*16*count
		self.mode = [off]*16*count
		self.settings = [(0,)]*16*count
		self.queue = Queue()

	def setconfig(self, mode, settings):
		self.settings = settings
		self.mode = mode
		#print self.mode
		#print self.settings
		self.queue.put([mode, settings])

	def startledcontroler(self):
		p = Process(target=self.ledcontroler,args=(self.queue,))
		p.daemon = True
		p.start()


	def setmode(self, data):
		print "use of depricated setmode"
		self.setconfig(data[0], data[1])


	def ledcontroler(self, queue):
		while(1):
			while not queue.empty():
				(self.mode, self.settings) = self.queue.get()
			for i in range(len(self.settings)):
				self.brightness[i]=self.mode[i](*(self.settings[i]), instance=self)
			TLC5940.setTLCvalue(TLC5940.buildvalue(self.brightness,TLC5940.regPWM),TLC5940.regPWM)

if __name__ == "__main__":
	# run a simple test of breathe animation
	
	print "test where out of date and have been removed"
