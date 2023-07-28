using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Bullet
    {
        public int characterID;
        public int ledId;
        public float width = 7;
        public int color;
        int numLeds;
        public Shoots shoots;
        public float dir;
        float timer;
        public List<int> leds;
        public bool isOn;
        float pos;
        float speed = 100f;

        public void Init(Shoots shoots, int characterID, int numLeds, int ledId, int _color)
        {
            this.ledId = ledId;
            leds = new List<int>();
            for (int a = 0; a < width; a++)
                leds.Add(0);
            this.shoots = shoots;
            this.numLeds = numLeds;
            Restart(characterID, ledId, _color);
        }
        public void Restart(int characterID, int ledId, int _color)
        {
            this.characterID = characterID;
            this.color = _color;
            this.pos = ledId;
            this.ledId = ledId;
            timer = 0;
            isOn = true;           
        }
        public void OnUpdate(float deltaTime)
        {
            if ( characterID == 1)
            {
                this.pos -= deltaTime * speed;
                if (this.pos < 0)
                {
                    isOn = false; return;
                }
            }
            else
            {
                this.pos += deltaTime * speed;
                if (this.pos > numLeds - 1)
                {
                    isOn = false; return;
                }
            }
           
            this.ledId = (int)pos;
            int thisLed = ledId - (int)(Mathf.Floor(width / 2));
            if (thisLed < 0) thisLed = numLeds - 1 + thisLed;
            else if (thisLed >= numLeds) thisLed = thisLed - numLeds;
            for (int a = 0; a < width; a++)
            {
                if (thisLed < 0) thisLed = numLeds + thisLed;
                else if (thisLed >= numLeds) thisLed = thisLed - numLeds;
                leds[a] = thisLed;
                thisLed++;
            }
        }
        public void Collide()
        {
            this.isOn = false;
        }


    }

}
