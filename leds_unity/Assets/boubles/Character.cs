using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Character
    {
        int characterID;
        public int ledId;
        int width;
        public int color;
        public int color2;
        public float speed;
        public int state;           
        float maxSpeed;
        int totalColors;
        BoublesGame game;

        public void Init(BoublesGame game, int characterID, int _ledID, int width, int totalColors)
        {
            this.width = width;
            this.game = game;
            this.characterID = characterID;
            state = 1;
            this.ledId = _ledID;
            this.totalColors = totalColors;
            color = Random.Range(0, totalColors);
            SetSecondaryColor();
        }
        public void ChangeColors()
        {
            color = color2; 
            SetSecondaryColor();
        }
        void SetSecondaryColor()
        {
            color2 = Random.Range(0, game.totalColors);
            if (color2 == color)
                SetSecondaryColor();
        }
        public void Draw(int numLeds)
        {
            if(characterID ==1)
            {
                for (int a = numLeds - 1; a > numLeds - 1- width; a--)
                {
                    if (a > numLeds -1- (width / 2)) game.ledsData[a] = game.colors[color2];
                    else game.ledsData[a] = game.colors[color];
                }
            }
           else
            {
                for (int a = 0; a < width; a++)
                {
                    if (a > (width / 2)) game.ledsData[a] = game.colors[color];
                    else game.ledsData[a] = game.colors[color2];
                }
            }
              
        }

    }

}
