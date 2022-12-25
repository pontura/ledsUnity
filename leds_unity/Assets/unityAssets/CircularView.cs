using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CircularView : MonoBehaviour
{
    [SerializeField]
    LedAsset ledAsset_to_add;
    public float offset = 200;
    List<LedAsset> all;

    public void Init(int numLeds)
    {
        all = new List<LedAsset>();
        for (int a = 0; a<numLeds; a++)
        {
            LedAsset led = Instantiate(ledAsset_to_add, transform);
            led.Init((float)a /(float)numLeds * 360f, offset);
            all.Add(led);
        }
    }
    public void OnUpdate(List<Color> data)
    {
        int id = 0;
        foreach(LedAsset ledAsset in all)
        {
            ledAsset.UpdateState(data[id]);
            id++;
        }
    }
}
