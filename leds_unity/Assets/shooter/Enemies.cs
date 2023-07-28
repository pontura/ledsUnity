using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class Enemies
    {
        public int numLeds;
        public Color color = Color.green;

        public List<Enemy> all;
        float delayToAdd = 3;

        public void Init(int numLeds)
        {
            all = new List<Enemy>();
            this.numLeds = numLeds;
            AddEnemy(0);
        }
        float timer = 0;
        public void OnUpdate(int aimPos, float deltaTime)
        {
            timer += deltaTime;
            if (timer> delayToAdd)
                AddEnemy(aimPos);
            foreach (Enemy e in all)
            {
                if(e.isOn)
                    e.OnUpdate(deltaTime);
            }
        }
        void AddEnemy(int characterPos)
        {
            foreach (Enemy en in all)
            {
                if (!en.isOn)
                {
                    InitEnemy(en, characterPos);
                    return;
                }
            }
            Enemy e = new Enemy();
            e.Init(0.1f, numLeds, characterPos, color);
            InitEnemy(e, characterPos);
            all.Add(e);
            timer = 0;
        }
        public void CheckCollision(List<Explotion> explotions)
        {
            foreach (Enemy enemy in all)
            {
                foreach (Explotion e in explotions)
                    if (e.isOn)
                    {
                        foreach (int ledID in e.leds)
                            if (
                                enemy.ledId > ledID - e.width / 2 &&
                                enemy.ledId < ledID + e.width / 2
                                )
                                enemy.Die();
                    }
            }
        }
        void InitEnemy(Enemy enemy, int characterPos)
        {
            int thisLed = characterPos - (numLeds/2);

            if (thisLed < 0) thisLed = numLeds + thisLed;
            else if (thisLed >= numLeds) thisLed = thisLed - numLeds;
            enemy.Restart(thisLed);
        }
    }

}
