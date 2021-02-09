# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import datetime
import time
from rpi_ws281x import *
import argparse
import random

#LED STRIP CONFIG
LED_COUNT      = 121      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# variables for clock setting
currentHourShown = 0
currentMinuteShown = 0
hourToSet = 0
minuteToSet = 0

# switch on to debug
debugmode = 1

#choose minute pins
#MINUTE1 = []
#MINUTE2 = []
#MINUTE3 = []
#MINUTE4 = []

WHITE = Color(255,255,255)
BLACK = Color(0,0,0)
RED = Color(255,0,0)
DARKRED = Color(50,0,0)
PINK = Color(255,0,255)
GREEN = Color(0,255,0)
DARKGREEN = Color(0,100,0)
BLUE = Color(0,0,255)
ROSE = Color(255,20,150)
BROWN = Color(139,96,20)
BEIGE = Color(245,245,220)
YELLOW = Color(255,150,0)
ORANGE = Color(255,165,0)
PURPLE = Color(180,0,255)
CYAN = Color(0,255,255)

HETIS = [6,7,9,10,11]
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
UUR = [111,112,113]
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
NAOMI = [16,28,40,48,64]
ELIE = [75,81,95,105]
NATHAN = [16,29,38,51,60,73]
MATHIS = [17,28,39,50,61,72]

HOURS = [EEN,TWEE,DRIE,VIER,VIJF,ZES,ZEVEN,ACHT,NEGEN,TIEN,ELF,TWAALF]

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
UUR = [111,112,113]

SEQUENCESPIRAL = [11,10,9,8,7,6,5,4,3,2,1,22,23,44,45,66,67,88,89,110,111,112,113,114,115,116,117,118,119,120,121,100,99,78,77,56,55,34,33,12,13,14,15,16,17,18,19,20,21,24,43,46,65,68,87,90,109,108,107,106,105,104,103,102,101,98,79,76,57,54,35,32,31,30,29,28,27,26,25,42,47,64,69,86,91,92,93,94,95,96,97,80,75,58,53,36,37,38,39,40,41,48,63,70,85,84,83,82,81,74,59,52,51,50,49,62,71,72,73,60,61]

ROW1 = [11,10,9,8,7,6,5,4,3,2,1]
ROW2 = [12,13,14,15,16,17,18,19,20,21,22]
ROW3 = [33,32,31,30,29,28,27,26,25,24,23]
ROW4 = [34,35,36,37,38,39,40,41,42,43,44]
ROW5 = [55,54,53,52,51,50,49,48,47,46,45]
ROW6 = [56,57,58,59,60,61,62,63,64,65,66]
ROW7 = [77,76,75,74,73,72,71,70,69,68,67]
ROW8 = [78,79,80,81,82,83,84,85,86,87,88]
ROW9 = [99,98,97,96,95,94,93,92,91,90,89]
ROW10 = [100,101,102,103,104,105,106,107,108,109,110]
ROW11 = [121,120,119,118,117,116,115,114,113,112,111]
MATRIXROWS = [ROW1, ROW2, ROW3, ROW4, ROW5,ROW6, ROW7, ROW8, ROW9, ROW10, ROW11]

COLUMN1 = [ROW1[0],ROW2[0],ROW3[0],ROW4[0],ROW5[0],ROW6[0],ROW7[0],ROW8[0],ROW9[0],ROW10[0],ROW11[0]]
COLUMN2 = [ROW1[1],ROW2[1],ROW3[1],ROW4[1],ROW5[1],ROW6[1],ROW7[1],ROW8[1],ROW9[1],ROW10[1],ROW11[1]]
COLUMN3 = [ROW1[2],ROW2[2],ROW3[2],ROW4[2],ROW5[2],ROW6[2],ROW7[2],ROW8[2],ROW9[2],ROW10[2],ROW11[2]]
COLUMN4 = [ROW1[3],ROW2[3],ROW3[3],ROW4[3],ROW5[3],ROW6[3],ROW7[3],ROW8[3],ROW9[3],ROW10[3],ROW11[3]]
COLUMN5 = [ROW1[4],ROW2[4],ROW3[4],ROW4[4],ROW5[4],ROW6[4],ROW7[4],ROW8[4],ROW9[4],ROW10[4],ROW11[4]]
COLUMN6 = [ROW1[5],ROW2[5],ROW3[5],ROW4[5],ROW5[5],ROW6[5],ROW7[5],ROW8[5],ROW9[5],ROW10[5],ROW11[5]]
COLUMN7 = [ROW1[6],ROW2[6],ROW3[6],ROW4[6],ROW5[6],ROW6[6],ROW7[6],ROW8[6],ROW9[6],ROW10[6],ROW11[6]]
COLUMN8 = [ROW1[7],ROW2[7],ROW3[7],ROW4[7],ROW5[7],ROW6[7],ROW7[7],ROW8[7],ROW9[7],ROW10[7],ROW11[7]]
COLUMN9 = [ROW1[8],ROW2[8],ROW3[8],ROW4[8],ROW5[8],ROW6[8],ROW7[8],ROW8[8],ROW9[8],ROW10[8],ROW11[8]]
COLUMN10 = [ROW1[9],ROW2[9],ROW3[9],ROW4[9],ROW5[9],ROW6[9],ROW7[9],ROW8[9],ROW9[9],ROW10[9],ROW11[9]]
COLUMN11 = [ROW1[10],ROW2[10],ROW3[10],ROW4[10],ROW5[10],ROW6[10],ROW7[10],ROW8[10],ROW9[10],ROW10[10],ROW11[10]]
MATRIXCOLS = [COLUMN1,COLUMN2,COLUMN3,COLUMN4,COLUMN5,COLUMN6,COLUMN7,COLUMN8,COLUMN9,COLUMN10,COLUMN11]

class ledConfig:
    def __init__(self, name, onOff, color):
        self.name = name
        self.onOff = onOff
        self.colorToSet = wheel(color)
    def blackout():
        self.intensity = 0
        self.onOff = 0
        self.colorToSet = 0

def colorWipe(strip, color, wait_ms):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -=170
        return Color(0,pos * 3 , 255 - pos * 3)

def addToConfig(strandConfig,lights, colorToSet):
    for i in lights:
        strandConfig[i].onOff = 1
        strandConfig[i].colorToSet = colorToSet
    return strandConfig

def addHourToConfig(strandConfig, hour, colorToSet):
    strandConfig = addToConfig(strandConfig, HOURS[hour-1], colorToSet)
    return strandConfig

def addMinuteToConfig(strandConfig, minute, colorToSet):
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

def getPlainColorConfig(strip, lengthNeeded, colorToSet):
    fullConfig = []
    for i in range (0, lengthNeeded+1):
        fullConfig.append(fullConfig(i, 1, colorToSet))
    return fullConfig

def getConfigWithCurrentTime(lengthNeeded, colorToSet):
    strandConfig = getEmptyConfig(lengthNeeded-1)
    hourToSet = datetime.datetime.now().hour
    if(hourToSet > 12):
        hourToSet = hourToSet - 12
    if(hourToSet == 0):
        hourToSet = 12
    minuteToSet = datetime.datetime.now().minute
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

def getConfigWithSetTime(lengthNeeded, colorToSet, hourToSet, minuteToSet):
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

def getEmptyConfig(lengthNeeded):
    emptyConfig = []
    for i in range (0, lengthNeeded+1):
        emptyConfig.append(ledConfig(i,0,BLACK))
    return emptyConfig

def flickerCurrentConfig(strandConfig, strip, times, frequency):
    strip.show()
    for i in range(times):
        setAColorForConfig(strandConfig, strip, Color(0,0,0))
        time.sleep(frequency/1000.0)
        setAColorForConfig(strandConfig, strip, Color(255,255,255))
        time.sleep(frequency/100.00)

def glowCurrentConfig(strandConfig, strip, speed, repeat, colorToSet):
    for r in range(0,repeat):
        for i in range(0,100):
            setBrightness(strip, 255-i)
            setAColorForConfig(strandConfig, strip, colorToSet)
            time.sleep(speed/1000.0)
        for i in range(155,255):
            setBrightness(strip, i)
            setAColorForConfig(strandConfig, strip, colorToSet)
            time.sleep(speed/1000.0)

def setBrightness(strip, brightness):
#    print("set brightness to: ",brightness)
    strip.setBrightness(brightness)

def getConfigToSpreadRainbowOnForeGround(strandConfig):
    countOns = 0
    for pixel in strandConfig:
        if(pixel.onOff == 1):
            countOns = countOns + 1
    colorToSet = round(255/(countOns+1))
    colorToIncrement = round(255/(countOns+1))
#    print("colorToSetIncrement",colorToSet)
    for i in range(len(strandConfig)):
        if(strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = wheel(colorToSet)
            colorToSet = colorToSet + colorToIncrement
    return strandConfig

def runARainbowOnCurrentConfig(strandConfig, strip, times, allOn):
    if allOn == 1:
        for colorNum in range(0,255):
#           running a rainbow on all LEDS
            for i in range(strip.numPixels()+1):
                strip.setPixelColor(i, wheel(colorNum))
                strip.show()
    elif allOn == 2:
        for colorNum in range(0,255):
            for i in range(strip.numPixels()+1):
#           runnign a rainbow on all non-config LEDS
                setAColorForOffConfig(strandConfig,strip,wheel(colorNum))
    else:
        print("running a rainbow on all config LEDS")
        for colorNum in range(0,255):
            reColorConfig(strandConfig,strip,wheel(colorNum))

def setAColorForConfig(strandConfig, strip, colorToSet):
    for i in range(strip.numPixels()+1):
        if (strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = colorToSet
    reflectConfig(strandConfig, strip)
    strip.show()

def reflectConfig(strandConfig, strip):
    for i in range(strip.numPixels()+1):
        strip.setPixelColor(i-1, strandConfig[i].colorToSet)
    strip.show()

def reColorConfig(strandConfig,strip, colorToSet):
#    print("recoloring")
    for i in range(strip.numPixels()+1):
        if (strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = colorToSet
    setAColorForConfig(strandConfig, strip, colorToSet)

def setAColorForOffConfig(strandConfig, strip, colorToSet):
    for i in range(strip.numPixels()+1):
        if (strandConfig[i].onOff == 0):
            strandConfig[i].colorToSet = colorToSet

def setWHITEForConfig(strandConfig, strip):
    for i in range(strip.numPixels()+1):
        if (strandConfig[i].onOff == 1):
            strandConfig[i].colorToSet = WHITE
            strip.setPixelColor(i-1,WHITE)
            strip.show()
        else:
            strandConfig[i].colorToSet = BLACK
            strip.setPixelColor(i-1,BLACK)
            strip.show()

def transitionWithStatic(strip, strandConfig, duration):
    print("-------static------")
    for i in range(duration*500):
        strip.setPixelColor(random.randint(0,(strip.numPixels()+1)), Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        strip.show()

def fadeToBlack(strip, duration):
    for i in range(256):
        strip.setBrightness(255-i)
        strip.show()

def fadeToConfig(strip, strandConfig, duration):
    strip.setBrightness(0)
    for i in range(strip.numPixels()+1):
        strip.setPixelColor(i-1, strandConfig[i].colorToSet)
    for i in range(256):
        strip.setBrightness(i)
        strip.show()

def runTheMatrix(strip, strandConfig):
#TO OPTIMIZE
    colorToSet = GREEN
    setAColorForConfig(strandConfig, strip, colorToSet)
    newConfig = strandConfig
    #replace by a "while anything is on"
    for repeats in range(50):
        print("repeat: ",repeats)
        time.sleep(1)
        # for each pixel on, switch on the one under it.
        for colNr in range(0,len(MATRIXCOLS)):
            print("working on col: ", colNr)
            COLUMN = MATRIXCOLS[colNr]
            for i in range(0,len(COLUMN)):
                print("working on row: ", i)
                ledNumber = COLUMN[i]
                if(strandConfig[ledNumber].onOff == 1 and strandConfig[ledNumber].colorToSet == colorToSet and i < len(COLUMN)-1):
                    print("dropping a letter: column ", colNr, " -- led ", ledNumber, "to ", COLUMN[i+1])
                    droppedLednumber = COLUMN[i+1]
                    newConfig[droppedLednumber].onOff = 1
                    newConfig[droppedLednumber].colorToSet = colorToSet
        strandConfig = newConfig
        reflectConfig(strandConfig,strip)
#        print("Starting To Fade")
#        for i in range(0,10):
#             print("fading")
#             strandConfig = fadeTen(strandConfig)
#             reflectConfig(strandConfig,strip)
#             time.sleep(1)

def fadeTen(strandConfig):
    for i in range(strip.numPixels()+1):
        if (strandConfig[i].onOff == 1):
             lngRGB = strip.getPixelColor(i)
             u8R = (lngRGB >> 16) & 0x7f
             u8G = (lngRGB >> 8) & 0x7f
             u8B = (lngRGB) & 0x7f
#             print("LED: ", i, "RED: ", u8R, "GREEN: ", u8G, "BLUE: ", u8B)
             if(u8R >= 10): u8R = u8R-10
             if(u8G >= 10): u8R = u8G-10
             if(u8B >= 10): u8R = u8B-10
             adjustedColor = Color(u8R,u8G,u8B)
             strandConfig[i].colorToSet = adjustedColor
    return strandConfig

def animationCoffee(strip, speed):
    COFFEECUP = [54,53,52,51,50,49,48,57,76,79,98,101,63,85,92,107,119,118,117,116,115,64,65,67,88,90,91]
    COFFEESMOKE1 = [11,13,31,8,16,28]
    COFFEESMOKE2 = [10,14,30,7,17,27]
    COFFEESMOKE3 = [9,15,29,6,18,26]

    for i in range (0,4):
        for lednumber in range(strip.numPixels()):
            strip.setPixelColor(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            strip.setPixelColor(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE1:
            strip.setPixelColor(lednumber-1, WHITE)
        strip.show()
        time.sleep(speed/10)
        for lednumber in range(strip.numPixels()):
             strip.setPixelColor(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            strip.setPixelColor(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE2:
            strip.setPixelColor(lednumber-1, WHITE)
        strip.show()
        time.sleep(speed/10)
        for lednumber in range(strip.numPixels()):
            strip.setPixelColor(lednumber-1, BLACK)
        for lednumber in COFFEECUP:
            strip.setPixelColor(lednumber-1, WHITE)
        for lednumber in COFFEESMOKE3:
            strip.setPixelColor(lednumber-1, WHITE)
        strip.show()
        time.sleep(speed/10)

def animationStatic(strip, duration):
    minimal = 0
    for i in range(0,255*duration):
        strip.setPixelColor(random.randint(0,LED_COUNT), wheel(random.randint(minimal,255)))
        strip.show()

def animationHeart(strip, duration):
    HEART = [14,15,19,20,32,29,27,24,34,39,44,45,55,57,75,81,95,105,93,85,69,65]
    FILL = [31,30,26,25,35,36,37,38,40,41,42,43,54,53,52,51,50,49,48,47,46,58,59,60,61,62,63,64,74,73,72,71,70,82,83,84,94]
    for lednumber in range(strip.numPixels()):
        strip.setPixelColor(lednumber-1, BLACK)
    print("showing heart")
    for lednumber in HEART:
        strip.setPixelColor(lednumber-1, RED)
    strip.show()
    for i in range(0,5):
        for lednumber in FILL:
            strip.setPixelColor(lednumber-1,RED)
        strip.show()
        time.sleep(0.2)
        for lednumber in FILL:
            strip.setPixelColor(lednumber-1,DARKRED)
        strip.show()
        time.sleep(0.2)
    time.sleep(duration)

def animationRunDown(strip, colorToSet):
    for rownumber in range(0,len(MATRIXROWS)+1):
        for i in range(0,len(ROW1)):
            if(rownumber < len(MATRIXROWS)):
                ROW = MATRIXROWS[rownumber]
                strip.setPixelColor(ROW[i]-1, colorToSet)
            if(rownumber > 0):
                PREVROW = MATRIXROWS[rownumber-1]
                strip.setPixelColor(PREVROW[i]-1,BLACK)
            strip.show()

def compareOnOff(strandConfig, newConfig):
    countDifferences = 0
    for led in strandConfig:
        if(led.onOff != newConfig[led.name].onOff):
            countDifferences = countDifferences + 1
    return countDifferences

def runSnake(strip, colorToSet, speed):
    print("--------SNAKE------")
    for i in range(strip.numPixels()):
        strip.setPixelColor(SEQUENCESPIRAL[i]-1, colorToSet)
        strip.show()
        time.sleep(speed/1000.0)

def animateSimpleList(strip, LIST, colorToSet):
    for lednumber in LIST:
        strip.setPixelColor(lednumber-1, colorToSet)
        strip.show()

def showSimpleList(strip, LIST, colorToSet):
    for lednumber in range(strip.numPixels()):
        strip.setPixelColor(lednumber-1, BLACK)
    for lednumber in LIST:
        strip.setPixelColor(lednumber-1, colorToSet)
    strip.show()


def showClock(strip, colorToSet):
    CIRCLE = [8,7,6,5,4,20,24,44,45,66,67,88,90,108,114,115,116,117,118,102,98,78,77,56,55,34,32,14]
    HANDS = [28,39,50,61,71,85]

    for lednumber in range(strip.numPixels()):
        strip.setPixelColor(lednumber-1, BLACK)
    strip.show()
    for lednumber in CIRCLE:
        strip.setPixelColor(lednumber-1, colorToSet)
        strip.show()
        time.sleep(20/1000.0)
    for lednumber in HANDS:
        strip.setPixelColor(lednumber-1, colorToSet)
    strip.show()

def getConfigForAnalogCurrentTime(strip, CIRCLECOLOR, BIGHANDCOLOR, SMALLHANDCOLOR):
    CIRCLE = [8,7,6,5,4,20,24,44,45,66,67,88,90,108,114,115,116,117,118,102,98,78,77,56,55,34,32,14]
    currentConfig = []
    currentConfig = getEmptyConfig(strip.numPixels())
    hourToSet = datetime.datetime.now().hour
    if(hourToSet >= 12):
        hourToSet = hourToSet - 12
    minuteToSet = datetime.datetime.now().minute
    if(debugmode > 2):
        print("hourToSet: ", hourToSet)
        print("minuteToSet: ", minuteToSet)
    if (minuteToSet >= 20):
        if(hourToSet == 12):
            hourToSet = 1
        else:
            hourToSet = hourToSet + 1
    for lednumber in range(strip.numPixels()):
        strip.setPixelColor(lednumber-1, BLACK)
    for lednumber in CIRCLE:
        currentConfig[lednumber].onOff = 1
        currentConfig[lednumber].colorToSet = CIRCLECOLOR
    currentConfig[61].onOff = 1
    currentConfig[61].colorToSet = CIRCLECOLOR
    #SET LARGE HAND
    listToLightLarge = getHand("large", minuteToSet)
    for setting in listToLightLarge:
        currentConfig[setting].onOff = 1
        currentConfig[setting].colorToSet = BIGHANDCOLOR
    #SET SMALL HAND
    if(minuteToSet<=30):listToLightSmall = getHand("small", (hourToSet * 5))
    else:listToLightSmall = getHand("small", (hourToSet * 5) + 3)
    for setting in listToLightSmall:
        currentConfig[setting].onOff = 1
        currentConfig[setting].colorToSet = SMALLHANDCOLOR
    return currentConfig


def showMoon(strip, duration):
     MOON = [6,5,4,20,24,43,45,66,67,87,90,108,107,115,116,117,103,102,98,78,77,56,76,75,81,82,72,62,48,41,27,18]
     MOONFILL = [19,25,26,42,47,46,63,64,65,71,70,69,68,79,80,97,96,83,84,85,86,95,104,94,105,93,106,92,91]
     showSimpleList(strip, MOON, WHITE)
     showSimpleList(strip, MOONFILL, YELLOW)
     time.sleep(duration)

def showSmiley(strip, duration):
    BLACKCIRCLE = [8,7,6,5,4,14,20,32,24,34,55,56,77,78,44,45,66,67,88,98,90,102,108,118,117,116,115,114]
    EYES = [37,52,41,48]
    MOUTH = [74,70,82,83,84]
    YELLOW = [15,16,17,18,19,31,30,29,28,27,26,25,35,36,38,39,40,42,43,54,53,51,50,49,47,46,57,58,59,60,61,62,63,64,65,76,75,73,72,71,69,68,79,80,81,85,86,87,97,96,95,94,93,92,91,103,104,105,106,107]

    for lednumber in range(strip.numPixels()):
        strip.setPixelColor(lednumber-1, WHITE)
    print("showing smiley")
    for lednumber in BLACKCIRCLE:
        strip.setPixelColor(lednumber-1, YELLOW)
    for lednumber in EYES:
        strip.setPixelColor(lednumber-1, BLACK)
    for lednumber in MOUTH:
        strip.setPixelColor(lednumber-1, BLACK)
    for lednumber in YELLOW:
        strip.setPixelColor(lednumber-1, YELLOW)
    strip.show()
    time.sleep(duration)
    print("showing smiley -- DONE")

def drawLetterAtPos(strip, row, col, LETTERROWS, LETTERCOLS, color):
    for led in range(0,len(LETTERROWS)):
        lightmatrixCell(strip, row + LETTERROWS[led], col + LETTERCOLS[led], color)
    strip.show()

def lightmatrixCell(strip, row, col, color):
    if row >= 0 and col >= 0 and row < len(MATRIXROWS):
        rowToLight = MATRIXROWS[row]
        if col < len(rowToLight):
            lednumber = rowToLight[col]
            strip.setPixelColor(lednumber-1, color)

def flushColor(strip, color):
    for lednr in range(0,strip.numPixels()):
        strip.setPixelColor(lednr, color)
    strip.show()

def showXMASTREE(strip):
    TREE = [6,16,17,18,30,29,28,27,26,38,39,40,52,51,50,49,48,58,59,60,61,62,63,64,74,73,72,71,70,80,81,82,83,84,85,86,98,97,96,95,94,93,92,91,90]
    STAM = [105,116]
    BALLS = [16,52,62,27,85,82,97]
    BALLCOLORS = [PINK, RED, BLUE, YELLOW, PINK, WHITE, ORANGE]

    for lednumber in range(strip.numPixels()+1):
        strip.setPixelColor(lednumber-1, BLACK)
    for lednr in TREE:
        strip.setPixelColor(lednr-1,DARKGREEN)
    for lednr in STAM:
        strip.setPixelColor(lednr-1, RED)
    strip.show()
    for counter in range(0,20):
        placeToLight = random.randint(0,len(TREE)-1)
        strip.setPixelColor(TREE[placeToLight]-1,BALLCOLORS[random.randint(0,len(BALLCOLORS)-1)])
        strip.show()
        time.sleep(0.5)
        for lednr in TREE:
            strip.setPixelColor(lednr-1,DARKGREEN)
        strip.show()
        time.sleep(random.randint(20,100)/100)

def getHand(size, minute):
    listToLight = []
    print("lighting minute:", minute, " for ",size," hand")
    if(minute < 1):
        if(size == "large"):listToLight = [50,39,28,17]
        else:listToLight = [50,39,28]
    if(minute < 2):
        if(size == "large"):listToLight = [50,39,28,18]
        else:listToLight = [50,39,28]
    if(minute < 3):
        if(size == "large"):listToLight = [50,39,27,18]
        else:listToLight = [50,39,28]
    if(minute < 4):
        if(size == "large"):listToLight = [50,40,27,18]
        else:listToLight = [50,40,27]
    elif(minute <6):
        if(size == "large"):listToLight = [50,40,27,19]
        else:listToLight = [50,40,27]
    elif(minute <7):
        if(size == "large"):listToLight = [50,40,26,19]
        else:listToLight = [50,40,27]
    elif(minute <8):
        if(size == "large"):listToLight = [49,41,26]
        else:listToLight = [49,41,26]
    elif(minute <9):
        if(size == "large"):listToLight = [49,41,25]
        else:listToLight = [49,41]
    elif(minute <10):
        if(size == "large"):listToLight = [49,41,42]
        else:listToLight = [49,41]
    elif(minute <11):
        if(size == "large"):listToLight = [62,48,47,43]
        else:listToLight = [62,48,47]
    elif(minute <12):
        if(size == "large"):listToLight = [62,48,47,46]
        else:listToLight = [62,48,47]
    elif(minute < 14):
        if(size == "large"):listToLight = [62,63,47,46]
        else:listToLight = [62,63,47]
    elif(minute < 15):
        if(size == "large"):listToLight = [62,63,64,46]
        else:listToLight = [62,63,64]
    elif(minute < 16):
        if(size == "large"):listToLight = [62,63,64,65]
        else:listToLight = [62,63,64]
    elif(minute < 17):
        if(size == "large"):listToLight = [62,63,64,68]
        else:listToLight = [62,63,64]
    elif(minute < 18):
        if(size == "large"):listToLight = [62,63,69,68]
        else:listToLight = [62,63,69]
    elif(minute < 19):
        if(size == "large"):listToLight = [62,70,69,68]
        else:listToLight = [62,70,69]
    elif(minute < 21):
        if(size == "large"):listToLight = [62,70,69,87]
        else:listToLight = [62,70,69]
    elif(minute < 22):
        if(size == "large"):listToLight = [71,70,86,87]
        else:listToLight = [71,70,86]
    elif(minute < 23):
        if(size == "large"):listToLight = [71,85,86]
        else:listToLight = [71,85]
    elif(minute < 24):
        if(size == "large"):listToLight = [71,85,91]
        else:listToLight = [71,85]
    elif(minute < 25):
        if(size == "large"):listToLight = [71,84,92]
        else:listToLight = [71,84]
    elif(minute < 26):
        if(size == "large"):listToLight = [72,84,93,107]
        else:listToLight = [72,84,93]
    elif(minute < 27):
        if(size == "large"):listToLight = [72,84,93,106]
        else:listToLight = [72,84,93]
    elif(minute < 28):
        if(size == "large"):listToLight = [72,84,93,106]
        else:listToLight = [72,84,93]
    elif(minute < 30):
        if(size == "large"):listToLight = [72,83,94,106]
        else:listToLight = [72,83,94]
    elif(minute < 31):
        if(size == "large"):listToLight = [72,83,94,105]
        else:listToLight = [72,83,94]
    elif(minute < 32):
        if(size == "large"):listToLight = [72,83,94,104]
        else:listToLight = [72,83,94]
    elif(minute < 33):
        if(size == "large"):listToLight = [72,83,95,104]
        else:listToLight = [72,83,95]
    elif(minute < 33):
        if(size == "large"):listToLight = [72,84,92]
        else:listToLight = [72,84]
    elif(minute < 35):
        if(size == "large"):listToLight = [72,82,95,103]
        else:listToLight = [72,82,95]
    elif(minute < 36):
        if(size == "large"):listToLight = [72,82,96,103]
        else:listToLight = [72,82,96]
    elif(minute < 37):
        if(size == "large"):listToLight = [72,82,96]
        else:listToLight = [72,82]
    elif(minute < 38):
        if(size == "large"):listToLight = [72,82,96,97]
        else:listToLight = [72,82,96]
    elif(minute < 39):
        if(size == "large"):listToLight = [73,81,97]
        else:listToLight = [72,81]
    elif(minute < 40):
        if(size == "large"):listToLight = [60,74,80]
        else:listToLight = [60,74]
    elif(minute < 41):
        if(size == "large"):listToLight = [60,74,75,79]
        else:listToLight = [60,74,75]
    elif(minute < 42):
        if(size == "large"):listToLight = [60,74,75,76]
        else:listToLight = [60,74,75]
    elif(minute < 43):
        if(size == "large"):listToLight = [60,59,75,76]
        else:listToLight = [60,59,75]
    elif(minute < 44):
        if(size == "large"):listToLight = [60,59,58,76]
        else:listToLight = [60,59,58]
    elif(minute < 45):
        if(size == "large"):listToLight = [60,59,75,76]
        else:listToLight = [60,59,75]
    elif(minute < 46):
        if(size == "large"):listToLight = [60,59,58,57]
        else:listToLight = [60,59,58]
    elif(minute < 47):
        if(size == "large"):listToLight = [60,59,58,54]
        else:listToLight = [60,59,58]
    elif(minute < 48):
        if(size == "large"):listToLight = [60,52,53,54]
        else:listToLight = [60,52,53]
    elif(minute < 48):
        if(size == "large"):listToLight = [60,52,53,54]
        else:listToLight = [60,52,53]
    elif(minute < 51):
        if(size == "large"):listToLight = [60,52,53,35]
        else:listToLight = [60,52,53]
    elif(minute < 52):
        if(size == "large"):listToLight = [60,52,36,35]
        else:listToLight = [60,52,36]
    elif(minute < 53):
        if(size == "large"):listToLight = [51,37,31]
        else:listToLight = [51,37]
    elif(minute < 55):
        if(size == "large"):listToLight = [51,38,30,15]
        else:listToLight = [51,38,30]
    elif(minute < 56):
        if(size == "large"):listToLight = [50,38,29,15]
        else:listToLight = [50,38,29]
    elif(minute < 57):
        if(size == "large"):listToLight = [50,38,29,16]
        else:listToLight = [50,38,29]
    elif(minute < 58):
        if(size == "large"):listToLight = [50,39,29,16]
        else:listToLight = [50,38,29]
    else:
        if(size == "large"):listToLight = [50,39,28,16]
        else:listToLight = [50,39,28]
    return listToLight

if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    if(debugmode > 1):
        for led in strandConfig:
            print(led.name, led.onOff, led.color)

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    strandConfig = []
    newConfig = []
    strandConfig = getEmptyConfig(LED_COUNT)
    colorToSet = WHITE
    strip.show()

    DEMO = 0
    #------DEMO-------
    if(DEMO == 1):
        hourToSet = 11
        minuteToSet = 50
    #------DEMO-------

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
#            showSmiley(strip, 5)
    #------DEMO-------
            if(DEMO == 1):
                minuteToSet = minuteToSet + 5
                if(minuteToSet == 60):
                    minuteToSet = 0
                    hourToSet = hourToSet + 1
                    if(hourToSet == 24):
                        hourToSet = 0
                print("timeToSet = ", hourToSet, ":", minuteToSet)
                print("setting time: ",hourToSet,":",minuteToSet)
            else:
                hourToSet = datetime.datetime.now().hour
                minuteToSet = datetime.datetime.now().minute
    #------DEMO-------

            if(DEMO == 1):
                newConfig = getConfigWithSetTime(len(strandConfig), colorToSet, hourToSet, minuteToSet)
            else:
                newConfig = getConfigWithCurrentTime(len(strandConfig), colorToSet)
            if(compareOnOff(strandConfig, newConfig) > 0):
#                transitionWithStatic(strip, strandConfig, 1)
                strandConfig = newConfig
# show Xmas tree for 5 secs
#                showXMASTREE(strip)

# show ZZZ if after 7PM
                if(hourToSet > 16 and hourToSet < 18):
                    animationCoffee(strip, 5)
                if(hourToSet < 10 or hourToSet > 19):
                    row1 = random.randint(1,8)
                    row2 = random.randint(1,8)
                    row3 = random.randint(1,8)
                    row4 = random.randint(1,8)
                    for pos in range(-20, 12):
                        flushColor(strip, BLACK)
                        LETTERZROWS = [1,1,1,1,2,3,4,5,5,5,5]
                        LETTERZCOLS = [1,2,3,4,3,2,1,1,2,3,4]
                        drawLetterAtPos(strip, row1, pos, LETTERZROWS, LETTERZCOLS, WHITE)
                        drawLetterAtPos(strip, row2, pos + 5, LETTERZROWS, LETTERZCOLS, WHITE)
                        drawLetterAtPos(strip, row3, pos + 10, LETTERZROWS, LETTERZCOLS, WHITE)
                        drawLetterAtPos(strip, row4, pos + 15, LETTERZROWS, LETTERZCOLS, WHITE)
                        time.sleep(0.1)
# on the full hour, run a snake
                COLORLIST = [RED, GREEN, BLUE, ROSE , BROWN, WHITE, RED, GREEN, BLUE, ROSE, BROWN, BEIGE, RED, GREEN, BLUE, ROSE , BROWN, WHITE, RED, GREEN, BLUE, ROSE, BROWN, BEIGE, RED, GREEN, BLUE, ROSE , BROWN, WHITE, RED, GREEN, BLUE, ROSE, BROWN, BEIGE, WHITE]
                if(minuteToSet == 0):
                    runSnake(strip, COLORLIST[hourToSet], 5)
                    colorToSet = COLORLIST[hourToSet]
                elif(minuteToSet != 0):
#                     animationHeart(strip, 3)
#                     animationRunDown(strip, RED)
#                     showSmiley(strip, 2)
#                     animationStatic(strip, 3)
                     colorToSet = COLORLIST[hourToSet]
                else:
                    colorToSet = WHITE

                fadeToBlack(strip, 5)
# Show analog clock
#                analogConfig = getConfigForAnalogCurrentTime(strip, WHITE, BLUE, RED)
#                setAColorForOffConfig(analogConfig, strip,BLACK)
#                fadeToConfig(strip, analogConfig, 5)
#                time.sleep(0.25)

                fadeToBlack(strip, 5)
                setAColorForOffConfig(strandConfig, strip,BLACK)
                setAColorForConfig(strandConfig, strip, colorToSet)
                fadeToConfig(strip, strandConfig, 5)
            if (DEMO != 1):
                if(hourToSet < 10):
#                    print("DIMMED")
                    strip.setBrightness(1)
                    strip.show()
                else:
#                    print("BRIGHT")
                    strip.setBrightness(255)
                    strip.show()
#            reflectConfig(strandConfig, strip)
#            setWHITEForConfig(strandConfig, strip)
            if(DEMO != 1):
                if(debugmode > 1):
                    for led in strandConfig:
                        print (led.name, led.onOff, led.color)
#            flickerCurrentConfig(strandConfig, strip, 5, 100)
#            if(minuteToSet == 15 or minuteToSet == 30 or minuteToSet == 45 or minuteToSet == 60):
#            glowCurrentConfig(strandConfig, strip, 5 ,5, BROWN)

#            runTheMatrix(strip, strandConfig)



#            animationRunDownToConfig(strip, strandConfig, RED)
            if(DEMO == 1):
                time.sleep(1)
            else:
                time.sleep(5)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, BLACK, 10)
