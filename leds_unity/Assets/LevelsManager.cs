using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class LevelsManager : MonoBehaviour
{
    List<LevelData> levels;
    List<LevelZone> all;
    int levelID;
    int numLeds;
    float frameRate;

    public class LevelData
    {
        public float speed;
        public int initialLength;
        public Color[] colors;
        public int nextLength;
        public int seconds;
    }
    public void Init(int numLeds, float frameRate)
    {
        this.frameRate = frameRate;
        all = new List<LevelZone>();
        this.numLeds = numLeds;
        levelID = -1;
        SetLevels();
        OnNextLevel();
    }
    void SetLevels()
    {
        levels = new List<LevelData>();
        AddZones(   150, new Color[] { Color.blue, Color.green });
        AddLevel(150,   2,      0,      5);
        AddLevel(2,     60,     0,      5);
        AddLevel(60,    2,      0,      3);
        AddLevel(2,     150,    0,      2);
        AddLevel(150,   100,    0,      2);
        AddLevel(100,   100,    80,      5);
        AddLevel(100,   100,   -80,      5);

    }
    void AddLevel( int initialLength, int nextLength, float speed, int seconds)
    {
        LevelData lData = new LevelData();
        lData.speed = speed;
        lData.initialLength = initialLength;
        lData.nextLength = nextLength;
        lData.seconds = seconds;

        levels.Add(lData);
    }
    
    void AddZones(int initialLength, Color[] colors)
    {
        all = new List<LevelZone>();
        float qty = colors.Length;
        for (int a = 0; a < qty; a++)
        {
            LevelZone levelzone = new LevelZone();
            levelzone.Init(a, this, a * (numLeds / qty), initialLength, colors[a], numLeds, frameRate);
            all.Add(levelzone);
        }
    }
    public void OnUpdate()
    {
        LevelData lData = levels[levelID];

        foreach (LevelZone level in all)
        {
            if(lData.nextLength != lData.initialLength)
            {
                int nextLength = lData.nextLength;
                level.ScaleTo(nextLength, lData.seconds);
            }
            if (lData.speed != 0)
            {
                level.Move(lData.speed, lData.seconds);
            }
        }      
    }
    public void OnNextLevel()
    {
        levelID++;
        if (levelID > levels.Count-1)
            levelID = 1;

        foreach (LevelZone levelzone in all)
            levelzone.Restart();

        Debug.Log("level:  " + levelID);

    }
    public List<LevelZone> GetLevelZones()  { return all; }
    
}
