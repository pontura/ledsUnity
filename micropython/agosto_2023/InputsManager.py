from machine import ADC, Pin
import time

button1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(13, Pin.IN, Pin.PULL_DOWN)
lt1 = 0
b1 = False
lt2 = 0
b2 = False
delay = 250
def AA():
    global b1
    global lt1
    if button1.value():
        lt1 = lt1+1
        print("::::::::::::::", lt1)
    else:        
        if b1 == True:
            b1 = False
    return False

def GetClick_1():
    global b1
    global lt1
    if button1.value():
        
        print("::::::::::::::")
        if b1 == False:
            if lt1+delay<time.ticks_ms():
                lt1 = time.ticks_ms()
                b1 = True
                return True
    else:
        
        print("_")
        if b1 == True:
            b1 = False
    return False
            
        
def GetClick_2():
    global b2
    global lt2
            
    if button2.value():
        if b2 == False:
            if lt2+delay<time.ticks_ms():
                lt2 = time.ticks_ms()
                return True
    else:
        if b2 == True:
            b2 = False
    return False
            
    
