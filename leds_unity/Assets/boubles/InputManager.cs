using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Boubles
{
    public class InputManager : MonoBehaviour
    {
        public float speed;
        float lastPos;
        BoublesGame game;

        public void Init(BoublesGame game)
        {
            this.game = game;
        }
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.Q))
                game.Shoot(1);
            if (Input.GetKeyDown(KeyCode.W))
                game.ChangeColors(1);

            if (Input.GetKeyDown(KeyCode.P))
                game.Shoot(2);
            if (Input.GetKeyDown(KeyCode.O))
                game.ChangeColors(2);
        }
    }
}
