import math
import LevelsManager

class LevelZone:
    color = (0,0,0)
    vfrom = 0
    vto = 0
    numLeds = 0
    pos = 0
    scaleSpeed = 0
    initialLength = 0
    length = 0
    frameRate = 0
    status = ""
    isMaster = False
    ready = False
    tweenTimer = 0
    
    def Init(self, _id, pos, length, color, numLeds, frameRate):
        self.frameRate = frameRate
        
        if _id ==0:
            self.isMaster = True
        else:
            self.isMaster = False
            
        #self.levelsManager = levelsManager
        self.pos = pos
        self.initialLength = length
        self.length = length
        self.numLeds = numLeds
        self.color = color
        self.SetFromAndTo()


    tweenTimer = 0.0
    timer = 0.0

    def ScaleTo(self, nextLength, seconds, ease, deltaTime):
        lerpValue = self.GetValueByTweenInTime(ease, deltaTime, seconds, True)
        self.length = self.lerp(self.initialLength, nextLength, lerpValue)
        #print("seconds: ", seconds,  " initialLength", self.initialLength, " length: ", self.length, " nextLength: ", nextLength, " lerpValue: ", lerpValue )
       
    def Move(self,speed, seconds, ease, deltaTime):
       # print("move", self.pos)
        self.pos += self.GetValueByTweenInTime(ease, deltaTime, seconds, False)*(speed/100) 
        if self.pos > self.numLeds:
           self.pos = 0
        if self.pos < 0:
            self.pos = self.numLeds
       

    def Process( self,seconds,  _status,  deltaTime):
        self.status = _status
        self.tweenTimer += deltaTime / seconds
        self.timer += deltaTime
        self.SetFromAndTo()
        if self.isMaster:
            if self.timer > seconds:        
                self.Ready()       

    def Restart(self,initialLength):
        self.initialLength = initialLength
        self.timer = 0
        self.tweenTimer = 0
        self.ready = False

    def IsInsideCurve(self, ledID):
        if self.vfrom<self.vto and (ledID > self.vfrom or ledID < self.vto):
            return True
        elif self.vfrom > self.vto and (ledID > self.vfrom or ledID < self.vto):
            return True
        return False

    def GetColor(self):
        return self.color
       
    def Ready(self):
        if self.ready != True:
            self.timer = 0
            self.tweenTimer = 0
            self.ready = True
            LevelsManager.OnNextLevel()

    def SetFromAndTo(self):
        mid = ((float)(self.length) / 2)
        f = math.floor(self.pos) - mid
        t = math.floor(self.pos) + mid
        self.vfrom = int(self.GetValueInsideLeds(f))
        self.vto = int(self.GetValueInsideLeds(t))

    def GetValueInsideLeds(self, ledID):
        if ledID > self.numLeds:
            return ledID - self.numLeds
        elif ledID < 0:
            return self.numLeds + ledID
        else:
            return ledID

    def GetValueByTweenInTime(self, ease, deltaTime, seconds, normalized):
        if ease == "inout":
            if normalized == True:        
                sqt = self.tweenTimer * self.tweenTimer
                return sqt / (2.0 * (sqt - self.tweenTimer) + 1.0)        
            else:        
                v = 0
                if self.tweenTimer < 0.5:
                    v = self.lerp(0, 1, self.tweenTimer * 2)
                else:
                    v = self.lerp(1, 0, (self.tweenTimer * 2)-1)
                return self.lerp(0, 1.0, v)       
        
        return self.lerp(0.0, 1.0, self.tweenTimer)

    def lerp(self, a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
