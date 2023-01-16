import leds

zone1 = [200,210,220, 0.7] #start, max,end, max_value
leds_zone1 = []


def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

class Curves:

    def Init(self, leds):
        for i in range(zone1[0], zone1[1]):
            normalizedValue = (i-zone1[0])/(zone1[1] - zone1[0])
            value = lerp(0, zone1[3], normalizedValue)
            thisLed = leds.all[i]
            thisLed.SetCurve(value)
            leds_zone1.append(thisLed)
#             print (value)
        for i in range(zone1[1], zone1[2]):
            normalizedValue = (i-zone1[1])/(zone1[2] - zone1[1])
            value = lerp(zone1[3],0, normalizedValue)
            thisLed = leds.all[i]
            thisLed.SetCurve(value)
            leds_zone1.append(thisLed)
#             print (value)
            
       
    zoneLedOnID = 0 
    def SetCurves(self, dimmer_ar, leds):
        global zoneLedOnID
        self.zoneLedOnID = self.zoneLedOnID+1
        for i in range(0, len(leds_zone1)):
            thisLed = leds_zone1[i]            
            if i % 2 == 0:
                self.zoneLedOnID = 0
            else:
                leds.SetPixelBrighteness(dimmer_ar, (255,0,0), thisLed.id, thisLed.curveValue) 



