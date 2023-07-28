using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class Enemy
    {
        public int ledId;
        float pos;
        public Color color;
        Color originalColor;
        int numLeds;
        float speed;
        float dir;
        public bool isOn;

        public void Init(float speed, int numLeds, int ledId, Color _color)
        {
            this.speed = speed;
            if (ledId != 0) this.speed *= -1;
            this.numLeds = numLeds;
            this.originalColor = _color;
            this.color = _color;
            Restart(ledId);
        }
        public void Restart(int ledId)
        {
            if (Random.Range(0, 10) < 5) dir = 1; else dir = -1;
            this.ledId = ledId;
            this.pos = ledId;
            isOn = true;
        }
        public void OnUpdate(float deltaTime)
        {
            this.pos += speed * dir;
            if (pos >= numLeds) pos = 0;
            else if (pos < 0) pos = numLeds - 1;
            ledId = (int)pos;
        }
        public void Die()
        {
            isOn = false;
        }


    }

}
