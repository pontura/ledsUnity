using UnityEngine;
using System.Collections;

public class Particle : MonoBehaviour
{
    public int ledID;
    public float value;
    public float speed;
    public float direction;

    public void Init(int _ledID, int initialAlpha)
    {
        this.value = initialAlpha;
        this.ledID = _ledID;
    }
    public void SetSpeed(float _speed, float _direction)
    {
        this.direction = _direction;
        this.speed = _speed;
    }
    public void OnUpdate(float deltaTime, float fade_desaceleration)
    {
        if (this.value == 0) return;
        this.value = this.value - (fade_desaceleration * deltaTime);
        if (this.value < 0) value = 0;
    }
    public bool IsAvailable()
    {
        return value == 0;
    }
}
