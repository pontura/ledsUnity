using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Character
{
    public int ledId;
    public float pos;
    public Color color;
    public Color originalColor;
    int numLeds;
    public float speed;
    public int state;
    float maxSpeed;
    float dangerZoneMaxSpeed;
    float originalSpeed;
    float aceleration;
    public Trail trail;
    //1 move
    //2 in danger
    //3 crash

    public void Init(int numLeds, int _ledID, Color _color, float maxSpeed)
    {
        this.trail = new Trail();
        trail.Init();
        state = 1;
        this.originalSpeed = maxSpeed;
        this.dangerZoneMaxSpeed = maxSpeed / 2;
        this.maxSpeed = maxSpeed; 
        this.numLeds = numLeds;
        this.originalColor = _color;
        this.color = _color;
        this.ledId = _ledID;
        pos = ledId;
    }
    public void OnUpdate(float _speed, float deltaTime)
    {
        float trail_fade_desaceleration = 500;
        trail.OnUpdate(deltaTime, (int)pos, trail_fade_desaceleration);
        if (state == 1 || state == 2)
            Move(_speed, deltaTime);
        else if (state == 3)
            CheckToBeBack();
    }
    float lastSpeed;
    void Move(float _speed, float deltaTime)
    {
        lastSpeed = Mathf.Lerp(lastSpeed, _speed*maxSpeed, deltaTime * 30);
        this.speed = lastSpeed;
        if (state == 1)
        {
            this.pos = this.pos + speed;
            if (pos >= numLeds) pos = 0;
            else if (pos < 0) pos = numLeds - 1;
            ledId = (int)pos;
        }
    }

    public void OutOfDanger()
    {
        color = originalColor;
        maxSpeed = originalSpeed;
        state = 1;
        timer = 0;
    }
    float timer;
    public void InDangerZone()
    {
        state = 2;
        timer += Time.deltaTime;
        color = Color.white;
        maxSpeed = dangerZoneMaxSpeed;
        if (timer > 0.5f)
            Crash();
    }
    public void Crash()
    {
        color = Color.white;
        state = 2;
        speed = 0;
    }
    float timeToRestart = 1;
    void CheckToBeBack()
    {
        timer += Time.deltaTime;
        if (timer > timeToRestart)
            Restart();
    }
    void Restart()
    {
        color = originalColor;
        timer = 0;
        state = 1;
        speed = 0;
    }
}
