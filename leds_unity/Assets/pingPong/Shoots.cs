using Boubles;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;

namespace PingPongGame
{
    public class Shoots
    {
        int numLeds;
        public PingPong game;
        public List<ExplotionParticle> explotions;
        public List<Bullet> bullets;
        float delayToAdd = 3;

        public void Init(PingPong game, int numLeds)
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

        public void OnUpdate(int centerLedID, float deltaTime)
        {
            //foreach (ExplotionParticle e in explotions)
            //{
            //    if (e.isOn)
            //    {
            //        e.OnUpdate(deltaTime);
            //        if (e.isOn)
            //        {
            //            Color c = e.color;
            //            c.a = e.alpha;
            //            game.ledsData[e.ledId] = c;
            //        }
            //    }
            //}

            foreach (Bullet bullet in bullets)
            {
                if (bullet.isOn)
                {
                    Debug.Log("is on");
                    ResetBullet(bullet);
                    if (bullet.isOn)
                    {
                        bullet.OnUpdate(deltaTime);
                        SetBullet(bullet);
                    }
                }
            }
        }   
        void SetBullet(Bullet bullet)
        {
            int ballID = game.ball.LedId;
            foreach (int l in bullet.leds)
            {
                if ((bullet.characterID == 1 && l <= ballID) ||
                    (bullet.characterID == 2 && l >= ballID)
                    )
                {
                    float force = 1;
                    if (bullet.characterID == 1) force *= -1;
                    game.ball.Collide(force, bullet.color);
                    bullet.Collide();
                    ResetBullet(bullet);
                    return;
                }
                else
                    game.ledsData[l] = game.colors[bullet.color];
            }
        }
        void ResetBullet(Bullet bullet)
        {
            foreach (int l in bullet.leds)
            {
                game.ledsData[l] = Color.black;
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
