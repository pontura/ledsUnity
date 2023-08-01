using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class BoublesGame : MonoBehaviour
    {
        [SerializeField] CircularView view;

        public List<Color> colors;
        public List<Color> ledsData;

        InputManager inputs;
        Enemies enemies;
        Shoots shoots;
        List<Character> characters;
        int numLeds = 288;
        float framerate = 30;

        int chararter_width = 10;
        float delayToAdd;
        float minDelayToAdd;
        float speed;
        float timeToAddColor;
        public int totalColors;
        float seconds = 0;
        float timer = 0;
        public int from = 0;
        public int to = 0;
        public int centerLedID;

        public void Init()
        {
            delayToAdd = 0.5f;
            minDelayToAdd = 0.1f;
            speed = 0.0025f;
            timeToAddColor = 15;
            totalColors = 3;
            seconds = 0;
            timer = 0;
            centerLedID = numLeds / 2;
        }

        void Start()
        {
            Init();
            colors = new List<Color> { Color.green, Color.red, Color.blue, Color.yellow, Color.cyan, Color.magenta, Color.grey };
            enemies = new Enemies();
            enemies.Init(this, chararter_width, numLeds);

            shoots = new Shoots();
            shoots.Init(this, numLeds);

            inputs = GetComponent<InputManager>();
            inputs.Init(this);
            characters = new List<Character>();

            Character ch;
            ch = new Character();
            ch.Init(this, 1, numLeds-1, chararter_width, totalColors);
            characters.Add(ch);
            ch = new Character();
            ch.Init(this, 2, 0, chararter_width, totalColors);
            characters.Add(ch);

            from = chararter_width;
            to = numLeds- chararter_width;

            view.Init(numLeds);
            ledsData = new List<Color>();
            for (int a = 0; a < numLeds; a++)
                ledsData.Add(Color.black);

            Restart();

        }
        void Update()
        {
            float deltaTime = Time.deltaTime;
            OnUpdate(deltaTime);
            characters[0].Draw(numLeds);
            characters[1].Draw(numLeds);
            SendData();
        }        
        public void Shoot(int characterID)
        {
            Character ch = characters[characterID - 1];
            int ledID = ch.ledId;
            if (characterID == 1)
                ledID -= 10;
            else
                ledID += 10;
            shoots.AddBullet(characterID, ledID, ch.color);
            ChangeColors(characterID);
        }
        public void ChangeColors(int characterID)
        {
            characters[characterID-1].ChangeColors();
        }
        void SendData()
        {
            view.OnUpdate(ledsData);
        }
        public void Win(int charaterID)
        {
            Restart();
        }
        public void AddExplotion(int from, int to, int characterID, int color)
        {
            shoots.AddExplotion(from, to, characterID, color);
        }
        public void Restart()
        {
            Init();
            enemies.Restart();
            shoots.Restart();
        }
        void OnUpdate(float deltaTime)
        {
            seconds += deltaTime;
            timer += deltaTime;

            if (timer > delayToAdd)
            {
                if (delayToAdd < minDelayToAdd)
                    delayToAdd = minDelayToAdd;
                else
                    delayToAdd -= speed;

                if (seconds > timeToAddColor)
                {
                    if (totalColors < colors.Count - 1)
                        totalColors++;
                    seconds = 0;
                }
                timer = 0;

                enemies.UpdateDraw();
            }
            enemies.CleanLeds();
            shoots.OnUpdate(centerLedID, enemies.data.Count, enemies.data2.Count, deltaTime);
        }
        public void CollideWith(int color, int characterID)
        {
            enemies.CollideWith(color, characterID);
        }
    }
}