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

    [SerializeField] float minCurvePossible = 25;//la minima curva posible dentro del random
    [SerializeField] float minCurvePossibleMax = 150;//el maximo de la minima curva posible dentro del random

    [SerializeField] Vector2 randomToCurveDuration = new Vector2(5, 10);

    List<float> limitsList_right;
    List<float> limitsList_left;
    Vector2 limits;
    float distance;
    float carMovement;
    float carPos;

    void Start()
    {
        limitsList_right = new List<float>();
        limitsList_left = new List<float>();
        limits = new Vector2 (0, 0);
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
    void AddLimitRight(float f)
    {
        limitsList_right.Add(f);
        if(limitsList_right.Count > 6)
            limitsList_right.RemoveAt(0);
    }
    void AddLimitLeft(float f)
    {
        limitsList_left.Add(f);
        if (limitsList_left.Count > 6)
            limitsList_left.RemoveAt(0);
    }
    int GetLimit(bool right)
    {
        float total = 0;
        if (right)
        {
            foreach (float a in limitsList_right)
                total += a;
            return (int)Math.Round(total / (float)limitsList_right.Count);
        }  else  {
            foreach (float a in limitsList_left)
                total += a;
            return (int)Math.Round(total / (float)limitsList_left.Count);
        }
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
        int roadPixelID = (int)Mathf.Round((float)roadPoints.Count / roadPixelPercent);
        float road_x = 0;
        int id = totalRoadPoints;
        foreach (RoadPoint rp in roadPoints)
        {
            if (id == roadPixelID)
            {
                color = Color.red;
                alpha = 1;
                road_x = rp.x / center;

            }
            else if (id < roadPixelID)
            {
                color = Color.blue;
                alpha = 1f;
                SetRoadPoint(rp, color, alpha);
            }
            else
            {
                color = Color.white;
                alpha = rp.width/totalPixels;
                SetRoadPoint(rp, color, alpha);
            }

            if (id == roadPixelID)
            {
                AddLimitRight((int)rp.x + (int)(rp.width / 2));
                AddLimitLeft((int)rp.x - (int)(rp.width / 2));
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
        int limit_right = GetLimit(true);
        int limit_left = GetLimit(false);

        SetColor(limit_right, Color.red, 1);
        SetColor(limit_right-1, Color.red, 0.5f);

        float moveByCurve = (road_x - 1) * 20;
        Move(moveByCurve);

        if (road_x < 1)
            SetColor(limit_right + 1, Color.red, 0.75f);
        if (road_x < 0.9)
            SetColor(limit_right + 2, Color.red, 0.75f); 
        if (road_x < 0.8f)
            SetColor(limit_right + 3, Color.red, 0.75f);
        if (road_x < 0.6f)
            SetColor(limit_right + 4, Color.red, 0.75f);

        SetColor(limit_left, Color.red, 1);
        SetColor(limit_left + 1, Color.red, 0.5f);

        if (road_x > 1f)
            SetColor(limit_left - 1, Color.red, 0.75f);
        if (road_x > 1.1)
            SetColor(limit_left - 2, Color.red, 0.75f);
        if (road_x > 1.2f)
            SetColor(limit_left - 3, Color.red, 0.75f);
        if (road_x > 1.4f)
            SetColor(limit_left - 4, Color.red, 0.75f);
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
            if (UnityEngine.Random.Range(0, 10) < 2)
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
        minCurvePossible += 1;
        if(minCurvePossible>minCurvePossibleMax)
            minCurvePossible = minCurvePossibleMax;
        CalculateCurve();
        InitPath();
    }
    float newVanishingPointTarget;
    void CalculateCurve()
    {
        float _newVanishingPointTarget = UnityEngine.Random.Range(-curvePosible, curvePosible);

        if (vanishingPoint + _newVanishingPointTarget > totalPixels - 50) _newVanishingPointTarget = totalPixels - 50;
        else if (vanishingPoint + _newVanishingPointTarget < 50) _newVanishingPointTarget = 50;

        if (Mathf.Abs(newVanishingPointTarget - _newVanishingPointTarget) < minCurvePossible)
            CalculateCurve();
        else
        {
            newVanishingPointTarget = _newVanishingPointTarget;
            vanishingPointTarget = vanishingPoint + newVanishingPointTarget;
        }
    }
    void InitPath()
    {
        if (randomToCurveDuration.x <= 2)
            randomToCurveDuration.x = 2;
        else
            randomToCurveDuration.x -= 0.05f;

        if (randomToCurveDuration.y <= 4)
            randomToCurveDuration.y = 4;
        else
            randomToCurveDuration.y -= 0.025f;

        elapsedTime = 0f;
        curveDuration = UnityEngine.Random.Range(randomToCurveDuration.x, randomToCurveDuration.x);
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
