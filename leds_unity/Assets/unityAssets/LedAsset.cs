using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LedAsset : MonoBehaviour
{
    [SerializeField] Image image;

    public void Init(float degrees, float offset)
    {
        transform.localEulerAngles = new Vector3(0, 0, degrees);
        image.gameObject.transform.localPosition = new Vector2(0, offset);
    }
    public void UpdateState(Color color)
    {
        image.color = color;
    }
}
