using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class Aim
    {
        public int ledId;
        public float pos;
        public Color color;
        public Color originalColor;
        int numLeds;
        public float speed;
        public int state;
        float maxSpeed;
        float dangerZoneMaxSpeed;
        float originalSpeed;
        float aceleration;

        public void Init(int numLeds, int _ledID, Color _color, float maxSpeed)
        {
            state = 1;
            this.originalSpeed = maxSpeed;
            this.dangerZoneMaxSpeed = maxSpeed / 2;
            this.maxSpeed = maxSpeed;
            this.numLeds = numLeds;
            this.originalColor = _color;
            this.color = _color;
            this.ledId = _ledID;
            pos = ledId;
        }
        public void OnUpdate(float _speed, float deltaTime)
        {
            if (state == 1 || state == 2)
                Move(_speed, deltaTime);
        }
        float lastSpeed;
        void Move(float _speed, float deltaTime)
        {
            lastSpeed = Mathf.Lerp(lastSpeed, _speed * maxSpeed, deltaTime * 5);
            this.speed = lastSpeed;
            if (state == 1)
            {
                this.pos = this.pos + speed;
                if (pos >= numLeds) pos = 0;
                else if (pos < 0) pos = numLeds - 1;
                ledId = (int)pos;
            }
        }

        public void Crash()
        {
            color = Color.white;
            state = 2;
            speed = 0;
        }
        float timeToRestart = 1;
       
        void Restart()
        {
            color = originalColor;
            state = 1;
            speed = 0;
        }
    }

}
