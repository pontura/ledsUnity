import math
class Explotion:
    color = (0,0,0)
    all = []
    numLeds = 0
    ledID = 0
    on = False
    totalParticles = 0
    fade_desaceleration = 0
    speed = 0

    def Init(_numLeds, _ledID, _color, _totalParticles, _fade_desaceleration, _speed) :

        self.totalParticles = _totalParticles
        self.numLeds = _numLeds
        
        for (int a = 0 a < totalParticles a++):    
            Particle particle = new Particle()
            all.Add(particle)
        
        InitFromPool(_ledID, _color, _fade_desaceleration, _speed)

    def InitFromPool(_ledID, _color, _fade_desaceleration, _speed):

        self.speed = _speed
        self.fade_desaceleration = _fade_desaceleration
        self.color = _color
        on = true
        a = 0
        num = 0
        foreach (Particle particle in all):   
           
            dir = 1f
            a++
            if (a>1):        
                dir = -1f
                a = 0
            
            self.ledID = _ledID + (int)(Mathf.Round(num / 2) * dir)
            if (ledID > numLeds - 1):
                ledID = 0
            elif (ledID < 0):
                ledID = numLeds - 1
            speed = Random.Range(60f, 25f) / 20f
            particle.SetSpeed(speed, dir)
            particle.Init(ledID, 255)
            num++
        

    lastLedID = 0
    def OnUpdate(float deltaTime):
        strongestParticle = 10
        a = 0
        foreach (Particle p in all):    
            a++
            p.OnUpdate(deltaTime, fade_desaceleration)
            value = Mathf.Lerp(0.2f,p.speed, p.value / 255)
            p.ledID = (int)Mathf.Round(p.ledID + (speed*(value) * p.direction)/8) // move the particleExpllotion
            if (p.ledID >= numLeds):
                p.ledID = 0
            else if (p.ledID < 0):
                p.ledID = numLeds-1
            strongestParticle = p.value
        
        if (strongestParticle < 1):
            on = False

