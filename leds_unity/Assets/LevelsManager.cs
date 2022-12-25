using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class LevelsManager : MonoBehaviour
{
    public List<LevelZone> all;
    int levelID;
    int numLeds;

    List<LevelData> levels;

    public class LevelData
    {
        public int initialLength;
        public Color[] colors;
        public int nextLength;
        public int seconds;

        public void Init(int initialLength, int nextLength, int seconds)
        {
            this.initialLength = initialLength;
            this.nextLength = nextLength;
            this.seconds = seconds;
        }
    }
    public void Init(int numLeds)
    {
        all = new List<LevelZone>();
        this.numLeds = numLeds;
        levelID = -1;
        SetLevels();
        OnNextLevel();
    }
    void SetLevels()
    {
        levels = new List<LevelData>();
        AddZones(50, new Color[] { Color.blue, Color.green });
        AddLevel(   150, 5,      5);
        AddLevel(   5, 50,      5);
        AddLevel(   50, 5,      5);
    }
    void AddLevel(int initialLength, int nextLength, int seconds)
    {
        LevelData lData = new LevelData();
        lData.Init(initialLength, nextLength, seconds);
        levels.Add(lData);
    }
    
    void AddZones(int initialLength, Color[] colors)
    {
        all = new List<LevelZone>();
        float qty = colors.Length;
        for (int a = 0; a < qty; a++)
        {
            LevelZone levelzone = new LevelZone();
            levelzone.Init(a, this, a * (numLeds / qty), initialLength, colors[a], numLeds);
            all.Add(levelzone);
        }
    }
    public void OnUpdate()
    {
        LevelData lData = levels[levelID];

        foreach (LevelZone level in all)
        {
            int nextLength = lData.nextLength;
            level.ScaleTo(nextLength, lData.seconds);
        }
      
    }
    public void OnNextLevel()
    {
        levelID++;
        if (levelID > 2)
            levelID = 1;


        foreach (LevelZone levelzone in all)
            levelzone.Restart();


        Debug.Log("level:  " + levelID);

    }
    
}
