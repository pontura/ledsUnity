import settings

def GetPos(num):
    if num >=settings.numLeds:
        return 0
    elif num < 0:
        return settings.numLeds - 1
    return num

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b