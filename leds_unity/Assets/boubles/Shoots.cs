using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Shoots
    {
        int numLeds;

        public List<ExplotionParticle> explotions;
        public List<Bullet> bullets;
        float delayToAdd = 3;

        public void Init(int numLeds)
        {
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
                if(e.isOn)
                    e.OnUpdate(deltaTime);

            foreach (ExplotionParticle e in explotions)
                if (e.isOn)
                    e.OnUpdate(deltaTime);
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
        public void AddExplotion(int from, int to, int characterID)
        {
            for (int a = from; a < to; a++)
                AddExplotionParticle(a, characterID);
        }
        public void AddExplotionParticle(int ledID, int characterID)
        {
            Debug.Log("AddExplotionParticle " + ledID + " ch: " + characterID);
            int dir = 1;
            if (characterID == 2)  dir = -1;
            foreach (ExplotionParticle ex in explotions)
            {
                if (!ex.isOn)
                {
                    ex.Restart(ledID, dir);
                    return;
                }
            }
            ExplotionParticle e = new ExplotionParticle();
            e.Init(numLeds, ledID, dir);
            explotions.Add(e);
        } 
    }
}
