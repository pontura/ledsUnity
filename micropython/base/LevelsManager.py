import levelZone
import json

levels = []
allZones = []

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
    allData = json.load(s)
    

def Init(_numLeds, _frameRate):
    frameRate = _frameRate
    allZones = []
    numLeds = _numLeds
    AddNewArea()

def AddLevel(nextLength, speed, seconds, status, ease):
    global lastLength
    global lastStatus
    
    nextLength = nextLength * (numLeds / 100) # numLeds/100 normaliza de 0 a 100 el scalesss
    lData = LevelData
    lData.speed = speed
    lData.initialLength = lastLength
    lData.ease = ease

    if status == "":
        lData.status = lastStatus
    else:
        lData.status = status

    lData.nextLength = nextLength
    lData.seconds = seconds
    levels.append(lData)
    
    lastStatus = status
    lastLength = nextLength


def AddNewArea():
    global areaID
    areaData = allData["areas"][areaID]
    length = len(areaData) * (numLeds / 100)#//numLeds/100 normaliza de 0 a 100 el scalesss
    lastLength = length
    zones = areaData["zones"]
    qty = len(zones)
    _id = 0
    for a in range(qty):               
        thisLevelZone = levelZone.LevelZone()
        zonesData = zones[a]
        color = GetColor(zonesData["color"])
        pos = zonesData["pos"]*numLeds
        thisLevelZone.Init(_id, pos, length, color, numLeds, framerate)
        allZones.append(thisLevelZone)
        _id = _id+1
    
    levels =areaData["levels"]
    
    for a in range(len(levels)):
        lData = levels[a]
        status = ""            
        
        AddLevel(lData["nextLength"], lData["speed"], lData["seconds"], status, lData["ease"])
    
    
    areaID = areaID+1
    if areaID > len(allData["areas"])-1:
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
        level = allZones[a]
        UpdateLevel(level, deltaTime)

def UpdateLevel(level, deltaTime):
    activeLevelData = levels[levelID]
    if activeLevelData.nextLength != activeLevelData.initialLength:
        level.ScaleTo(activeLevelData.nextLength, activeLevelData.seconds, activeLevelData.ease, deltaTime)
    if activeLevelData.speed != 0:
        level.Move(activeLevelData.speed, activeLevelData.seconds, activeLevelData.ease, deltaTime)

    level.Process(activeLevelData.seconds, activeLevelData.status, deltaTime)

def  OnNextLevel():
    levelID = levelID+1
    if levelID > levels.Count - 1:    
        levelID = 0
        AddNewArea()
#     else:    
#         activeLevelData = levels[levelID]
    activeLevelData = levels[levelID]
    for a in range(len(allZones)):
        LevelZone = allZones[a]
        levelzone.Restart(activeLevelData.initialLength)

def GetLevelZones():
    return allZones 
