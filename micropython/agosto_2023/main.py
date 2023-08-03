import character
import time
import FPS
import InputsManager, leds, settings, zones

characters = []
ledsData = []

fps = FPS.fps()
leds = leds.Leds()
z = zones.Zones()

def Init():
    leds.Init()
    character1 = character.Character()
#     character2 = character.Character()
    z.Init(0, leds)
    character1.Init(settings.numLeds, 0, 2, 2, leds, z)
#     character2.Init(settings.numLeds, int(settings.numLeds/2), 3, 2, leds, z)
    characters.append(character1)
#     characters.append(character2)
    z.Add(0, 10)
    z.Add(75, 10)    
    z.Add(145, 10)
    z.Add(225, 10)
        
def Update():
    deltaTime = 0.005
    while True:
#         leds.Update()
#         z.Update(deltaTime)
        InputsManager.AA()
#         characters[0].OnUpdate(InputsManager.GetClick_1(), deltaTime)
#         characters[1].OnUpdate(InputsManager.GetClick_2(), deltaTime)   
#        deltatime = fps.Update()
            
Init()
Update()

