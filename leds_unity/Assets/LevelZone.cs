using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LevelZone
{
    Color color;
    public int from;
    public int to;
    int numLeds;
    float pos;
    float scaleSpeed;
    float length;
    LevelsManager levelsManager;
    public bool ready;
    bool isMaster;
    float frameRate;
    public void Init(int id, LevelsManager levelsManager, float pos, int length, Color color, int numLeds, float frameRate)
    {
        this.frameRate = frameRate;
         isMaster = id == 0;
        this.levelsManager = levelsManager;
        this.pos = pos;
        this.length = length;
        this.numLeds = numLeds;
        this.color = color;
        SetFromAndTo();
    }

    float scale_timer = 0.0f;
    float move_timer = 0.0f;
    public void ScaleTo(float nextLength, float seconds, float deltaTime)
    {
        scale_timer += deltaTime / seconds;
        length = Mathf.Lerp(length, nextLength, Mathf.SmoothStep(0.0f, 1.0f, scale_timer));
        SetFromAndTo();
        if (isMaster)
        {
            if (Mathf.Abs(length - nextLength) <= 1f)
            {
                Ready();
            }
        }
    }
    public void Move(float speed, float seconds, float deltaTime)
    {
        move_timer += deltaTime;
        this.pos += (speed * deltaTime);
        if (pos > numLeds) pos = 0;
        if (pos < 0) pos = numLeds;
        SetFromAndTo();
        if (isMaster)
        {
            if(move_timer > seconds)
            {
                Ready();
            }
        }
    }


    public void Restart()
    {
        move_timer = 0;
        scale_timer = 0;
        ready = false;
    }
    public bool IsInsideCurve(int ledID)
    {
        if (ledID > from && ledID < to)
            return true;
        return false;
    }
    public Color GetColor()
    {
        return color;
    }   
    void Ready()
    {
        if (ready) return;
        move_timer = 0;
        scale_timer = 0;
        ready = true;
        levelsManager.OnNextLevel();
    }
    void SetFromAndTo()
    {
        float mid = ((float)(length) / 2);
        this.from = (int)Mathf.Round(pos) - (int)mid;
        this.to = (int)Mathf.Round(pos) + (int)mid;
        from = GetValueInsideLeds(from);
        to = GetValueInsideLeds(to);
    }
    int GetValueInsideLeds(int ledID)
    {
        if (ledID > numLeds) return ledID - numLeds;
        else if (ledID < 0) return numLeds + ledID;
        return ledID;
    }
}
