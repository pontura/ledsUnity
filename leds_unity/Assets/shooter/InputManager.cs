using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Shooter
{
    public class InputManager : MonoBehaviour
    {
        public float speed;
        float lastPos;
        ShooterGame shooterGame;

        public void Init(ShooterGame shooterGame)
        {
            this.shooterGame = shooterGame;
        }
        void Update()
        {
            speed = lastPos - Input.mousePosition.x;
            speed /= 5;
            lastPos = Input.mousePosition.x;
            if (Input.GetKeyDown(KeyCode.Space))
                shooterGame.Shoot();
        }
    }
}
