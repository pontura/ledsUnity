using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Explotion : MonoBehaviour
{
    Color color;
    public List<Particle> all;
    int numLeds;
    int ledID;
    public bool on;
    int totalParticles;

    public void Init(int _numLeds, int _ledID, int _totalParticles) // init for the first time:
    {
        this.totalParticles = _totalParticles;
        this.numLeds = _numLeds;
        all = new List<Particle>();
        for (int a = 0; a < totalParticles; a++)
        {
            Particle particle = new Particle();
            all.Add(particle);
        }
        Init(ledID);
    }
    public void Init(int _ledID) // init from pool
    {
        on = true;
        this.ledID = _ledID;
        int a = 0;
        foreach (Particle particle in all)
        {
            float dir = 1f;

            a++;
            if (a>1)
            {
                dir = -1f;
                a = 0;
            }
            float speed = Random.Range(80f, 30f) / 20f;
            particle.SetSpeed(speed, dir);
            particle.Init(ledID);

            Debug.Log(speed+ " dir: " + dir);
        }
    }
    int lastLedID;
    public void OnUpdate(float deltaTime, float _speed)
    {
        float strongestParticle = 10;
        int a = 0;
        foreach (Particle p in all)
        {
            a++;
            p.OnUpdate(deltaTime, _speed);
            float speed = Mathf.Lerp(0.2f,p.speed, p.value / 255);
            p.ledID = (int)Mathf.Round(p.ledID + ((speed) * p.direction)/5); // move the particleExpllotion;
            if (p.ledID >= numLeds) p.ledID = 0;
            else if (p.ledID < 0) p.ledID = numLeds-1;
            strongestParticle = p.value;
        }
        if (strongestParticle < 1)
            on = false;
    }
}
