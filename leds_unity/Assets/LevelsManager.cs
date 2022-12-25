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
    int lastLength = 150;

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
        AddZones(lastLength, new Color[] { Color.blue, Color.green, Color.red });
        AddLevel(2, 0, 5);
        AddLevel(60, 0, 5);
        AddLevel(2, 0, 3);
        AddLevel(145, 0, 2);
        AddLevel(70, 0, 2);
        AddLevel(70, 40, 3);
        AddLevel(2, 0, 2);
        AddLevel(70, 0, 2);
        AddLevel(70, -40, 3);
        AddLevel(100, 0, 2); 

        AddLevel(100, 60, 5);
        AddLevel(125, 0, 1);
        AddLevel(100, 0, 1);
        AddLevel(100, -60, 5);

        AddLevel(105, 80, 2);
        AddLevel(2, 0, 4);
        AddLevel(125, 0, 2);
        AddLevel(20, -80, 5);

        AddLevel(2, 0, 2);

    }
    void AddLevel(int nextLength, float speed, int seconds)
    {
        LevelData lData = new LevelData();
        lData.speed = speed;
        lData.initialLength = lastLength;
        lData.nextLength = nextLength;
        lData.seconds = seconds;
        levels.Add(lData);
        lastLength = nextLength;
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
    public void OnUpdate(float deltaTime)
    {
        LevelData lData = levels[levelID];

        foreach (LevelZone level in all)
        {
            if(lData.nextLength != lData.initialLength)
            {
                int nextLength = lData.nextLength;
                level.ScaleTo(nextLength, lData.seconds, deltaTime);
            }
            level.Move(lData.speed, lData.seconds, deltaTime);
        }      
    }
    public void OnNextLevel()
    {
        levelID++;
        if (levelID > levels.Count-1)
            levelID = 1;

        foreach (LevelZone levelzone in all)
            levelzone.Restart();
        
    }
    public List<LevelZone> GetLevelZones()  { return all; }
    
}
