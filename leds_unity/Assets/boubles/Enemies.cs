using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Enemies
    {
        public List<int> data;
        public List<int> data2;

        public int centerLedID;
        int numLeds;
        int totalColors;
        float delayToAdd = 3;
        float speed = 0.4f;
        int bubbleTotalWidth = 8;
        int bubbleWidth = 0;
        int currentColor;
        int currentColor2;
        BoublesGame game;
        int from, to = 0;

        public void Init(BoublesGame game, int totalColors, int chararter_width, int numLeds)
        {
            from = chararter_width;
            to = numLeds - chararter_width;
            this.game = game;
            data = new List<int>();
            data2 = new List<int>();

            this.totalColors = totalColors;
            this.numLeds = numLeds;

            Center();
        }
        public void Restart()
        {
            Center();
            data.Clear();
            data2.Clear();
        }
        void Center()
        {
            this.centerLedID = numLeds / 2;
        }
        void OnReward(int characterID, int rewards)
        {
            if(characterID == 1)
                this.centerLedID -= rewards;
            else
                this.centerLedID += rewards;
            Debug.Log("center: " + centerLedID);
        }
        float timer = 0;
        public void OnUpdate(float deltaTime)
        {
            timer += deltaTime;

            if (timer > speed)
            {
                if (bubbleWidth >= bubbleTotalWidth)
                {
                    SetNewBubble1();
                    SetNewBubble2();
                    bubbleWidth = 0;
                }
                
                DestroyLine();

                AddLine();
                AddLine();

                bubbleWidth++;
                timer = 0;

                Draw();
            }
            CleanLeds();
        }
        void CleanLeds()
        {
            int firstMid = centerLedID - data2.Count;
            for (int a = from; a < firstMid; a++)
                game.ledsData[a] = Color.black;
            int lastMid = centerLedID + data.Count;
            for (int a = lastMid; a < to; a++)
                game.ledsData[a] = Color.black;
        }
        void Draw()
        {

            int center = centerLedID;
            int ledId = 0;

           

            foreach (int colorID in data)
            {
                int ledID = ledId + center;
                if (ledID > numLeds - 5)
                {
                    game.Win(2);
                    return;
                }
                game.ledsData[ledID] = game.colors[colorID];
                ledId++;
            }
            ledId = 0;
            foreach (int colorID in data2)
            {
                int ledID = center - ledId;
                if (ledID < 5)
                {
                    game.Win(1);
                    return;
                }
                game.ledsData[ledID] = game.colors[colorID];
                ledId++;
            }
        }
        void DestroyLine()
        {
            if(data.Count>0)
                data.RemoveAt(data.Count-1);
            if (data2.Count > 0)
                data2.RemoveAt(data2.Count - 1);
        }
       
        void AddLine()
        {
            data.Insert(0, currentColor);
            data2.Insert(0, currentColor2);
        }
        public void CollideWith(int color, int characterID)
        {
            if (characterID == 1)
            {
                if (data[data.Count - 1] == color) DestroyLastColor1(color);
                else AddColors(color, characterID);
            } else
            {
                if (data2[data2.Count - 1] == color) DestroyLastColor2(color);
                else AddColors(color, characterID);
            }
        }   
        void DestroyLastColor1(int color)
        {
            int from = 0;
            int to = 0;
            int num = 0;
            for(int a = data.Count-1; a>0; a--)
            {
                if (data[a] == color)
                {
                    data.RemoveAt(data.Count - 1);
                    from = a + centerLedID;
                    if (num == 0)
                        to = a + centerLedID;
                    num++;
                }
                else
                {
                    if (from != 0 && to != 0)
                    {
                        game.AddExplotion(from, to, 1, color);
                        OnReward(1, 2);
                    }
                    return;
                }
            }
            Draw();
        }
        void DestroyLastColor2(int color)
        {
            int from = 0;
            int to = 0;
            int num = 0;
            for (int a = data2.Count - 1; a > 0; a--)
            {
                if (data2[a] == color)
                {
                    data2.RemoveAt(data2.Count - 1);
                    to = centerLedID - a;
                    if (num == 0)
                        from = centerLedID - a;
                    num++;
                }
                else {
                    if (from != 0 && to != 0)
                    {
                        game.AddExplotion(from, to, 2, color);
                        OnReward(2, 2);
                    }
                    return;
                }
            }
            Draw();
        }
        void AddColors(int color, int characterID)
        {
            for (int a = 0; a < bubbleTotalWidth; a++)
            {
                if(characterID == 1)
                    data.Add(color); 
                else
                    data2.Add(color);
            }
            Draw();
        }


        void SetNewBubble1()
        {
            int newColor = Random.Range(0, totalColors);
            if (newColor == currentColor)  SetNewBubble1();
            else currentColor = newColor;
        }
        void SetNewBubble2()
        {
            int newColor = Random.Range(0, totalColors);
            if (newColor == currentColor2)   SetNewBubble2();
            else currentColor2 = newColor;
        }
    }

}
