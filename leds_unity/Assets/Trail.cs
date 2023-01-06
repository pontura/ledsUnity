using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Trail
{
    Color color;
    public List<Particle> all;

    public void Init()
    {
        all = new List<Particle>();
    }
    int lastLedID;
    public void OnUpdate(float deltaTime, int ledID, float _fade_desaceleration)
    {
        foreach (Particle p in all)
            p.OnUpdate(deltaTime, _fade_desaceleration);

        if (lastLedID == ledID) return;
        Particle trail = GetParticleOrCreate();
        trail.Init(ledID, 180);
    }
    Particle GetParticleOrCreate()
    {
        foreach (Particle t in all)
            if (t.IsAvailable())
                return t;
        Particle trail = new Particle();
        all.Add(trail);
        return trail;
    }
}
