using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Xcalectric : MonoBehaviour
{
    List<Character> characters;
    Curves curves;
    int numLeds = 300;
    [SerializeField] CircularView view;
    float framerate = 30;
    List<Color> ledsData;
    InputsManager inputs;

    void Start()    
    {
        inputs = GetComponent< InputsManager>();
        characters = new List<Character>();
        for (int a = 0; a<2; a++)
        {
            Character ch = new Character();
            if(a == 0)
                ch.Init(numLeds, 0, Color.blue, 3);
            else
                ch.Init(numLeds, 0, Color.green, 3);
            characters.Add(ch);
        }
        view.Init(numLeds);
        ledsData = new List<Color>();
        for (int a = 0; a < numLeds; a++)
            ledsData.Add(Color.black);
        curves = new Curves();
        curves.Init();
        Loop();
    }
    void Loop()
    {
        float deltaTime = Time.deltaTime;
        SetData();
        characters[0].OnUpdate(inputs.character1_speed, deltaTime);
        characters[1].OnUpdate(inputs.character2_speed, deltaTime);
        CheckCollision();
        SendData();
        Invoke("Loop", 1 / (float)framerate);
    }

    void SetData()
    {
        for (int a = 0; a < numLeds; a++)
            ledsData[a] = Color.black;
        foreach (Curve curve in curves.all)
        {
            int ledID = curve.from;
            foreach (float value in curve.values)
            {
                Color color = new Color(value + 0.1f, 0, 0);
                ledsData[ledID] = color;
                ledID++;
            }
        }
        foreach (Character ch in characters)
            ledsData[ch.ledId] = ch.color;
    }
    void SendData()
    {
        view.OnUpdate(ledsData);
    }
    void CheckCollision()
    {
        int ledID;
        foreach(Character character in characters)
        {
            float curveSpeedChecker = Mathf.Abs(character.speed / 4);
            if (curveSpeedChecker > 0.1f)
            {
                ledID = character.ledId;
                foreach (Curve curve in curves.all)
                {
                    if (curve.IsInsideCurve(ledID))
                    {
                        float curveValue = curve.GetValue(ledID);

                       // Debug.Log("curveValue " + (1-curveValue) + "   curveSpeedChecker " + curveSpeedChecker);
                        if (curveSpeedChecker > 1-curveValue)
                        {
                            character.InDangerZone();
                            return;
                        }
                        else
                        {
                            if (character.state == 2)
                                character.OutOfDanger();
                        }
                    }
                }
            }
        }
    }

}
