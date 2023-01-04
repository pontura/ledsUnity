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
    List<Explotion> explotions;

    void Start()
    {
        explotions = new List<Explotion>();
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
        //Invoke("AddExplotion", 5);
    }
    float deltaTime;
    void Update()
    {
        deltaTime = Time.deltaTime;
        SetData();
        levelsManager.OnUpdate(deltaTime);
        characters[0].OnUpdate(inputs.character1_speed, deltaTime);
        characters[1].OnUpdate(inputs.character2_speed, deltaTime);
        CheckCollision();
        SendData();
        if (Input.GetKeyDown(KeyCode.P))
            AddExplotion(characters[0].ledId);

      //  Invoke("Loop", GetFrameRate());
    }
    public float GetFrameRate()
    {
        return Time.deltaTime;
       // return 1 / (float)framerate;
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
            else if (to != from)
            {
                ColorizeZone(from, numLeds, color);
                ColorizeZone(0, to, color);
            }
            
        }
        foreach (Character character in characters)
        {
            ledsData[character.ledId] = character.color;
            Color c = character.color;
            foreach (Particle particle in character.trail.all)
            {
                if (particle.value > 0 && particle.ledID != character.ledId)
                {
                    c.a = particle.value / 255;
                    ledsData[particle.ledID] = c;
                }
            } 
        }
        foreach (Explotion explotion in explotions)
        {
            if (explotion.on)
            {
                Color c = Color.red;
                explotion.OnUpdate(deltaTime, 500);
                foreach (Particle particle in explotion.all)
                {
                    c.a = particle.value / 255;
                    ledsData[particle.ledID] = c;
                }
            }
        }
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
    void AddExplotion(int _ledId)
    {
        Debug.Log("AddExplotion " + _ledId);
        foreach (Explotion e in explotions)
        {
            if (!e.on)
            {
                Debug.Log("Explotion Restart from pool");
                e.Init(_ledId);
                return;
            }
        }
        Debug.Log("New Explotion!");
        Explotion explotion = new Explotion();
        explotion.Init(numLeds, _ledId, 50);
        explotions.Add(explotion);
    }

}
