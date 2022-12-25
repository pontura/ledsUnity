using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Curves
{
    public List<Curve> all;

    public void Init()
    {
        all = new List<Curve>();
        Curve curve = new Curve();
        curve.Init(100, 130, 115, 0.5f);
        all.Add(curve);

        curve = new Curve();
        curve.Init(210, 260, 225, 0.6f);
        all.Add(curve);
    }
}
