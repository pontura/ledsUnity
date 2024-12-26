using UnityEngine;
using UnityEngine.UI;

public class Pixel : MonoBehaviour
{
    [SerializeField] Image image;
    [SerializeField] Color color = Color.white;
    public void SetData(Color color, float alpha)
    {
        color.a = alpha;
        image.color = color;
    }
}
