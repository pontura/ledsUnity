using System;
using UnityEngine;

namespace PingPongGame
{
    public class Ball
    {
        float ledId;
        public int LedId {
            get { return (int)Mathf.Round(ledId); }
        }

        public int color;
        int numLeds;
        float speed = 0;
        float weight = 12f;
        PingPong game;

        public void Init(PingPong game, int numLeds, int centerLedID, int _color)
        {
            this.game = game;     
            this.numLeds = numLeds;
            this.color = _color;
            Restart(centerLedID);
        }
        public void Restart(int centerLedID)
        {
            this.ledId = centerLedID;
        }
        int titlaID;
        public void OnUpdate(float deltaTime)
        {
            if (speed>0)
                speed -= weight * (deltaTime / 50);
            else if(speed<0)
                speed += weight * (deltaTime / 50);

            float totalSpeed = Mathf.Abs(speed);
            if (totalSpeed < 0.001f) 
                speed = 0;
            else
            {
                SetColor(Color.black);
            }
            ledId = ledId + speed;
            SetColor(game.colors[color]);

            if (titlaID == 1 && game.colors[color] != Color.black)
            {
                titlaID = 0;
                game.ledsData[LedId] = Color.white;
            }
            else
            {
                game.ledsData[LedId] = game.colors[color];
            }
        }
        void SetColor(UnityEngine.Color c)
        {
            if (ledId < 1) return;
            if (ledId > numLeds-2) return;

            game.ledsData[LedId - 1] = c;
            if (c != Color.black)
            {
                game.ledsData[LedId] = Color.white;
            }
            game.ledsData[LedId + 1] = c;

        }
        public void Collide(float force, int collisionColor)
        {
            if (collisionColor == color)
            {
                speed = force / 5;
            }
            else
            {
                this.color = collisionColor;
                Color c = game.colors[this.color];
                SetColor(c);
            }

             Debug.Log("collide " + force);
            // speed += force*1000;
        }

    }

}
