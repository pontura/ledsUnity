using UnityEngine;
using UnityEngine.InputSystem;

public class InputManager : MonoBehaviour
{
    PixelsManager pixelsManager;
    [SerializeField] float value;
    float zeroValue;
    float lastMousePos;
    bool started;

    public types type;
    public enum types
    {
        keyboard,
        joystick
    }

    void Start()
    {
        zeroValue = Input.mousePosition.x;
        pixelsManager = GetComponent<PixelsManager>();
    }

    void Update()
    {
        if (type == types.keyboard) UpdateKeyboard();
        else UpdateJoystick();
    }
    void UpdateKeyboard()
    {
        if (Input.GetMouseButtonDown(0))
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
    void UpdateJoystick()
    {
        value = Input.GetAxis("Horizontal")*100*-1;
        pixelsManager.Move(value);
    }
}
