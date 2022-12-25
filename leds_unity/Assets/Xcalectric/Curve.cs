using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Curve
{
    public List<float> values;
    public int from;
    int to;

    public void Init(int from, int to, int keyframe, float value)
    {
        this.from = from;
        this.to = to;

        values = new List<float>();
        int dest =  keyframe - from;
        for (int a = 0; a< dest; a++)
        {
            float lerpValue = (float)a / (float)(dest);
            float realValue = Mathf.Lerp(0, value, lerpValue);
            values.Add(realValue);
        }
        dest = to - keyframe;
        for (int a = 0; a < dest; a++)
        {
            float lerpValue = (float)a / (float)(dest);
            float realValue = Mathf.Lerp(value, 0, lerpValue);
            values.Add(realValue);
        }
    }
    public bool IsInsideCurve(int ledID)
    {
        if (ledID > from && ledID < to)
            return true;
        return false;
    }
    public float GetValue(int ledID)
    {
        return values[ledID-from];
    }
}
