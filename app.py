import time
import math
from MMA8452Q import MMA8452Q
from neopixel import *
import time
import atexit

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def colorAll(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

def exit_handler():
    print("Clearing strip before exit")
    colorAll(strip, Color(0,0,0))
    print("Goodbye")

atexit.register(exit_handler)
#colorWipe(strip, Color(0, 0, 255))
mma8452q = MMA8452Q()

# file_handle = open("accel.dat", 'w')
# file_handle.write("# Num\tX\tY\tZ\n")
# i = 0
mma8452q.mode_configuration()
mma8452q.data_configuration()
time.sleep(0.5)

signaled = False

colors = [ Color(0,255,0), Color(255,0,0), Color(0,0,255) ] 
current_color = 0

while True :
    accl = mma8452q.read_accl()
    g_force = math.sqrt(accl['x'] * accl['x'] + accl['y'] * accl['y'] + accl['z'] * accl['z'])
    #print("Acceleration in X-Axis : {}".format(accl['x']))
    #print("Acceleration in Y-Axis : {}".format(accl['y']))
    #print("Acceleration in Z-Axis : {}".format(accl['z']))
    print("TOTAL: {}".format(g_force))
    if g_force > 2000 and not signaled:
        signaled = True
        print('WOW!')
        color_to_show = colors[current_color]
        colorAll(strip, color_to_show)
        current_color= current_color + 1
        if current_color >= len(colors):
            current_color = 0
    elif g_force <= 1200:
        signaled = False
        colorAll(strip, Color(0,0,0))
    #print(" ************************************* ")
    # file_handle.write("{}\t{}\t{}\t{}\n".format(i, accl['x'], accl['x'], accl['x']))
    # i = i + 1
    time.sleep(0.1)

file_handle.close()
