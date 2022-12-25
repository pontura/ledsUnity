using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InputsManager : MonoBehaviour
{
    public float character1_speed;
    public float character2_speed;

    void Update()
    {
        character1_speed = Input.GetAxis("Horizontal1");
        character2_speed = Input.GetAxis("Horizontal2");
    }
}
