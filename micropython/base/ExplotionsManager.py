import time
explotions = []
numLeds = 0

def init(self, numLeds):
    self.numLeds = numLeds
    
def GetExplotions():
    return explotions

def AddExplotionDouble(_ledId, color, delay):
    print("double")
#     	  yield return new WaitForSeconds(0.15f);
#         AddExplotion(_ledId, Color.white,   20, 450, 3);
#         yield return new WaitForSeconds(0.1f);
#         AddExplotion(_ledId, Color.red,     10, 300, 1.8f);
#         yield return new WaitForSeconds(0.1f);
#         AddExplotion(_ledId, color,         25, 100, 1.45f);

def AddExplotion(_ledId, color,totalParticles, _fade_desaceleration, _speed):
    foreach e in explotions:
        if (!e.on):
            e.Init(_ledId, color, _fade_desaceleration, _speed);
            return;
    explotion = new Explotion;
    explotion.Init(numLeds, _ledId, color, totalParticles, _fade_desaceleration, _speed);
    explotions.Add(explotion);

    
