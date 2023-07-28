using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class ShooterGame : MonoBehaviour
    {
        List<Character> characters;
        List<Aim> aims;
        int numLeds = 288;
        [SerializeField] CircularView view;
        float framerate = 30;
        List<Color> ledsData;
        InputManager inputs;
        Enemies enemies;
        Shoots shoots;

        void Start()
        {
            enemies = new Enemies();
            enemies.Init(numLeds);

            shoots = new Shoots();
            shoots.Init(numLeds);

            inputs = GetComponent<InputManager>();
            inputs.Init(this);
            characters = new List<Character>();
            for (int a = 0; a < 1; a++)
            {
                Character ch = new Character();
                ch.Init(numLeds, numLeds/2, Color.blue, 3);
                characters.Add(ch);
            }
            aims = new List<Aim>();
            for (int a = 0; a < 1; a++)
            {
                Aim ch = new Aim();
                ch.Init(numLeds, numLeds / 2, Color.white, 3);
                aims.Add(ch);
            }
            view.Init(numLeds);
            ledsData = new List<Color>();
            for (int a = 0; a < numLeds; a++)
                ledsData.Add(Color.black);
            Loop();
        }
        void Loop()
        {
            float deltaTime = Time.deltaTime;
            enemies.OnUpdate(characters[0].ledId, deltaTime);
            enemies.CheckCollision(shoots.all);
            shoots.OnUpdate(deltaTime);
            SetData();
            aims[0].OnUpdate(inputs.speed, deltaTime);
            characters[0].OnUpdate(aims[0].pos, deltaTime);
            CheckCollision();
            SendData();
            Invoke("Loop", deltaTime);//1 / (float)framerate);
        }

        void SetData()
        {
            for (int a = 0; a < numLeds; a++)
                ledsData[a] = Color.black;
            foreach (Explotion e in shoots.all)
                if (e.isOn)
                {
                    foreach (int ledID in e.leds)
                        ledsData[ledID] = e.color;
                }
            foreach (Character ch in characters)
                ledsData[ch.ledId] = ch.color;
            foreach (Aim aim in aims)
                ledsData[aim.ledId] = aim.color;
            foreach (Enemy e in enemies.all)
                if (e.isOn)
                    ledsData[e.ledId] = e.color;
            
        }
        void SendData()
        {
            view.OnUpdate(ledsData);
        }
        void CheckCollision()
        {
           // int ledID;
        }
        public void Shoot()
        {
            shoots.Add(aims[0].ledId);
        }
    }
}