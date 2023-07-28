using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class Character
    {
        int characterID;
        public int ledId;
        public int width = 6;
        public int color;
        public int color2;
        public float speed;
        public int state;
        float maxSpeed;
        int totalColors;

        public void Init(int characterID, int _ledID, int totalColors)
        {
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
            color2 = Random.Range(0, totalColors);
            if (color2 == color)
                SetSecondaryColor();
        }

    }

}
