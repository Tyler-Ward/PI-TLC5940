from TLC5940 import *
import math
import sys

sl = 5.0;
if len(sys.argv) == 2:
	sl = float(sys.argv[1])

resetTLC()

for id in range(0, 16*5, 1):
	val = [0]*id + [4000] + [0]*(16*5 - id - 1)
	print val
	setTLCvalue(buildvalue(val, regPWM), regPWM)
	time.sleep(sl)

