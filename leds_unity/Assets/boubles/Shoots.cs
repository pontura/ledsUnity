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
            explotions.Clear();
            bullets.Clear();
        }

        public void OnUpdate(float deltaTime)
        {
            foreach (Bullet e in bullets)
            {
                if (e.isOn)
                { 
                    

                    e.OnUpdate(deltaTime);
                }
            }

            foreach (ExplotionParticle e in explotions)
                if (e.isOn)
                    e.OnUpdate(deltaTime);

            Draw();
        }
        void Draw()
        {
            foreach (ExplotionParticle a in explotions)
            {
                if (a.isOn)
                {
                    Color c = a.color;
                    c.a = a.alpha;
                    game.ledsData[a.ledId] = c;
                }
            }

            int ledId = 0;
            foreach (Bullet b in bullets)
            {
                if (b.isOn)
                {
                    int max = game.enemies.data.Count + game.enemies.centerLedID;
                    int max2 = game.enemies.centerLedID - game.enemies.data2.Count;
                    foreach (int l in b.leds)
                    {
                        if ((b.characterID == 1 && ledId == 0 && l <= max) ||
                            (b.characterID == 2 && ledId == 0 && l >= max2)
                            )
                        {
                            game.enemies.CollideWith(b.color, b.characterID);
                            b.Collide();
                            return;
                        }
                        game.ledsData[l] = game.colors[b.color];
                    }
                    ledId++;
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
