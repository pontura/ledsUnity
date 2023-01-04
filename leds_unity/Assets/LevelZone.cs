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
    float initialLength;
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
        this.initialLength = length;
        this.length = length;
        this.numLeds = numLeds;
        this.color = color;
        SetFromAndTo();
    }

    float tweenTimer = 0.0f; // de cero a uno siempre:
    float timer = 0.0f; // tiempo real

    public void ScaleTo(float nextLength, float seconds, string ease, float deltaTime)
    {
        float lerpValue = GetValueByTweenInTime(ease, deltaTime, seconds, true);
        length = Mathf.Lerp(initialLength, nextLength, lerpValue);
        //if (isMaster) Debug.Log(length + " lerp: " + lerpValue + "   tweenTimer: " + tweenTimer + "     from-to" + initialLength + ":" + nextLength + "      ease" + ease);
    }
    
    public void Move(float speed, float seconds, string ease, float deltaTime)
    {
        this.pos += GetValueByTweenInTime(ease, deltaTime, seconds, false)*(speed/100); 
        if (pos > numLeds) pos = 0;
        if (pos < 0) pos = numLeds;
       
    }
    public void Process(float seconds, string status, float deltaTime)
    {
        tweenTimer += deltaTime / seconds;
        timer += deltaTime;
        SetFromAndTo();
        if (isMaster)
        {
            if (timer > seconds)
            {
                Ready();
            }
        }
        if (status == "safe")
            color.a = 0.45f;
        else
            color.a = 1;
    }


    public void Restart(float initialLength)
    {
        this.initialLength = initialLength;
        timer = 0;
        tweenTimer = 0;
        ready = false;
    }
    public bool IsInsideCurve(int ledID)
    {
        if(from<to && ledID > from && ledID < to)
            return true;
        else if (from > to && (ledID > from || ledID < to))
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
        timer = 0;
        tweenTimer = 0;
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
    float GetValueByTweenInTime(string ease, float deltaTime, float seconds, bool normalized) // normalized va de 0 a 1 siempre
    {      
        if (ease == "inout")
        {
            if (normalized)
            {
                float sqt = tweenTimer * tweenTimer;
                return sqt / (2.0f * (sqt - tweenTimer) + 1.0f);
            }
            else
            {
                float v = 0;
                if (tweenTimer < 0.5f)
                    v = Mathf.SmoothStep(0f, 1f, tweenTimer * 2);
                else
                    v = Mathf.SmoothStep(1f, 0f, (tweenTimer * 2)-1);
                return Mathf.Lerp(0f, 1.0f, v);
            }
        }
        return Mathf.SmoothStep(0.0f, 1.0f, tweenTimer);
    }
}
