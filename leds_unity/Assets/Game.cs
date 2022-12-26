using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Game : MonoBehaviour
{
    List<Character> characters;
    LevelsManager levelsManager;
    int numLeds = 300;
    [SerializeField] CircularView view;
    float framerate = 30;
    List<Color> ledsData;
    InputsManager inputs;
    [SerializeField] TextAsset jsonData;

    void Start()
    {
        inputs = GetComponent<InputsManager>();
        characters = new List<Character>();
        for (int a = 0; a < 2; a++)
        {
            Character ch = new Character();
            if (a == 0)
                ch.Init(numLeds, 0, Color.blue, 3);
            else
                ch.Init(numLeds, numLeds/2, Color.green, 3);
            characters.Add(ch);
        }
        view.Init(numLeds);
        ledsData = new List<Color>();
        for (int a = 0; a < numLeds; a++)
            ledsData.Add(Color.black);
        levelsManager = GetComponent<LevelsManager>();
        levelsManager.Init(numLeds, GetFrameRate(), jsonData.text);
        Loop();
    }
    void Loop()
    {
        float deltaTime = Time.deltaTime;
        SetData();
        levelsManager.OnUpdate(deltaTime);
        characters[0].OnUpdate(inputs.character1_speed, deltaTime);
        characters[1].OnUpdate(inputs.character2_speed, deltaTime);
        CheckCollision();
        SendData();
        Invoke("Loop", GetFrameRate());
    }
    public float GetFrameRate()
    {
        return 1 / (float)framerate;
    }
    void SetData()
    {
        for (int a = 0; a < numLeds; a++)
            ledsData[a] = Color.black;
        foreach (LevelZone levelzone in levelsManager.GetLevelZones())
        {
            int ledID = levelzone.from;
            Color color = levelzone.GetColor();
            int to = levelzone.to;
            int from = levelzone.from;
            if(to>from)
            {
                ColorizeZone(from, to, color);
            }
            else
            {
                ColorizeZone(from, numLeds, color);
                ColorizeZone(0, to, color);
            }
            
        }
        foreach (Character ch in characters)
            ledsData[ch.ledId] = ch.color;
    }
    void ColorizeZone(int from, int to, Color color)
    {
        for (int ledID = from; ledID < to; ledID++)
        {
            if (ledID > ledsData.Count-1) return;
            else if (ledID < 0) return;
            ledsData[ledID] = color;
        }
    }
    void SendData()
    {
        view.OnUpdate(ledsData);
    }
    void CheckCollision()
    {
        int ledID;
        int id = 0;
        foreach (Character character in characters)
        {
            id++;
            character.color = character.originalColor;
            ledID = character.ledId;

            foreach (LevelZone levelzone in levelsManager.GetLevelZones())
            {
                if (levelzone.IsInsideCurve(ledID))
                {
                    Color color = levelzone.GetColor();
                    if (character.originalColor != color)
                    {
                        character.color = Color.white;
                    } else if (character.originalColor == color)
                    {
                        character.color = Color.black;
                    }
                }
            }
        }
    }

}
