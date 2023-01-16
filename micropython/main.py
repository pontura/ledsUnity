import array, time
import math
import random
import character, explotion, leds, led, inputs, curves

NUM_PARTICLES = 16
NUM_LEDS = 300         
N = 200_000

def Init():
    global character1
    global character2
    global NUM_LEDS
    global curves
    
    
    framerate = 2.45
    acceleration = 0.02
    
    curves = curves.Curves()
    
    character1 = character.Character()
    character1.Init(1, framerate, acceleration)
    
    character2 = character.Character()
    character2.Init(2, framerate, acceleration)
    
    for i in range(NUM_LEDS):
        thisLed = led.Led(i)
        thisLed.Init(i)
        leds.all.append(thisLed)
    curves.Init(leds)
    

        
def Loop():
    while True:
        t0 = time.ticks_us()
        dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
        
        #Background(dimmer_ar)
        LoopGame(dimmer_ar)
        
        t1 = time.ticks_us()
        dt = time.ticks_diff(t1,t0)
        fmt = "{:8.2f} kblinks/sec"
        
        leds.SetLeds(dimmer_ar,8)
        print(fmt.format(N/dt * 1e3))
        
def Background(dimmer_ar):
    ledsSetColor = leds.setColor
    for i in range(NUM_LEDS):
        c = ledsSetColor((1,1,1))
        r = int(((c >> 8) & 0xFF) )
        g = int(((c >> 16) & 0xFF))
        b = int((c & 0xFF) )
        dimmer_ar[i] = (g<<16) + (r<<8) + b
        
def LoopGame(dimmer_ar):     
    inputs.UpdatePot()
    character1.Move(inputs.pot1_value, NUM_LEDS)
    character2.Move(inputs.pot2_value, NUM_LEDS)      
    curves.SetCurves(dimmer_ar, leds)        
    explotionParticlesLength = len(explotion.explotionParticles)
    if explotionParticlesLength > 0:
        UpdateCollisions(dimmer_ar, explotionParticlesLength)   
    if character1.state == 1 or character1.state == 3:
        playCharacter(1, dimmer_ar)        
    if character2.state == 1 or character2.state == 3:
        playCharacter(2, dimmer_ar)
    #time.sleep(0.01)
    
    
def UpdateCollisions(dimmer_ar, i):
    global characterID
    while i > 0:
        particle = explotion.explotionParticles[i-1]
        characterID = particle.characterID
        particle.Update(NUM_LEDS)
        leds.SetPixel(dimmer_ar, particle.color, particle.ledID)
        if particle.speed<=0.01:                
            explotion.explotionParticles.remove(particle)
            del particle;
        i = i-1
            
            
    
def playCharacter(characterID, dimmer_ar):
    character = character1
    if characterID == 1:
        character = character1
        speed = character1.speed 
        id = math.floor(character1.pos)
        decimals = character1.pos% 1
    else:
        character = character2
        speed = character2.speed 
        id = math.floor(character2.pos)
        decimals = character2.pos% 1
        
    if id>=NUM_LEDS:
        id = 0
        
    ledsToCalculate = (speed * 8) + 2
    for i in range(ledsToCalculate):
        
        realID = int(id-i)
        
        if realID<0:
            realID = NUM_LEDS+realID
            
        led = leds.all[realID]
        curveValue = led.curveValue
        if curveValue >0 and (1-curveValue) < speed:
            character.InDangerZone()    
        elif character.GetState() == 3:
            character.InDangerZoneReset()
        maxColorValue = 50
        if i == 0:
            led.ChangeValues((maxColorValue*decimals))
        elif i == 1 :
            if speed < 0.12:
                led.ChangeValues(maxColorValue*(1-decimals))
            else:
                led.ChangeValues(maxColorValue)            
        else:
            led.Reset()
        
        if led.value >0:
            colorVar = int(led.value)
            if character.GetState() == 3:
                leds.SetPixel(dimmer_ar,(255, 255, 255), realID)
            elif characterID == 1:   
                leds.SetPixel(dimmer_ar,(0,0,colorVar), realID)
            else:
                leds.SetPixel(dimmer_ar,(0,colorVar,0), realID)         
        
        
def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

Init()
Loop()