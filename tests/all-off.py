from TLC5940 import *
import math

resetTLC()

val = [0]*16*5
setTLCvalue(buildvalue(val, regPWM), regPWM)

