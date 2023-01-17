import json
import LevelsManager, character
import time
import FPS
#import InputsManager

numLeds = 300         
N = 200_000
framerate = 30
characters = []
ledsData = []
deltaTime = 0
fps = FPS.fps()

def Init():
    LevelsManager.Init(numLeds, framerate)
    character1 = character.Character()
    character2 = character.Character()
    character1.Init(numLeds, 0, (0,255,0), 2)
    character2.Init(numLeds, 0, (0,0,255), 2)
    characters.append(character1)
    characters.append(character2)
    #explotionsManager = new ExplotionsManager()
    for a in range(numLeds): 
        ledsData.append((0,0,0))
        
def Update():    
    while True:
        SetData()
        LevelsManager.OnUpdate(deltaTime)
        sp1 = 0.1 #inputs.character1_speed
        sp2 = -0.1 #inputs.character2_speed
        characters[0].OnUpdate(sp1, deltaTime)
        characters[1].OnUpdate(sp2, deltaTime)        
        deltatime = fps.Update()
        #time.sleep(0.1)
        
      
boolValue = False
def SetData():
    global boolValue
    if boolValue == False:
        boolValue = True
    else:
        boolValue = False
        
    ledsData = []
    for a in range(numLeds): 
        ledsData.append((0,0,0))
               
    levelZones = LevelsManager.GetLevelZones()
    
    for a in range(len(levelZones)):
        levelzone = levelZones[a]    
        ledID = levelzone.vfrom
        color = levelzone.GetColor()
        vto = levelzone.vto
        vfrom = levelzone.vfrom
        status = levelzone.status
        
        if (vto>vfrom):        
            ColorizeZone(vfrom, vto, color, status)
        
        elif (vto != vfrom):
        
            ColorizeZone(vfrom, numLeds, color, status)
            ColorizeZone(0, vto, color, status)        
        
    for a in range(len(characters)):
        character = characters[a]
        ledsData[character.ledId] = character.color
        c = character.color
        
#         foreach (Particle particle in character.trail.all)
#         
#             if (particle.value > 0 && particle.ledID != character.ledId)
#             
#                 c.a = particle.value / 255
#                 ledsData[particle.ledID] = c
            
         
    
#     foreach (Explotion explotion in explotionsManager.GetExplotions())
#     
#         if (explotion.on)
#         
#             Color c = explotion.color
#             explotion.OnUpdate(deltaTime)
#             foreach (Particle particle in explotion.all)
#             
#                 c.a = particle.value / 255
#                 ledsData[particle.ledID] = c
            
        
    

            
Init()
Update()
