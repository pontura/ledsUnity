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
    ExplotionsManager explotionsManager;

    void Start()
    {
        explotionsManager = new ExplotionsManager();
        explotionsManager.Init(numLeds);
        inputs = GetComponent<InputsManager>();
        characters = new List<Character>();
        for (int a = 0; a < 2; a++)
        {
            Character ch = new Character();
            if (a == 0)
                ch.Init(numLeds, 0, Color.blue, 2);
            else
                ch.Init(numLeds, numLeds/2, Color.green, 2);
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
        {
            Character character = characters[0];
            StartCoroutine(explotionsManager.AddExplotionDouble(character.ledId, character.color, 0.1f) );
        }
    }
    public float GetFrameRate()
    {
        return Time.deltaTime;
       // return 1 / (float)framerate;
    }
    bool boolValue;
    void SetData()
    {
        boolValue = !boolValue;
        for (int a = 0; a < numLeds; a++)
            ledsData[a] = Color.black;
        foreach (LevelZone levelzone in levelsManager.GetLevelZones())
        {
            int ledID = levelzone.from;
            Color color = levelzone.GetColor();
            int to = levelzone.to;
            int from = levelzone.from;
            string status = levelzone.status;
            if (to>from)
            {
                ColorizeZone(from, to, color, status);
            }
            else if (to != from)
            {
                ColorizeZone(from, numLeds, color, status);
                ColorizeZone(0, to, color, status);
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
        foreach (Explotion explotion in explotionsManager.GetExplotions())
        {
            if (explotion.on)
            {
                Color c = explotion.color;
                explotion.OnUpdate(deltaTime);
                foreach (Particle particle in explotion.all)
                {
                    c.a = particle.value / 255;
                    ledsData[particle.ledID] = c;
                }
            }
        }
    }
    
    void ColorizeZone(int from, int to, Color color, string status)
    {
        for (int ledID = from; ledID < to; ledID++)
        {
            if (ledID > ledsData.Count-1) return;
            else if (ledID < 0) return;
            if (status == "safe")
            {
                bool isPair = (ledID % 2 == 0);
                if (boolValue == isPair) color.a = 0.4f; else color.a = 0.2f;
            }
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

            //foreach (LevelZone levelzone in levelsManager.GetLevelZones())
            //{
            //    if (levelzone.IsInsideCurve(ledID))
            //    {
            //        Color color = levelzone.GetColor();
            //        if (character.originalColor != color)
            //        {
            //            character.color = Color.white;
            //        } else if (character.originalColor == color)
            //        {
            //            character.color = Color.black;
            //        }
            //    }
            //}
        }
    }
}
