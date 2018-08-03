import time
import math
from Accel import Accel
import time
import atexit
import sys

deviceName = 0x1a

MMA8451 = Accel()

# file_handle = open("accel.dat", 'w')
# file_handle.write("# Num\tX\tY\tZ\n")
# i = 0
MMA8451.init()
time.sleep(0.5)
# if MMA8451.whoAmI() != deviceName:
#    print("Error! Device not recognized! (" + str(deviceName) + ")")
#    print(MMA8451.whoAmI())
#    sys.exit()

signaled = False

MMA8451.debugShowRpiInfo()
MMA8451.debugShowRegisters()    
MMA8451.debugShowOrientation()

while True :
    accl = MMA8451.getAxisValue()
    MMA8451.debugShowAxisAcceleration(accl['x'], accl['y'], accl['z']) 
    g_force = math.sqrt(accl['x'] * accl['x'] + accl['y'] * accl['y'] + accl['z'] * accl['z'])
    #print("Acceleration in X-Axis : {}".format(accl['x']))
    #print("Acceleration in Y-Axis : {}".format(accl['y']))
    #print("Acceleration in Z-Axis : {}".format(accl['z']))
    print("TOTAL: {}".format(g_force))
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
