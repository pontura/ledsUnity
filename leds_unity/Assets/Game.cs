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
                ch.Init(numLeds, 0, Color.green, 3);
            characters.Add(ch);
        }
        view.Init(numLeds);
        ledsData = new List<Color>();
        for (int a = 0; a < numLeds; a++)
            ledsData.Add(Color.black);
        levelsManager = new LevelsManager();
        levelsManager.Init(numLeds);
        Loop();
    }
    void Loop()
    {
        SetData();
        levelsManager.OnUpdate();
        characters[0].OnUpdate(inputs.character1_speed);
        characters[1].OnUpdate(inputs.character2_speed);
        CheckCollision();
        SendData();
        Invoke("Loop", 1 / (float)framerate);
    }

    void SetData()
    {
        for (int a = 0; a < numLeds; a++)
            ledsData[a] = Color.black;
        foreach (LevelZone levelzone in levelsManager.all)
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
            if (ledID > ledsData.Count) return;
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
        foreach (Character character in characters)
        {
            character.color = character.originalColor;
            ledID = character.ledId;
            foreach (LevelZone levelzone in levelsManager.all)
            {
                if (levelzone.IsInsideCurve(ledID))
                {
                    Color color = levelzone.GetColor();

                    if (character.color != color)
                    {
                        character.color = Color.white;
                    } else if (character.color == color)
                    {
                        character.color = Color.black;
                    }
                }
            }
        }
    }

}
