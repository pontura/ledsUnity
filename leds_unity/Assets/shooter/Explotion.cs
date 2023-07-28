using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class Explotion
    {
        public int ledId;
        public float width = 7;
        public Color color;
        public Color originalColor;
        int numLeds;
        public Shoots shoots;
        public float dir;
        float timer;
        public List<int> leds;
        public bool isOn;

        public void Init(Shoots shoots, int numLeds, int ledId, Color _color)
        {
            Debug.Log("Init " + numLeds);
            this.ledId = ledId;
            leds = new List<int>();
            for (int a = 0; a < width; a++)
                leds.Add(0);
            this.shoots = shoots;
            this.numLeds = numLeds;
            this.originalColor = _color;
            this.color = _color;
            Restart(ledId);

        }
        public void Restart(int ledId)
        {
            this.ledId = ledId;
            timer = 0;
            isOn = true;
            int thisLed = ledId - (int)(Mathf.Floor(width/2));
            if (thisLed < 0) thisLed = numLeds-1 + thisLed;
            else if (thisLed >= numLeds) thisLed = thisLed - numLeds;
            for (int a = 0; a < width; a++)
            {
                if (thisLed < 0) thisLed = numLeds + thisLed;
                else if (thisLed >= numLeds) thisLed = thisLed - numLeds;
                leds[a] = thisLed;
                thisLed++;
            }
        }
        public void OnUpdate(float deltaTime)
        {
            timer += deltaTime;
            if (timer > 1)
                isOn = false;
        }
       
    }

}
