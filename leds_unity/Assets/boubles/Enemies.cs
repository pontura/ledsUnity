using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Enemies
    {
        public List<int> data;
        public List<int> data2;

        int numLeds;

        int bubbleTotalWidth = 8;
        int bubbleWidth = 0;
        int currentColor;
        int currentColor2;
        BoublesGame game;

        public void Init(BoublesGame game, int chararter_width, int numLeds)
        {
            this.game = game;
            data = new List<int>();
            data2 = new List<int>();
            Restart();
            this.numLeds = numLeds;
        }
        public void Restart()
        {
            data.Clear();
            data2.Clear();
        }
        void OnReward(int characterID, int rewards)
        {
            if(characterID == 1)
                game.centerLedID -= rewards;
            else
                game.centerLedID += rewards;
        }
        public void UpdateDraw()
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

            Draw();
        }
        public void CleanLeds()
        {
            int firstMid = game.centerLedID - data2.Count;
            for (int a = game.from; a < firstMid; a++)
                game.ledsData[a] = Color.black;
            int lastMid = game.centerLedID + data.Count;
            for (int a = lastMid; a < game.to; a++)
                game.ledsData[a] = Color.black;
        }
        void Draw()
        {
            int center = game.centerLedID;
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
                if (data.Count>1 && data[data.Count - 1] == color) DestroyLastColor1(color);
                else AddColors(color, characterID);
            } else
            {
                if (data2.Count > 1 && data2[data2.Count - 1] == color) DestroyLastColor2(color);
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
                    from = a + game.centerLedID;
                    if (num == 0)
                        to = a + game.centerLedID;
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
                    to = game.centerLedID - a;
                    if (num == 0)
                        from = game.centerLedID - a;
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
            int newColor = Random.Range(0, game.totalColors);
            if (newColor == currentColor)  SetNewBubble1();
            else currentColor = newColor;
        }
        void SetNewBubble2()
        {
            int newColor = Random.Range(0, game.totalColors);
            if (newColor == currentColor2)   SetNewBubble2();
            else currentColor2 = newColor;
        }
    }

}
