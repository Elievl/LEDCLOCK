import array, utime, math
from machine import Pin
import rp2
import machine

# Configure the number of WS2812 LEDs.
NUM_LEDS = 122
PIN_NUM = 21
previousTick = 0
brightness = 0.5
normalbrightness = 0.5
addedMins = 0
addedHours = 0
lastPressed = utime.ticks_ms() 

increaseMins = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

hourToSet = 0
minuteToSet = 0
debugmode = 2

NAOMI = [16,28,40,48,64]
ELIE = [75,81,95,105]
NATHAN = [16,29,38,51,60,73]
MATHIS = [17,28,39,50,61,72]


BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

DARKRED = (50,0,0)
PINK = (255,0,255)
DARKGREEN = (0,100,0)
ROSE = (255,20,150)
BROWN = (139,96,20)
BEIGE = (245,245,220)
ORANGE = (255,165,0)

COLORLIST = [RED, GREEN, BLUE, PURPLE , BROWN, WHITE, RED, GREEN, BLUE, PURPLE, BROWN, BEIGE, RED, GREEN, BLUE, PURPLE , BROWN, WHITE, RED, GREEN, BLUE, PURPLE, BROWN, BEIGE, RED, GREEN, BLUE, PURPLE , BROWN, WHITE, RED, GREEN, BLUE, PURPLE, BROWN, BEIGE, WHITE]

###########################################################################################################

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################

class ledConfig:
    def __init__(self, name, onOff, color):
        self.name = name
        self.onOff = onOff
        self.colorToSet = wheel(color)
    def blackout():
        self.intensity = 0
        self.onOff = 0
        self.colorToSet = BLACK

##########################################################################

def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

############# END OF PIXEL SETTING CORE #################


############## ANIMATIONS ###############################

def fadeToBlack(duration):
    global brightness
    global normalbrightness
    for i in range(50):
        brightness = brightness/1.1
        pixels_show()
    brightness = 0
    pixels_show()
    brightness = normalbrightness
    reflectConfig(getEmptyConfig(NUM_LEDS))
        
def fadeInToConfig(strandConfig, duration):
    global brightness
    global normalbrightness
    print("fading in")
    brightness = 0
    pixels_show()
    for i in range(NUM_LEDS):
        if (strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = colorToSet
    reflectConfig(strandConfig)
    increaseBright = (normalbrightness-brightness)/50
    for i in range(50):
        brightness = brightness + increaseBright
        print("brightness = ", brightness)
        pixels_show()
    brightness = normalbrightness
    pixels_show()
    print("fade done")

def animationCoffee(speed):
    COFFEECUP = [54,53,52,51,50,49,48,57,76,79,98,101,63,85,92,107,119,118,117,116,115,64,65,67,88,90,91]
    COFFEESMOKE1 = [11,13,31,8,16,28]
    COFFEESMOKE2 = [10,14,30,7,17,27]
    COFFEESMOKE3 = [9,15,29,6,18,26]    
    for i in range (0,4):
        for lednumber in range(NUM_LEDS):
            pixels_set(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            pixels_set(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE1:
            pixels_set(lednumber-1, WHITE)
        pixels_show()
        utime.sleep(speed/10)
        for lednumber in range(NUM_LEDS):
            pixels_set(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            pixels_set(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE2:
            pixels_set(lednumber-1, WHITE)
        pixels_show()
        utime.sleep(speed/10)
        for lednumber in range(NUM_LEDS):
            pixels_set(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            pixels_set(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE3:
            pixels_set(lednumber-1, WHITE)
        pixels_show()
        utime.sleep(speed/10)

def animationSpiral(colorToSet, speed):
    SEQUENCESPIRAL = [11,10,9,8,7,6,5,4,3,2,1,22,23,44,45,66,67,88,89,110,111,112,113,114,115,116,117,118,119,120,121,100,99,78,77,56,55,34,33,12,13,14,15,16,17,18,19,20,21,24,43,46,65,68,87,90,109,108,107,106,105,104,103,102,101,98,79,76,57,54,35,32,31,30,29,28,27,26,25,42,47,64,69,86,91,92,93,94,95,96,97,80,75,58,53,36,37,38,39,40,41,48,63,70,85,84,83,82,81,74,59,52,51,50,49,62,71,72,73,60,61]
    for i in range(NUM_LEDS-1):
        pixels_set(SEQUENCESPIRAL[i]-1, colorToSet)
        pixels_show()
        utime.sleep(speed/1000.0)
    fadeToBlack(5)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        utime.sleep(wait)

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

#CLOCK METHODS
def getEmptyConfig(lengthNeeded):
    emptyConfig = []
    for i in range (0, lengthNeeded+1):
        emptyConfig.append(ledConfig(i,0,0))
        emptyConfig[i].colorToSet = BLACK
    return emptyConfig

def getConfigWithSetTime(lengthNeeded, colorToSet, hourToSet, minuteToSet):
    HETIS = [6,7,9,10,11]
    strandConfig = getEmptyConfig(lengthNeeded-1)
    if(hourToSet > 12):
        hourToSet = hourToSet - 12
    if(hourToSet == 0):
        hourToSet = 12
    if(debugmode > 2):
        print("hourToSet: ", hourToSet)
        print("minuteToSet: ", minuteToSet)
    if (minuteToSet >= 20):
        if(hourToSet == 12):
            hourToSet = 1
        else:
            hourToSet = hourToSet + 1
    strandConfig = addToConfig(strandConfig,HETIS, colorToSet)
    strandConfig = addHourToConfig(strandConfig, hourToSet, colorToSet)
    strandConfig = addMinuteToConfig(strandConfig, minuteToSet, colorToSet)
    return strandConfig

def setAColorForConfig(strandConfig, colorToSet):
    for i in range(NUM_LEDS):
        if (strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = colorToSet
    reflectConfig(strandConfig)
    
def reflectConfig(strandConfig):
    for i in range(NUM_LEDS):
        pixels_set(i-1, strandConfig[i].colorToSet)
    pixels_show()

def addToConfig(strandConfig,lights, colorToSet):
    for i in lights:
#        print("adding on config: ",i)
        strandConfig[i].onOff = 1
        strandConfig[i].colorToSet = colorToSet
    return strandConfig

def addHourToConfig(strandConfig, hour, colorToSet):
#    print("setting hour")
    EEN = [45,46,47]
    TWEE = [56,57,58,59]
    DRIE = [62,63,64,65]
    VIER = [74,75,76,77]
    VIJF = [67,68,69,70]
    ZES = [78,79,80]
    ZEVEN = [84,85,86,87,88]
    ACHT = [96,97,98,99]
    NEGEN = [89,90,91,92,93]
    TIEN = [101,102,103,104]
    ELF = [108,109,110]
    TWAALF = [116,117,118,119,120,121]
    HOURS = [EEN,TWEE,DRIE,VIER,VIJF,ZES,ZEVEN,ACHT,NEGEN,TIEN,ELF,TWAALF]

    strandConfig = addToConfig(strandConfig, HOURS[hour-1], colorToSet)
    return strandConfig

def addMinuteToConfig(strandConfig, minute, colorToSet):
#    print("setting minutes")
    UUR = [111,112,113]
    VIJFOVER = [1,2,3,4,30,31,32,33]
    TIENOVER = [12,13,14,15,30,31,32,33]
    KWARTOVER = [23,24,25,26,27,41,42,43,44]
    TIENVOORHALF = [12,13,14,15,19,20,21,22,34,35,36,37]
    VIJFVOORHALF = [1,2,3,4,19,20,21,22,34,35,36,37]
    HALF = [34,35,36,37]
    VIJFOVERHALF = [1,2,3,4,30,31,32,33,34,35,36,37]
    TIENOVERHALF = [12,13,14,15,30,31,32,33,34,35,36,37]
    KWARTVOOR = [23,24,25,26,27,52,53,54,55]
    TIENVOOR = [12,13,14,15,19,20,21,22]
    VIJFVOOR = [1,2,3,4,19,20,21,22]
    if(minute < 5):strandConfig=addToConfig(strandConfig,UUR, colorToSet)
    elif(minute < 10):strandConfig=addToConfig(strandConfig,VIJFOVER, colorToSet)
    elif(minute < 15):strandConfig=addToConfig(strandConfig,TIENOVER, colorToSet)
    elif(minute < 20):strandConfig=addToConfig(strandConfig,KWARTOVER, colorToSet)
    elif(minute < 25):strandConfig=addToConfig(strandConfig,TIENVOORHALF, colorToSet)
    elif(minute < 30):strandConfig=addToConfig(strandConfig,VIJFVOORHALF, colorToSet)
    elif(minute < 35):strandConfig=addToConfig(strandConfig,HALF, colorToSet)
    elif(minute < 40):strandConfig=addToConfig(strandConfig,VIJFOVERHALF, colorToSet)
    elif(minute < 45):strandConfig=addToConfig(strandConfig,TIENOVERHALF, colorToSet)
    elif(minute < 50):strandConfig=addToConfig(strandConfig,KWARTVOOR, colorToSet)
    elif(minute < 55):strandConfig=addToConfig(strandConfig,TIENVOOR, colorToSet)
    else:strandConfig=addToConfig(strandConfig,VIJFVOOR, colorToSet)
    return strandConfig

def buttonPressed(irq):
    global lastPressed
    global addedMins
    global addedHours
    hoursToAdd = 0
    minsToAdd = 0
    time_ms = utime.ticks_us()
    delay = utime.ticks_diff(time_ms, lastPressed)
    if(delay < 200000):
        return
    if(delay > 500000): # simple click
        lastPressed = time_ms
        addedMins = addedMins + 5
        if(addedMins >= 60):
            addedMins = addedMins - 60 
    else: # it is a double click
        lastPressed = time_ms
        addedMins = addedMins - 5
        addedHours = addedHours + 1
        if(addedHours >= 24):
            addedHours = 0
        if(addedMins <= 0):
            addedMins = addedMins + 60        
    print("mins added: ", addedMins)
    print("hours added: ", addedHours)
    
# PROG STARTS HERE
strandConfig = []
newConfig = []
colorToSet = PURPLE

# temp monitoring
#sensor_temp = machine.ADC(4)
#conversion_factor = 3.3 / (65535)
pixels_fill(BLACK)

while True:
    print("processor time: ", utime.localtime()[3], ":", utime.localtime()[4], ":", utime.localtime()[5])
    hourToSet = utime.localtime()[3] + addedHours
    minuteToSet = utime.localtime()[4] + addedMins
    if(minuteToSet >= 60):
        minuteToSet = minuteToSet - 60
        hourToSet = hourToSet + 1
    secondsToSet = utime.localtime()[5]
    colorToSet = COLORLIST[hourToSet]
    print("corrected time: ", hourToSet, ":", minuteToSet, ":", secondsToSet)
    
    # SHOW COFFEE ANIMATION BETWEEN 4 AND 5 PM
    if(hourToSet >= 16 and hourToSet <= 17 and minuteToSet%5 == 0 and secondsToSet < 3):
        animationCoffee(4)
    # RUN SPIRAL ON THE HOUR
    if(minuteToSet == 0 and secondsToSet < 2):
        animationSpiral(colorToSet, 5)
#    print("time is now: ", hourToSet, ":", minuteToSet, ":", secondsToSet)
# set lightstrip
    strandConfig = getEmptyConfig(NUM_LEDS)
    newConfig = getConfigWithSetTime(len(strandConfig), colorToSet, hourToSet, minuteToSet)
    reflectConfig(newConfig)
#    fadeInToConfig(newConfig,2)
    if(increaseMins.value()):
        print("VALUE!")
        utime.sleep(0.2)
        addedMins = addedMins + 5
        if(addedMins >= 60):
            addedMins = addedMins - 60
            addedHours = addedHours + 1
    else:
        utime.sleep(0.2)

#    increaseMins.irq(trigger = machine.Pin.IRQ_RISING, handler = buttonPressed)
    
