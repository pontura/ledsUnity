using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class ExplotionParticle
    {
        float speed;
        public int ledId;
        public float alpha;
        int numLeds;
        float timer;
        public bool isOn;
        int dir;
        float pos;

        public void Init(int numLeds, int ledId, int dir)
        {
            this.ledId = ledId;
            this.numLeds = numLeds;
            Restart(ledId, dir);
        }
        public void Restart(int ledId, int dir)
        {
            timer = 0;
            isOn = true;
            this.dir = dir;
            this.speed = Random.Range(20, 80);
            this.ledId = ledId;
            this.pos = ledId;
            int thisLed = (int)pos;
            alpha = 1;

        }
        public void OnUpdate(float deltaTime)
        {
            timer += deltaTime;
            if (timer < 0.05f) return;
            speed /= 1.01f;
            pos += deltaTime * speed * dir;
            alpha -= deltaTime/2;
            if (alpha < 0) alpha = 0;
           
            ledId = (int)pos;
            if (ledId < 0) ledId = numLeds - 1 + ledId;
            else if (ledId >= numLeds) ledId = ledId - numLeds;

            if (timer > 1)
                isOn = false;
        }
       
    }

}
