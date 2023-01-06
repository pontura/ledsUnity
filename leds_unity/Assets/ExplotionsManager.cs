using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ExplotionsManager
{
    List<Explotion> explotions;
    int numLeds;

    public List<Explotion> GetExplotions()
    {
        return explotions;
    }
    public void Init(int numLeds)
    {
        this.numLeds = numLeds;
        explotions = new List<Explotion>();
    }
    public IEnumerator AddExplotionDouble(int _ledId, Color color, float delay)
    {
        yield return new WaitForSeconds(0.15f);
        AddExplotion(_ledId, Color.white,   20, 450, 3);
        yield return new WaitForSeconds(0.1f);
        AddExplotion(_ledId, Color.red,     10, 300, 1.8f);
        yield return new WaitForSeconds(0.1f);
        AddExplotion(_ledId, color,         25, 100, 1.45f);
    }
    public void AddExplotion(int _ledId, Color color, int totalParticles, float _fade_desaceleration, float _speed)
    {
        foreach (Explotion e in explotions)
        {
            if (!e.on)
            {
                e.Init(_ledId, color, _fade_desaceleration, _speed);
                return;
            }
        }
        Explotion explotion = new Explotion();
        explotion.Init(numLeds, _ledId, color, totalParticles, _fade_desaceleration, _speed);
        explotions.Add(explotion);
    }
}
