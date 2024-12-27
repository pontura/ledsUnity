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
    [SerializeField]float  roadPixelPercent = 1.6f;
    float timer;

    [SerializeField] float distance_betweenPoints = 0.3f;
    [SerializeField] float speed = 3;
    [SerializeField] float aceleration = 20;
    float distance;
    float carMovement;
    float carPos;

    void Start()
    {
        center = totalPixels / 2;
        carMovement = 0;
        carPos = center;
        pixels = new List<Pixel>();
        roadPoints = new List<RoadPoint>();
        vanishingPoint = totalPixels / 2;
        for (int i = 0; i < totalPixels; i++)
        {
            Pixel p = Instantiate(pixel_to_add, container);
            pixels.Add(p);
        }
        SetNextPath();
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
        SetCar();
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
    RoadPoint activeRoadPoint;
    int roadPointDraws;
    private void Draw()
    {

        float alpha = 0;
        Color color = Color.white;

        for (int a = 0; a < totalPixels; a++)
        {
            SetColor(a, Color.black, 0);
        }
        int totalRoadPoints = roadPoints.Count;
        int roadPixelID = (int)Mathf.Round((float)roadPoints.Count / roadPixelPercent);
        int id = totalRoadPoints;
        foreach (RoadPoint rp in roadPoints)
        {
            if (id == roadPixelID)
            {
                if(rp != activeRoadPoint)
                {
                    activeRoadPoint = rp;
                    roadPointDraws = 0;
                }
                else
                {
                    roadPointDraws++;
                    print(roadPointDraws);
                }
                color = Color.red;
                alpha = 1;
            }
            else if (id < roadPixelID)
            {
                color = Color.blue;
                alpha = 1f;
            }
            else
            {
                color = Color.white;
                alpha = rp.width/totalPixels;
            }
            SetRoadPoint(rp, color, alpha);

            if (id == roadPixelID)
            {
                for (int a = 0; a < 9-roadPointDraws; a++)
                {
                    SetRoadPoint(rp, Color.red, 1, a);
                }
                for (int a = 0;a < roadPointDraws; a++)
                {
                    SetRoadPoint(rp, Color.red, 1, a * -1);
                }
                SetRoadPoint(rp, Color.red, 1);
            }
            else
            {

                if (id >= roadPixelID + (roadPixelID / 2))
                    SetRoadPoint(rp, Color.white, alpha, 1);
                if (id >= roadPixelID + (roadPixelID / 1.75))
                    SetRoadPoint(rp, Color.white, alpha, 2);
                if (id >= roadPixelID + (roadPixelID / 1.5))
                    SetRoadPoint(rp, Color.white, alpha, 3);
                if (id >= roadPixelID + (roadPixelID / 1.3f))
                    SetRoadPoint(rp, Color.white, alpha, 4);
            }

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
    void SetRoadPoint(RoadPoint rp, Color color, float alpha, int offset = 0)
    {
        int pixel_right = (int)rp.x + (int)(rp.width / 2);
        int pixel_left = (int)rp.x - (int)(rp.width / 2);

        SetColor(pixel_right + offset, color, alpha);
        SetColor(pixel_left - offset, color, alpha);
    }


    float curveDuration;
    private float elapsedTime;
    float curvePosible;
    void SetNextPath()
    {
        if(distance<10)
            StayStraight();
        else  if (vanishingPointTarget == center)
        {
            if (UnityEngine.Random.Range(0, 10) < 2)
                StayStraight();
            else
                CurveRandom();
        }
        else
        {
            if (UnityEngine.Random.Range(0, 10) < 4)
                GotoCenter();
            else
                CurveRandom();
        }
    }
    void GotoCenter()
    {
        vanishingPointTarget = center;
        InitPath();
    }
    void StayStraight()
    {
        vanishingPointTarget = center;
        InitPath();
    }
    void CurveRandom() {
        curvePosible = 50 + distance;
        vanishingPointTarget = vanishingPoint + (int)UnityEngine.Random.Range(-curvePosible, curvePosible);
        InitPath();
    }
    void InitPath()
    {
        if (vanishingPointTarget > totalPixels - 50) vanishingPointTarget = totalPixels - 50;
        else if (vanishingPointTarget < 50) vanishingPointTarget = 50;

        elapsedTime = 0f;
        curveDuration = UnityEngine.Random.Range(3, 10);
    }
    void SetVanishingPoint()
    {
        elapsedTime += Time.deltaTime;
        float progress = Mathf.Clamp01(elapsedTime / curveDuration);
        float easedProgress = EaseInOut(progress);
        float currentValue = Mathf.Lerp(vanishingPoint, vanishingPointTarget, easedProgress);

        if (progress >= 1f)
        {
            SetNextPath();
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
    float carSpeed = 1;
    public void Move(float value)
    {
        carPos -= carSpeed * value * Time.deltaTime;
    }
    void SetCar()
    {
        SetColor((int)carPos-1, Color.yellow, 1);
        SetColor((int)carPos+1, Color.yellow, 1);
    }
}
