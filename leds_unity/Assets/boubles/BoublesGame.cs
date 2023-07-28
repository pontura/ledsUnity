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
        List<Color> ledsData;
        InputManager inputs;
        Enemies enemies;
        Shoots shoots;
        List<Color> colors;

        void Start()
        {
            colors = new List<Color> { Color.green, Color.red, Color.blue, Color.yellow, Color.cyan };
            enemies = new Enemies();
            enemies.Init(this, colors.Count, numLeds);

            shoots = new Shoots();
            shoots.Init(numLeds);

            inputs = GetComponent<InputManager>();
            inputs.Init(this);
            characters = new List<Character>();

            Character ch;
            ch = new Character();
            ch.Init(1, numLeds-1, colors.Count);
            characters.Add(ch);
            ch = new Character();
            ch.Init(2, 0, colors.Count);
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
            SetData();
            SendData();
        }

        void SetData()
        {
            for (int a = 0; a < numLeds; a++)
                ledsData[a] = Color.black;


            //Characters
            int center = enemies.centerLedID;
            int ledId = 0;
           
            foreach (int colorID in enemies.data)
            {
                int ledID = ledId + center;
                if (ledID > numLeds - 5)
                {
                    Win(2);
                    return;
                }
                ledsData[ledID] = colors[colorID];
                ledId++;
            }
            ledId = 0;
            foreach (int colorID in enemies.data2)
            {
                int ledID = center - ledId;
                if (ledID < 5)
                {
                    Win(1);
                    return;
                }
                ledsData[ledID] = colors[colorID];
                ledId++;
            }


            //Characters Signals
            Character ch = characters[0];
            for (int a = numLeds - 1; a > numLeds - ch.width; a--)
            {
                if(a>numLeds - 1- (ch.width/2)) ledsData[a] = colors[ch.color2];
                else  ledsData[a] = colors[ch.color];
            }
            ch = characters[1];
            for (int a = 0; a < ch.width; a++)
            {
                if (a > (ch.width / 2)) ledsData[a] = colors[ch.color];
                else ledsData[a] = colors[ch.color2];
            }


            //Bullets
            ledId = 0;
            foreach (Bullet b in shoots.bullets)
            {
                if (b.isOn)
                {
                    foreach (int l in b.leds)
                    {
                        if ((b.characterID == 1 && ledId == 0 && l <= enemies.data.Count + center) ||
                            (b.characterID == 2 && ledId == 0 && l >= center-enemies.data2.Count)
                            )
                        {
                            enemies.CollideWith(b.color, b.characterID);
                            b.Collide();
                            return;
                        }
                        ledsData[l] = colors[b.color];
                    }
                    ledId++;
                }
            }

            foreach (ExplotionParticle a in shoots.explotions)
                if (a.isOn)
                    ledsData[a.ledId] = new Color(1, 1, 1, a.alpha);


            ledsData[enemies.centerLedID] = Color.black;
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

        void Win(int charaterID)
        {
            enemies.Restart();
            shoots.Restart();
        }
        public void AddExplotion(int from, int to, int characterID)
        {
            shoots.AddExplotion(from, to, characterID);
        }
    }
}