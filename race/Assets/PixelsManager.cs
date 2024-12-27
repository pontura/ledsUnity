using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;

public class PixelsManager : MonoBehaviour
{
    [SerializeField] Pixel pixel_to_add;

    List<Pixel> pixels;
    [SerializeField] Transform container;
    int totalPixels = 300;
    int center;
    [SerializeField] float vanishingPointTarget;
    [SerializeField] float vanishingPoint;
    List<RoadPoint> roadPoints;
    [Serializable]
    class RoadPoint
    {
        public float initial_x;
        public float x;
        public float width;
    }

    float timer;

    [SerializeField] float distance_betweenPoints = 0.3f;
    [SerializeField] float speed = 3;
    [SerializeField] float aceleration = 20;
    float distance;

    void Start()
    {
        center = totalPixels / 2;
        pixels = new List<Pixel>();
        roadPoints = new List<RoadPoint>();
        vanishingPoint = totalPixels / 2;
        for (int i = 0; i < totalPixels; i++)
        {
            Pixel p = Instantiate(pixel_to_add, container);
            pixels.Add(p);
        }
        SetCurve();
    }

    void Update()
    {
        distance += Time.deltaTime;
        timer += Time.deltaTime;

        if (timer > distance_betweenPoints)
            AddRoadPoint();
        UpdateRoadPoints();
        Draw();
        SetVanishingPoint();
    }
    void AddRoadPoint()
    {
        timer = 0;
        RoadPoint rp = new RoadPoint();
        rp.initial_x = vanishingPoint;
        rp.x = rp.initial_x;
        rp.width = 1;
        roadPoints.Add(rp);
    }
    void UpdateRoadPoints()
    {
        RoadPoint toRemove = null;
        int a = 0;
        int totalRoadPoints = roadPoints.Count;
        int half = totalPixels / 2;
        foreach (RoadPoint rp in roadPoints)
        {
            rp.width += speed * Time.deltaTime;
            rp.width *= aceleration;
            rp.x = rp.initial_x + (rp.width * (center - rp.initial_x) / totalPixels);
            a++;
            if (rp.width > totalPixels)
                toRemove = rp;
        }
        if (toRemove != null)
            roadPoints.Remove(toRemove);
    }
    private void Draw()
    {
        float alpha = 0;
        Color color = Color.white;

        for (int a = 0; a < totalPixels; a++)
        {
            SetColor(a, Color.black, 0);
        }
        int totalRoadPoints = roadPoints.Count;
        int roadPixelID = (int)((float)roadPoints.Count / 1.5f);
        int id = totalRoadPoints;
        foreach (RoadPoint rp in roadPoints)
        {
            if (id < roadPixelID)
            {
                color = Color.blue;
                alpha = 1f;
            }
            else if (id == roadPixelID)
            {
                color = Color.red;
                alpha = 1;
            }
            else
            {
                color = Color.white;
                alpha = 1;
            }

            if (id == roadPixelID)
                SetRoadPoint(rp, Color.red, 1, 1);
            else
                SetRoadPoint(rp, color, alpha);

            if (id >= roadPixelID + (roadPixelID / 2))
                SetRoadPoint(rp, Color.white, alpha, 1);
            if (id >= roadPixelID + (roadPixelID / 1.75))
                SetRoadPoint(rp, Color.white, alpha, 2);
            if (id >= roadPixelID + (roadPixelID / 1.5))
                SetRoadPoint(rp, Color.white, alpha, 3);
            if (id >= roadPixelID + (roadPixelID / 1.3f))
                SetRoadPoint(rp, Color.white, alpha, 4);

            id--;
        }

        SetColor((int)vanishingPoint, Color.green, 1);
    }
    void SetColor(int pixel, Color color, float alpha)
    {
        if (pixel < 0) return;
        if (pixel >= pixels.Count) return;

        pixels[pixel].SetData(color, alpha);
    }
    void SetRoadPoint(RoadPoint rp,  Color color, float alpha, int offset = 0)
    {
        int pixel_right = (int)rp.x + (int)(rp.width / 2);
        int pixel_left = (int)rp.x - (int)(rp.width / 2);

        SetColor(pixel_right + offset, color, alpha);
        SetColor(pixel_left - offset, color, alpha);
    }


    float curveDuration;
    private float elapsedTime;
    float curvePosible;
    void SetCurve()
    {
        elapsedTime = 0f;
        curveDuration = UnityEngine.Random.Range(2, 5);
        curvePosible = 10 + distance;
        vanishingPointTarget = vanishingPoint + (int)UnityEngine.Random.Range(-curvePosible, curvePosible);
        if (vanishingPointTarget > totalPixels - 50) 
            vanishingPointTarget = totalPixels - 50;
        else if (vanishingPointTarget < 50)
            vanishingPointTarget = 50;
    }

    void SetVanishingPoint()
    {
        elapsedTime += Time.deltaTime;
        float progress = Mathf.Clamp01(elapsedTime / curveDuration);
        float easedProgress = EaseInOut(progress);
        float currentValue = Mathf.Lerp(vanishingPoint, vanishingPointTarget, easedProgress);

        if (progress >= 1f)
        {
            SetCurve();
        }
        else
        {
            Debug.Log(currentValue + "   curvePosible: " + curvePosible + "  distance: " + distance + " progress:" + progress);
            vanishingPoint = currentValue;
        }
    }
    private float EaseInOut(float t)
    {
        // t es el progreso normalizado entre 0 y 1
        return t < 0.5f
            ? 2f * t * t // EaseIn
            : 1f - Mathf.Pow(-2f * t + 2f, 2f) / 2f; // EaseOut
    }
}
