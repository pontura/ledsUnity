using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class BoublesGame : MonoBehaviour
    {
        List<Character> characters;
        int numLeds = 288;
        [SerializeField] CircularView view;
        float framerate = 30;
        public List<Color> ledsData;
        InputManager inputs;
        public Enemies enemies;
        Shoots shoots;
        public List<Color> colors;

        int chararter_width = 10;

        void Start()
        {
            colors = new List<Color> { Color.green, Color.red, Color.blue, Color.yellow, Color.cyan };
            enemies = new Enemies();
            enemies.Init(this, colors.Count, chararter_width, numLeds);

            shoots = new Shoots();
            shoots.Init(this, numLeds);

            inputs = GetComponent<InputManager>();
            inputs.Init(this);
            characters = new List<Character>();

            Character ch;
            ch = new Character();
            ch.Init(this, 1, numLeds-1, chararter_width, colors.Count);
            characters.Add(ch);
            ch = new Character();
            ch.Init(this, 2, 0, chararter_width, colors.Count);
            characters.Add(ch);

            view.Init(numLeds);
            ledsData = new List<Color>();
            for (int a = 0; a < numLeds; a++)
                ledsData.Add(Color.black);
        }
        void Update()
        {
            float deltaTime = Time.deltaTime;
            enemies.OnUpdate(deltaTime);
            shoots.OnUpdate(deltaTime);
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
            enemies.Restart();
            shoots.Restart();
        }
        public void AddExplotion(int from, int to, int characterID, int color)
        {
            shoots.AddExplotion(from, to, characterID, color);
        }
    }
}