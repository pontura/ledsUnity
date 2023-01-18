import LevelsManager, character
import time
import FPS
import Udp
#import InputsManager

numLeds = 300         
N = 200_000
framerate = 30
characters = []
ledsData = []

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
    deltaTime = 0.01
    while True:
        SetData()
        LevelsManager.OnUpdate(deltaTime)
        sp1 = 1 #inputs.character1_speed
        sp2 = -1 #inputs.character2_speed
        characters[0].OnUpdate(sp1, deltaTime)
        characters[1].OnUpdate(sp2, deltaTime)        
        deltatime = fps.Update()
        #print(ledsData)
        Udp.Send(ledsData)
        time.sleep(0.015)
        
      
boolValue = False
def SetData():
    levelZones = LevelsManager.GetLevelZones()
    global boolValue
    global ledsData
    if boolValue == False:
        boolValue = True
    else:
        boolValue = False
        
    ledsData = []
    for a in range(numLeds): 
        ledsData.append((0,0,0))               
        t = len(levelZones)
        for a in range(t):
            levelzone = levelZones[a]    
            ledID = levelzone.vfrom
            color = levelzone.GetColor()
            #print(levelzone.vfrom, " ", levelzone.vto)
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
            
def ColorizeZone(vfrom, vto, color, status):
    #print(" from ", vfrom, "    to: ", vto, "   color ", color, " status: ", status)
    
    for ledID in range(vto-vfrom):
        ledID = ledID +vfrom
        if ledID > len(ledsData)-1:
            return
        elif ledID < 0:
            return
        if status == "safe":
            isPair = (ledID % 2 == 0)
            a = 0
            if boolValue == isPair:
                a = 0.1
            else:
                a = 0.05
            color = (color[0]*a, color[1]*a, color[2]*a)
        ledsData[ledID] = color;
            
Init()
Update()
