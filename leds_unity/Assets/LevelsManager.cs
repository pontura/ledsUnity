using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class LevelsManager : MonoBehaviour
{
    List<LevelData> levels;
    List<LevelZone> all;
    int levelID;
    int areaID;
    int numLeds;
    float frameRate;
    int lastLength = 150;

    public Data allData;
    [Serializable]
    public class Data
    {
        public List<AreaData> areas;
    }
    [Serializable]
    public class AreaData
    {
        public List<ColorData> colors;
        public List<LevelData> levels;
        public int length;
    }
    [Serializable]
    public class ColorData
    {
        public string color;
        public int pos;
    }
    [Serializable]
    public class LevelData
    {
        public float speed;
        public int initialLength;
        public int nextLength;
        public int seconds;
    }
    public void Init(int numLeds, float frameRate, string json)
    {
        this.frameRate = frameRate;
        all = new List<LevelZone>();
        this.numLeds = numLeds;
        levelID = -1;
        SetLevels(json);
        OnNextLevel();
    }
    void SetLevels(string json)
    {
        allData = JsonUtility.FromJson<Data>(json);
        Debug.Log(json);
        levels = new List<LevelData>();
        AreaData areaData = allData.areas[areaID];
        AddZones(areaData);

        foreach(LevelData lData in areaData.levels)
        {
            AddLevel(lData.nextLength, lData.speed, lData.seconds);
        }

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
    
    void AddZones(AreaData areaData)
    {
        all = new List<LevelZone>();
        float qty = areaData.colors.Count;
        for (int a = 0; a < qty; a++)
        {
            LevelZone levelzone = new LevelZone();
            Color color = GetColor(areaData.colors[a].color);
            levelzone.Init(a, this, a * (numLeds / qty), areaData.length, color, numLeds, frameRate);
            all.Add(levelzone);
        }
    }
    Color GetColor(string colorName)
    {
        switch (colorName)
        {
            case "red": return Color.red;
            case "green": return Color.green;
            case "blue": return Color.blue;
        }
        return Color.black;
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
