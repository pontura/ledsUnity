using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class Shoots
    {
        int numLeds;
        Color color = Color.red;

        public List<Explotion> all;
        float delayToAdd = 3;

        public void Init(int numLeds)
        {
            all = new List<Explotion>();
            this.numLeds = numLeds;
        }
        float timer = 0;
        public void OnUpdate(float deltaTime)
        {
            foreach (Explotion e in all)
                if(e.isOn)
                    e.OnUpdate(deltaTime);
        }
        public void Add(int ledID)
        {
            foreach (Explotion ex in all)
            {
                if (!ex.isOn)
                {
                    ex.Restart(ledID);
                    return;
                }
            }
            Explotion e = new Explotion();
            e.Init(this, numLeds, ledID, color);
            all.Add(e);
        } 
    }
}
