import math

class LevelZone:    
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

    def ScaleTo(nextLength, seconds, ease, deltaTime):
        lerpValue = GetValueByTweenInTime(ease, deltaTime, seconds, true)
        length = Mathf.Lerp(initialLength, nextLength, lerpValue)
       
    def Move(speed, seconds, ease, deltaTime):
        self.pos += GetValueByTweenInTime(ease, deltaTime, seconds, false)*(speed/100) 
        if pos > numLeds:
            pos = 0
        if pos < 0:
            pos = numLeds
       

    def Process( seconds,  _status,  deltaTime):
        self.status = _status
        tweenTimer += deltaTime / seconds
        timer += deltaTime
        SetFromAndTo()
        if isMaster:
            if timer > seconds:        
                Ready()
           
       

    def Restart(initialLength):
        self.initialLength = initialLength
        timer = 0
        tweenTimer = 0
        ready = false

    def IsInsideCurve(ledID):
        if vfrom<to and (ledID > vfrom or ledID < vto):
            return true
        elif vfrom > vto and (ledID > vfrom or ledID < vto):
            return true
        return false

    def GetColor():
        return color
       
    def Ready():
        if ready != true:
            timer = 0
            tweenTimer = 0
            ready = true
            levelsManager.OnNextLevel()

    def SetFromAndTo(self):
        mid = ((float)(self.length) / 2)
        self.vfrom = math.floor(self.pos) - mid
        self.vto = math.floor(self.pos) + mid
        self.vfrom = self.GetValueInsideLeds(self.vfrom)
        self.vto = self.GetValueInsideLeds(self.vto)

    def GetValueInsideLeds(self, ledID):

        if ledID > self.numLeds:
            return ledID - self.numLeds
        elif ledID < 0:
            return self.numLeds + ledID
        else:
            return ledID

    def GetValueByTweenInTime(ease, deltaTime, seconds, normalized):
        if ease == "inout":
            if normalized == true:        
                sqt = tweenTimer * tweenTimer
                return sqt / (2.0 * (sqt - tweenTimer) + 1.0)        
            else:        
                v = 0
                if tweenTimer < 0.5:
                    v = lerp(0, 1, tweenTimer * 2)
                else:
                    v = lerp(1, 0, (tweenTimer * 2)-1)
                return lerp(0, 1.0, v)       
        
        return lerp(0.0, 1.0, tweenTimer)

    def lerp(a: float, b: float, t: float) -> float:
        return (1 - t) * a + t * b
