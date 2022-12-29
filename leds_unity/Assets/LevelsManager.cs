using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class LevelsManager : MonoBehaviour
{
    List<LevelData> levels;
    List<LevelZone> allZones;

    int levelID;
    int areaID;
    int numLeds;
    float frameRate;
    int lastLength = 150;
    string lastStatus = "";

    public Data allData;
    [Serializable]
    public class Data
    {
        public List<AreaData> areas;
    }
    [Serializable]
    public class AreaData
    {
        public List<ZoneData> zones;
        public List<LevelData> levels;
        public int length;
    }
    [Serializable]
    public class ZoneData
    {
        public string color;
        public float pos; // normalized (0, 1)
    }
    [Serializable]
    public class LevelData
    {
        public string status; //"safe": zona libre con transparencia // "status": "full" hace daño
        public float speed;
        public int initialLength;
        public int nextLength;
        public int seconds;
        public string ease;
    }
    public void Init(int numLeds, float frameRate, string json)
    {
        this.frameRate = frameRate;
        allZones = new List<LevelZone>();
        this.numLeds = numLeds;
        SetLevels(json);
        AddNewArea();
    }
    void SetLevels(string json)
    {
        allData = JsonUtility.FromJson<Data>(json);
        Debug.Log(json);
        levels = new List<LevelData>(); 
    }
    void AddLevel(int nextLength, float speed, int seconds, string status, string ease)
    {
        nextLength = nextLength * (numLeds / 100); //numLeds/100 normaliza de 0 a 100 el scalesss
        LevelData lData = new LevelData();
        lData.speed = speed;
        lData.initialLength = lastLength;
        lData.ease = ease;

        if (status == "")
            lData.status = lastStatus;
        else
            lData.status = status;

        lData.nextLength = nextLength;
        lData.seconds = seconds;
        levels.Add(lData);
        
        lastStatus = status;
        lastLength = nextLength;
    }
    
    void AddNewArea()
    {
        lastLength = 0;
        Debug.Log("AddNewArea: " + areaID);
        AreaData areaData = allData.areas[areaID];
        allZones = new List<LevelZone>();
        float qty = areaData.zones.Count;
        for (int a = 0; a < qty; a++)
        {
            int length = areaData.length * (numLeds / 100); //numLeds/100 normaliza de 0 a 100 el scalesss
            LevelZone levelzone = new LevelZone();
            Color color = GetColor(areaData.zones[a].color);
            levelzone.Init(a, this, areaData.zones[a].pos*numLeds, length, color, numLeds, frameRate);
            allZones.Add(levelzone);
        }
        levels = new List<LevelData>();
        foreach (LevelData lData in areaData.levels)
        {
            AddLevel(lData.nextLength, lData.speed, lData.seconds, lData.status, lData.ease);
        }
        activeLevelData = levels[0];
        areaID++;
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
        foreach (LevelZone level in allZones)
            UpdateLevel(level, deltaTime);
    }
    void UpdateLevel(LevelZone level, float deltaTime)
    {
     //   Debug.Log("area: " + areaID + "   Level " + levelID + "   nextLength" +  activeLevelData.nextLength + "   initialLength:" +  activeLevelData.initialLength + "    speed:" + activeLevelData.speed + "    seconds:" + activeLevelData.seconds + " level " + level.from + " to:" + level.to);

        if (activeLevelData.nextLength != activeLevelData.initialLength)
            level.ScaleTo(activeLevelData.nextLength, activeLevelData.seconds, activeLevelData.ease, deltaTime);
        if (activeLevelData.speed != 0)
            level.Move(activeLevelData.speed, activeLevelData.seconds, activeLevelData.ease, deltaTime);

        level.Process(activeLevelData.seconds, activeLevelData.status, deltaTime);
    }
    LevelData activeLevelData;
    public void OnNextLevel()
    {
        Debug.Log("OnNextLevel  area: " + areaID + "   Add Level " + levelID);
        levelID++;
        if (levelID > levels.Count - 1)
        {
            levelID = 0;
            AddNewArea();
        }
        else
        {
            activeLevelData = levels[levelID];
        }
        foreach (LevelZone levelzone in allZones)
            levelzone.Restart(activeLevelData.initialLength);
    }
    public List<LevelZone> GetLevelZones()  { return allZones; }
    
}
