using UnityEngine;
using UnityEngine.InputSystem;

public class InputManager : MonoBehaviour
{
    PixelsManager pixelsManager;
    [SerializeField] float value;
    float zeroValue;
    float lastMousePos;
    bool started;
    void Start()
    {
        zeroValue = Input.mousePosition.x;
        pixelsManager = GetComponent<PixelsManager>();
    }

    void Update()
    {
        if(Input.GetMouseButtonDown(0))
        {
            started = true;
            value = 0;
            zeroValue = Input.mousePosition.x;
        }
        if (!started) return;
        pixelsManager.Move(value);
        if (lastMousePos == Input.mousePosition.x)
            return;

        lastMousePos = Input.mousePosition.x;
        value = zeroValue - Input.mousePosition.x;
    }
}
