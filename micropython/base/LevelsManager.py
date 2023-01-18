import levelZone
import json
        
d ='''{
  "areas":
  [
      {
        "length": "0",
        "zones":
        [
            {
              "color": "",
              "pos": ""
            }
        ],
        "levels":
        [
            {
              "nextLength": 0,
              "speed": 0,
              "seconds": 0,
              "ease": 0
            }
        ]
      }
  ]
}'''

levels = [object]
allZones = [object]

framerate = 0
levelID = 0
areaID = 0
numLeds = 0
lastLength = 150
lastStatus = ""

class LevelData:
    status = ""#; //"safe": zona libre con transparencia // "status": "full" hace daño
    speed = 0.0
    initialLength = 0
    nextLength = 0
    seconds = 0
    ease = ""

with open('data.json') as s:
    d = json.load(s)
    #print(d)
    

def Init(_numLeds, _frameRate):
    global numLeds
    frameRate = _frameRate
    allZones = []
    numLeds = _numLeds
    AddNewArea(frameRate, numLeds)

def AddLevel(_nextLength, speed, seconds, status, ease):
    global lastLength
    global lastStatus
    global numLeds
    global levels
    
    nextLength = _nextLength * (numLeds / 100) # numLeds/100 normaliza de 0 a 100 el scalesss
    print("level nextLength", _nextLength, " speed: ", speed, " seconds:", seconds, " status", status, " ease:", ease, " numLeds: ", numLeds)
    lData = LevelData
    lData.speed = speed
    lData.initialLength = lastLength
    lData.nextLength = nextLength
    lData.seconds = seconds
    lData.status = status
    lData.ease = ease

    if status == "":
        lData.status = lastStatus
    else:
        lData.status = status

    lData.nextLength = nextLength
    lData.seconds = seconds
    levels = []
    levels.append(lData)
    
    lastStatus = status
    lastLength = nextLength


def AddNewArea(framerate, numLeds):
    global allZones
    global areaID
    global thisLevelZone
    global levels
    
    areaData = d["areas"][areaID]
    length = areaData["length"] * (numLeds / 100)#//numLeds/100 normaliza de 0 a 100 el scalesss
    lastLength = length
    zones = areaData["zones"]
    
    
    allZones = [object]
    
    zN = len(zones)
    
    _id = 0
    for a in range(zN):               
        thisLevelZone = levelZone.LevelZone()
        zonesData = zones[a]
        
        if len(zonesData)>0:
            color = GetColor(zonesData["color"])
            pos = zonesData["pos"]*numLeds
        else:
            color = (0,0,0)
            pos = 0
           
        thisLevelZone.Init(_id, pos, length, color, numLeds, framerate)
        allZones.append(thisLevelZone)
        _id = _id+1
        
    levels = [object]
    l = areaData["levels"]
    lN = len(l)
    print("Add area id:", areaID, " zones: ", zN, " levels:", lN, " numLeds:", numLeds)
      
    for a in range(lN):        
        lData = l[a]
        speed = 0
        status = ""
        nextLength = 0
        seconds = ""
        ease = ""
        
        if lData.get("status"):
            status = lData["status"]
        if lData.get("speed"):
            speed = lData["speed"]
        if lData.get("nextLength"):
            nextLength = lData["nextLength"]
        if lData.get("seconds"):
            seconds = lData["seconds"]
        if lData.get("ease"):
            ease = lData["ease"]
            
        AddLevel(nextLength, speed, seconds, status, ease)    
    
    areaID = areaID+1
    if areaID > len(d["areas"])-1:
        areaID = 0

def GetColor(colorName):
    if colorName == "red":
        return (255,0,0)
    elif colorName == "green":
        return (0,255,0)
    elif colorName == "blue":
        return (0,0,255)
    else:
        return (0,0,0)

def OnUpdate(deltaTime):
    total = len(allZones)
    for a in range(total):
        if a < len(allZones):
            level = allZones[a]
            UpdateLevel(level, deltaTime)

def UpdateLevel(level, deltaTime):
    activeLevelData = levels[levelID]
    #print("initialLength: ", activeLevelData.initialLength,  " nextLength", activeLevelData.nextLength,  " seconds", activeLevelData.seconds  )
       
       
    if activeLevelData.nextLength != activeLevelData.initialLength:
        level.ScaleTo(activeLevelData.nextLength, activeLevelData.seconds, activeLevelData.ease, deltaTime)
    if activeLevelData.speed != 0:
        level.Move(activeLevelData.speed, activeLevelData.seconds, activeLevelData.ease, deltaTime)

    level.Process(activeLevelData.seconds, activeLevelData.status, deltaTime)

def OnNextLevel():
    global levelID
    global activeLevelData
    global framerate
    global numLeds
    levelID = levelID+1
    
    if levelID > len(levels) - 1:    
        levelID = 0
        AddNewArea(framerate, numLeds)
    else:    
        activeLevelData = levels[levelID]
        
    activeLevelData = levels[levelID]
    for a in range(len(allZones)):
        LevelZone = allZones[a]
        LevelZone.Restart(activeLevelData.initialLength)

def GetLevelZones():
    return allZones 
