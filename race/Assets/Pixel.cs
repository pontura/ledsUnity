using UnityEngine;
using UnityEngine.UI;

public class Pixel : MonoBehaviour
{
    [SerializeField] Image image;
    [SerializeField] Color color = Color.black;

    public void SetData(Color color, float alpha)
    {
        this.color = color;
        this.color.a = alpha;
        image.color = this.color;
    }
    public bool IsAvailable()
    {
        return this.color.a < 0.1f;
    }
}
