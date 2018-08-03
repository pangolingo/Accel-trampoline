import time
import math
from MMA8452Q import MMA8452Q
from neopixel import *
import time
import atexit

mma8452q = MMA8452Q()

# file_handle = open("accel.dat", 'w')
# file_handle.write("# Num\tX\tY\tZ\n")
# i = 0
mma8452q.mode_configuration()
mma8452q.data_configuration()
time.sleep(0.5)

signaled = False

while True :
    accl = mma8452q.read_accl()
    g_force = math.sqrt(accl['x'] * accl['x'] + accl['y'] * accl['y'] + accl['z'] * accl['z'])
    #print("Acceleration in X-Axis : {}".format(accl['x']))
    #print("Acceleration in Y-Axis : {}".format(accl['y']))
    #print("Acceleration in Z-Axis : {}".format(accl['z']))
    print("Accel x: {}, y: {}, z: {}".format(accl['x'], accl['y'], accl['z']))
    #print("TOTAL: {}".format(g_force))
    if g_force > 2000 and not signaled:
        signaled = True
        print('WOW!')
    elif g_force <= 1200:
        signaled = False
    #print(" ************************************* ")
    # file_handle.write("{}\t{}\t{}\t{}\n".format(i, accl['x'], accl['x'], accl['x']))
    # i = i + 1
    time.sleep(0.1)

file_handle.close()
