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

    public void Init(int id, LevelsManager levelsManager, float pos, int length, Color color, int numLeds)
    {
        isMaster = id == 0;
        this.levelsManager = levelsManager;
        this.pos = pos;
        this.length = length;
        this.numLeds = numLeds;
        this.color = color;
        SetFromAndTo();
    }
    public void Restart()
    {
        t = 0.0f;
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
    public void Move(float speed)
    {
        this.pos += (speed * Time.deltaTime);
        SetFromAndTo();
    }
    void Ready()
    {
        t = 0.0f;
        ready = true;
        levelsManager.OnNextLevel();
    }
   
    float t = 0.0f;
    public void ScaleTo(float nextLength, float seconds)
    {
        t += Time.deltaTime / seconds;
        length  = Mathf.Lerp(length, nextLength, Mathf.SmoothStep(0.0f, 1.0f, t));
        SetFromAndTo();
        if (isMaster && Mathf.Abs(length - nextLength) <= 2f)
            Ready();
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
