using System;
using System.Collections.Generic;
using UnityEngine;

public class PixelsManager : MonoBehaviour
{
    [SerializeField] Pixel pixel_to_add;

    List<Pixel> pixels;
    [SerializeField] Transform container;
    int totalPixels = 300;
    [SerializeField] int center;
    [SerializeField] int curve;
    List<RoadPoint> roadPoints;
    [Serializable] class RoadPoint
    {
        public float z;
    }

    float timer;

    [SerializeField] float distance_betweenPoints = 0.3f;
    [SerializeField] float speed = 3;
    [SerializeField] float roadWidth = 20;
    [SerializeField] float aceleration = 20;

    void Start()
    {
        pixels = new List<Pixel>();
        roadPoints = new List<RoadPoint>();
        center = totalPixels / 2;
        for (int i = 0; i < totalPixels; i++)
        {
            Pixel p = Instantiate(pixel_to_add, container);
            pixels.Add(p);
        }
    }
    void Update()
    {
        timer += Time.deltaTime;
        if (timer > distance_betweenPoints)
            AddRoadPoint();
        UpdateRoadPoints();
        Draw();
    }
    void AddRoadPoint()
    {
        timer = 0;
        RoadPoint rp = new RoadPoint();
        rp.z = 100;
        roadPoints.Add(rp);
    }
    void UpdateRoadPoints()
    {
        RoadPoint toRemove = null;
        foreach (RoadPoint rp in roadPoints)
        {
            rp.z -= Time.deltaTime * speed;
            float _aceleration = (100-rp.z) / aceleration;
            rp.z -= _aceleration;
            if (rp.z < 0)
                toRemove = rp;
        }
        if(toRemove != null) 
            roadPoints.Remove(toRemove);
    }
    private void Draw()
    {
        int p = center;
        float alpha = 0;
        Color color = Color.white;
        for (int a = center; a < totalPixels; a++) {

            Pixel pixel = pixels[a];
            
            if (IsBorder(p))
                SetColor(p, Color.red, 1);
            else
                SetColor(p, Color.black, 0);
            p++;
        }

        SetColor(center, Color.blue, 1);
        foreach (RoadPoint rp in roadPoints)
        {
            int pixel = (int)(rp.z * (center) / 100);

            pixel = pixel + (int)(rp.z * (float)curve);

             pixel = (center - pixel) + center;

            int limit = center + (int)roadWidth;
           
            if (pixel < center + roadWidth)
            {
                color = Color.blue;
                alpha = 0.6f;
                // alpha = ((pixel - center) / roadWidth) / 1.2f;
            }
            else
            {
                color = Color.white;
                alpha = 1;
            }


            if (pixel == limit)
            {
                SetColor(pixel + 1, Color.red, 1);
                SetColor(pixel + 2, Color.red, 1);
                SetColor(pixel + 3, Color.red, 1);
            }
            else
                SetColor(pixel, color, 0.5f);

            //150 + ((300 - 150) / 1)

            if (pixel >= center + (totalPixels - center) /2)
            {
                SetColor(pixel + 1, Color.white, alpha);
            }
            if (pixel >= center + (totalPixels - center) / 1.75)
            {
                SetColor(pixel + 2, Color.white, alpha);
            }
            if (pixel >= center + (totalPixels - center) / 1.5)
            {
                SetColor(pixel + 3, Color.white, alpha);
            }
            if (pixel >= center + (totalPixels - center) / 1.3f)
            {
                SetColor(pixel + 4, Color.white, alpha);
            }
        }
    }
    bool IsBorder(int p)
    {
        if (p == center - (int)roadWidth - 1)
            return true;
        else if (p == center + (int)roadWidth + 1)
            return true;
        return false;
    }
    void Mirrored(int _pixel, Color color, float alpha)
    {
        int pixel = center - (_pixel - center);
        if (pixel < 0) return;
        pixels[pixel].SetData(color, alpha);
    }
    void SetColor(int pixel, Color color, float alpha)
    {
        if (pixel < 0) return;
        if (pixel >= pixels.Count) return;

       

        pixels[pixel].SetData(color, alpha);
      //  Mirrored(pixel, color, alpha);
    }
}
