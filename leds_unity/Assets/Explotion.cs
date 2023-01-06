using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Explotion : MonoBehaviour
{
    public Color color;
    public List<Particle> all;
    int numLeds;
    int ledID;
    public bool on;
    int totalParticles;
    float fade_desaceleration;
    float speed;

    public void Init(int _numLeds, int _ledID, Color _color, int _totalParticles, float _fade_desaceleration, float _speed) // init for the first time:
    {
        this.totalParticles = _totalParticles;
        this.numLeds = _numLeds;
        all = new List<Particle>();
        for (int a = 0; a < totalParticles; a++)
        {
            Particle particle = new Particle();
            all.Add(particle);
        }
        Init(_ledID, _color, _fade_desaceleration, _speed);
    }
    public void Init(int _ledID, Color _color, float _fade_desaceleration, float _speed) // init from pool
    {
        this.speed = _speed;
        this.fade_desaceleration = _fade_desaceleration;
        this.color = _color;
        on = true;
        int a = 0;
        int num = 0;
        foreach (Particle particle in all)
        {
           
            float dir = 1f;
            a++;
            if (a>1)
            {
                dir = -1f;
                a = 0;
            }
            this.ledID = _ledID + (int)(Mathf.Round(num / 2) * dir);
            if (ledID > numLeds - 1) ledID = 0; else if (ledID < 0) ledID = numLeds - 1;
            float speed = Random.Range(60f, 25f) / 20f;
            particle.SetSpeed(speed, dir);
            particle.Init(ledID, 255);
            num++;
        }
    }
    int lastLedID;
    public void OnUpdate(float deltaTime)
    {
        float strongestParticle = 10;
        int a = 0;
        foreach (Particle p in all)
        {
            a++;
            p.OnUpdate(deltaTime, fade_desaceleration);
            float value = Mathf.Lerp(0.2f,p.speed, p.value / 255);
            p.ledID = (int)Mathf.Round(p.ledID + (speed*(value) * p.direction)/8); // move the particleExpllotion;
            if (p.ledID >= numLeds) p.ledID = 0;
            else if (p.ledID < 0) p.ledID = numLeds-1;
            strongestParticle = p.value;
        }
        if (strongestParticle < 1)
            on = false;
    }
}
