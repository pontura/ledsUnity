using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Shoots
    {
        int numLeds;
        public BoublesGame game;
        public List<ExplotionParticle> explotions;
        public List<Bullet> bullets;
        float delayToAdd = 3;

        public void Init(BoublesGame game, int numLeds)
        {
            this.game = game;
            explotions = new List<ExplotionParticle>();
            bullets = new List<Bullet>();
            this.numLeds = numLeds;
        }
        float timer = 0;

        public void Restart()
        {
            explotions = new List<ExplotionParticle>();
            bullets = new List<Bullet>();
        }

        public void OnUpdate(int centerLedID, int data1Count, int data2Count, float deltaTime)
        {
            foreach (ExplotionParticle e in explotions)
            {
                if (e.isOn)
                {
                    e.OnUpdate(deltaTime);
                    if (e.isOn)
                    {
                        Color c = e.color;
                        c.a = e.alpha;
                        game.ledsData[e.ledId] = c;
                    }
                }
            }

            int max = data1Count + centerLedID;
            int max2 = centerLedID - data2Count;
            foreach (Bullet e in bullets)
            {
                if (e.isOn)
                {
                    e.OnUpdate(deltaTime);
                    if(e.isOn)
                    {
                        foreach (int l in e.leds)
                        {
                            if ((e.characterID == 1 && l <= max) ||
                                (e.characterID == 2 && l >= max2)
                                )
                            {
                                game.CollideWith(e.color, e.characterID);
                                e.Collide();
                            }
                            else
                            {
                                game.ledsData[l] = game.colors[e.color];
                            }
                        }
                    }
                }
            }
        }       
        public void AddBullet(int characterID, int ledID, int color)
        {
            foreach (Bullet b in bullets)
            {
                if (!b.isOn)
                {
                    b.Restart(characterID, ledID, color);
                    return;
                }
            }
            Bullet e = new Bullet();
            e.Init(this, characterID, numLeds, ledID, color);
            bullets.Add(e);
        }
        public void AddExplotion(int from, int to, int characterID, int color)
        {
            for (int a = from; a < to; a++)
                AddExplotionParticle(a, characterID, color);
        }
        public void AddExplotionParticle(int ledID, int characterID, int color)
        {
            int dir = 1;
            if (characterID == 2)  dir = -1;
            Color c = game.colors[color];
            foreach (ExplotionParticle ex in explotions)
            {
                if (!ex.isOn)
                {
                    ex.Restart(ledID, dir, c);
                    return;
                }
            }
            ExplotionParticle e = new ExplotionParticle();
           
            e.Init(numLeds, ledID, dir, c);
            explotions.Add(e);
        } 
    }
}
