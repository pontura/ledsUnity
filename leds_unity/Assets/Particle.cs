using UnityEngine;
using System.Collections;

public class Particle : MonoBehaviour
{
    public int ledID;
    public float value;
    public float speed;
    public float direction;

    public void Init(int _ledID)
    {
        this.value = 255;
        this.ledID = _ledID;
    }
    public void SetSpeed(float _speed, float _direction)
    {
        this.direction = _direction;
        this.speed = _speed;
    }
    public void OnUpdate(float deltaTime, float _speed_to_fade)
    {
        if (this.value == 0) return;
        this.value = this.value - (_speed_to_fade * deltaTime);
        if (this.value < 0) value = 0;
    }
    public bool IsAvailable()
    {
        return value == 0;
    }
}
