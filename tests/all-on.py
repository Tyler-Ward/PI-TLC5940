from TLC5940 import *
import math
import sys

brightness = 4000;
if len(sys.argv) == 2:
        brightness = int(sys.argv[1])

resetTLC()

val = [brightness]*16*5
setTLCvalue(buildvalue(val, regPWM), regPWM)

