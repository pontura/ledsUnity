using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CircularView : MonoBehaviour
{
    static CircularView mInstance = null;
    [SerializeField]
    LedAsset ledAsset_to_add;
    public float offset = 200;
    List<LedAsset> all;
    void Start()
    {
        if (mInstance == null)
            mInstance = this as CircularView;
        Init(300);
    }
    public static CircularView Instance
    {
        get {  return mInstance;   }
    }
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
    List<Color> data;
    public void OnUpdate(List<Color> data)
    {
        this.data = data;
    }
    int a = 0;
    void Update()
    {
        if (data == null) return;
        a++;
        if (a < 10) return;
        a = 0;
        int id = 0;
        foreach (LedAsset ledAsset in all)
        {
            if (id >= data.Count - 1) return;
            Color c = data[id];
            ledAsset.UpdateState(c);
            id++;
        }
    }
}
