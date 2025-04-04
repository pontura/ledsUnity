using System;
using System.Collections.Generic;
using UnityEngine;

public class PixelsManager : MonoBehaviour
{
    [SerializeField] Pixel pixel_to_add;
    const int FRAMERATE = 60;

    int state = -1; //0 = playing 1=die;

    List<Pixel> pixels;
    [SerializeField] Transform container;

    //cars
    float initCarsIn = 5; // seconds
    [SerializeField] Vector2 carsRandomLimits = new Vector2(1,5);
    Vector2 carsRandom = new Vector2(0, 0);
    Vector2 minCarsRandom = new Vector2(0.2f, 0.75f);
    float carsRandomDisminutionSubstraction = 0.05f; //cuanto resta por iteracion

    float carPassed = 0;
    int totalPixels = 300;
    int center;
    List<RoadPoint> roadPoints;

    float limitsList_right;
    float limitsList_left;

    float limitsList_right_goto;
    float limitsList_left_goto;

    Vector2 limits;
    float distance;
    float carMovement;
    float carPos;

    int limit_right;
    int limit_left;


    [SerializeField] float vanishingPointTarget;
    [SerializeField] float vanishingPoint;
    [SerializeField] float roadPixelWidth;
    [SerializeField] Vector2 roadPixelWidthLimits = new Vector2(200, 60);
    [SerializeField] float roadPixelWidthDecrease = 1;
    float timer;

    [SerializeField] float distance_betweenPoints = 0.3f;

    [SerializeField] float speed;
    [SerializeField] float aceleration;

    [SerializeField] float speedInrease = 1;
    [SerializeField] Vector2 speedLimits = new Vector2(10, 20);
    [SerializeField] Vector2 acelerationLimits = new Vector2(1.02f, 1.04f);

    [SerializeField] float minCurvePossible = 25;//la minima curva posible dentro del random
    [SerializeField] float minCurvePossibleMax = 150;//el maximo de la minima curva posible dentro del random

    [SerializeField] Vector2 randomToCurveDuration = new Vector2(5, 10);


    [Serializable]
    class RoadPoint
    {
        float roadPixelWidth;
        float alphaValue = 0.25f;
        public float initial_x;
        public float x;
        public float width;
        public float car_x;
        public bool InPosition()
        {
            return width > roadPixelWidth;
        }
        public void UpdateCar()
        {
            if (alphaValue == 0.25f)
                alphaValue = 0.75f;
            else if (alphaValue == 0.75f)
                alphaValue = 0.25f;
        }
        public float Alpha()
        {
            if (width > roadPixelWidth - 30)
                return 1;
            else if (width > roadPixelWidth - 60)
                return 0.7f;
            else if (width > roadPixelWidth - 100)
                return 0.5f;
            else
                return alphaValue;
        }
        public void AddCar(float roadPixelWidth)
        {
            this.roadPixelWidth = roadPixelWidth;
            car_x = UnityEngine.Random.Range(0.1f, 0.9f);
        }
        public void SetOff()
        {
            car_x = 0;
        }
    }

    void Start()
    {
        roadPoints = new List<RoadPoint>();
        Application.targetFrameRate = FRAMERATE;
        center = totalPixels / 2;

        pixels = new List<Pixel>();
        for (int i = 0; i < totalPixels; i++)
        {
            Pixel p = Instantiate(pixel_to_add, container);
            pixels.Add(p);
        }
        Restart();
    }
    void Restart()
    {
        carsRandom = carsRandomLimits;
        state = 0;
        roadPixelWidth = roadPixelWidthLimits.x;
        timer = 0;
        distance = 0;
        limits = new Vector2(0, totalPixels);
        speed = speedLimits.x;
        aceleration = acelerationLimits.x; 
        carPos = center;
        carMovement = 0;
        roadPoints.Clear();
        vanishingPoint = center;

        CancelInvoke();
        SetNextPath();
        Invoke("AddCar", initCarsIn);
    }
    void Update()
    {
        if (state == 1)
            UpdateCrash();
        else
            UpdatePlaying();
    }
    
    void UpdatePlaying()
    {
        distance += Time.deltaTime;
        timer += Time.deltaTime;
        if (timer > distance_betweenPoints)
            AddRoadPoint();
        UpdateRoadPoints();
        Draw();
        SetVanishingPoint();
        if (roadPixelWidth <= roadPixelWidthLimits.y)
            roadPixelWidth = roadPixelWidthLimits.y;
        else
            roadPixelWidth -= roadPixelWidthDecrease * Time.deltaTime;
        if(speed>=speedLimits.y)
            speed = speedLimits.y;
        speed += (speedInrease * Time.deltaTime)/10;
        if (aceleration >= acelerationLimits.y)
            aceleration = acelerationLimits.y;
        aceleration += (speedInrease * Time.deltaTime) / 1000;
    }
    void AddCar()
    {
        roadPoints[roadPoints.Count - 1].AddCar(roadPixelWidth);
        Invoke("AddCar", UnityEngine.Random.Range(carsRandom.x, carsRandom.y));

        if (carsRandom.x <= minCarsRandom.x) 
            carsRandom.x = minCarsRandom.x;
        else
            carsRandom.x -= carsRandomDisminutionSubstraction;

        if (carsRandom.y <= minCarsRandom.y)
            carsRandom.y = minCarsRandom.y;
        else
            carsRandom.y -= carsRandomDisminutionSubstraction;

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
        int totalRoadPoints = roadPoints.Count;
        int half = totalPixels / 2;
        foreach (RoadPoint rp in roadPoints)
        {
            rp.width += speed * Time.deltaTime;
            rp.width *= aceleration;
            rp.x = rp.initial_x + (rp.width * (center - rp.initial_x) / totalPixels);
            if (rp.width > totalPixels)
                toRemove = rp;
        }
        if (toRemove != null)
            roadPoints.Remove(toRemove);
    }
    void AddLimitRight(float f)
    {
        limitsList_right_goto = f;
    }
    void AddLimitLeft(float f)
    {
        limitsList_left_goto = f;
    }
    int GetLimit(bool right)
    {
        float total = 0;
        if (right)
        {
            limitsList_right = Mathf.Lerp(limitsList_right, limitsList_right_goto, 0.1f);
            return (int)limitsList_right;
        }  else
        {
            limitsList_left = Mathf.Lerp(limitsList_left, limitsList_left_goto, 0.1f);
            return (int)limitsList_left;
        }
    }
    int lastRightKeyframe;
    void SetAllPixelsTo(Color color, float alpha)
    {
        for (int a = 0; a < totalPixels; a++)
        {
            SetColor(a, color, alpha);
        }
    }
    private void Draw()
    {
        float alpha = 0;
        Color color = Color.white;
        SetAllPixelsTo(Color.black, 0);
        int totalRoadPoints = roadPoints.Count;
        int roadPixelID = 0;
        float road_x = 0;
        int id = totalRoadPoints;
        foreach (RoadPoint rp in roadPoints)
        {
            if (roadPixelID == 0 && rp.width < roadPixelWidth)
            {
                roadPixelID = id;
                color = Color.red;
                alpha = 1;
                road_x = rp.x / center;
            }
            else if (id < roadPixelID)
            {
                color = Color.blue; 
                alpha = 0.15f+(rp.width / roadPixelWidth);
                SetRoadPoint(rp, color, alpha, 0, 0);               
            }
            else
            {
                if (carPassed > 0)
                {
                    color = Color.red;
                    alpha = 1;
                    carPassed+=Time.deltaTime;
                    if (carPassed > 1.5f)
                        carPassed = 0;
                }
                else
                {
                    color = Color.white;
                    alpha = (rp.width - roadPixelWidth) / (totalPixels - roadPixelWidth);
                }
                SetRoadPoint(rp, color, alpha);
            }
            if (rp.car_x != 0)
            {
                bool carOnPosition = rp.InPosition();
                rp.UpdateCar();
                int pixel = (int)Mathf.Lerp(rp.x - (rp.width / 2), rp.x + (rp.width / 2), rp.car_x);
                float car_alpha = rp.Alpha();
                Color car_color = Color.red;
                Color redDark = new Color(0.25f, 0, 0);
                if (rp.width > roadPixelWidth - 40)
                {
                    //Two_lights
                    SetColor(pixel + 5, car_color, 1);
                    SetColor(pixel + 4, car_color, 1);
                    SetColor(pixel + 3, car_color, 1);
                    SetColor(pixel + 2, redDark, 1);
                    SetColor(pixel + 1, redDark, 1);
                    SetColor(pixel,     redDark, 1);
                    SetColor(pixel - 1, redDark, 1);
                    SetColor(pixel - 2, redDark, 1);
                    SetColor(pixel - 3, car_color, 1);
                    SetColor(pixel - 4, car_color, 1);
                    SetColor(pixel - 5, car_color, 1);
                }
                else
               if (rp.width > roadPixelWidth - 80)
                {
                    //Two_lights
                    SetColor(pixel + 3, car_color, car_alpha);
                    SetColor(pixel + 2, car_color, car_alpha);
                    SetColor(pixel + 1, redDark, 1);
                    SetColor(pixel    , redDark, 1);
                    SetColor(pixel - 1, redDark, 1);
                    SetColor(pixel - 2, car_color, car_alpha);
                    SetColor(pixel - 3, car_color, car_alpha);
                } else
                if (rp.width>roadPixelWidth -130)
                {
                    //Two_lights
                    SetColor(pixel + 1, car_color, car_alpha);
                    SetColor(pixel - 1, car_color, car_alpha);
                } else
                    SetColor(pixel, car_color, car_alpha);

              
                if (carOnPosition)
                {
                    rp.SetOff();
                    carPassed = 1;
                    if (carPos >= pixel - 5 && carPos <= pixel + 5)
                        Crash();
                }
            }
            if (id == roadPixelID)
            {
                float _right = (int)rp.x + (int)(rp.width / 2);
                if (lastRightKeyframe > (int)_right)
                {
                    float _left = (int)rp.x - (int)(rp.width / 2);
                    AddLimitRight(_right);
                    AddLimitLeft(_left);
                }
                lastRightKeyframe = (int)_right;
            }
            else
            {

                if (id > roadPixelID + 2)
                    SetRoadPoint(rp, color, alpha, 1);
                if (id > roadPixelID + 4)
                    SetRoadPoint(rp, color, alpha, 2);
                if (id > roadPixelID + 6)
                    SetRoadPoint(rp, color, alpha, 3);
                if (id > roadPixelID + 8)
                    SetRoadPoint(rp, color, alpha, 4);
            }

            id--;
        }
        SetColor((int)vanishingPoint, Color.blue, 1);
        limit_right = GetLimit(true);
        limit_left = GetLimit(false);

        SetColor(limit_right, Color.white, 1);
        SetColor(limit_right-1, Color.white, 0.25f);

        float moveByCurve = (road_x - 1) * 200;
        Move(moveByCurve);

        SetLimits(road_x);

        if (carPos >= limit_right || carPos <= limit_left)
            Crash();

        SetCar();
    }
    void SetLimits(float road_x)
    {
        Color color = Color.white;
        if (road_x < 1)
            SetColor(limit_right + 1, color, 1f);
        if (road_x < 0.8)
            SetColor(limit_right + 2, color, 0.75f);
        if (road_x < 0.6f)
            SetColor(limit_right + 3, color, 0.5f);
        if (road_x < 0.4f)
            SetColor(limit_right + 4, color, 0.3f);

        SetColor(limit_left, color, 1);
        SetColor(limit_left + 1, color, 0.25f);

        if (road_x > 1f)
            SetColor(limit_left - 1, color, 1f);
        if (road_x > 1.2)
            SetColor(limit_left - 2, color, 0.75f);
        if (road_x > 1.4f)
            SetColor(limit_left - 3, color, 0.5f);
        if (road_x > 1.6f)
            SetColor(limit_left - 4, color, 0.3f);
    }
    void SetColor(int pixel, Color color, float alpha)
    {
        if (pixel < 0) return;
        if (pixel >= pixels.Count) return;

        pixels[pixel].SetData(color, alpha);
    }
    void SetRoadPoint(RoadPoint rp, Color color, float alpha, int offset = 0, int priority = 1)
    {
        int pixel_right = (int)rp.x + (int)(rp.width / 2);
        int pixel_left = (int)rp.x - (int)(rp.width / 2);

        if(priority == 0)
        {
            if (pixels[pixel_right + offset].IsAvailable())
                SetColor(pixel_right + offset, color, alpha);
            if (pixels[pixel_left - offset].IsAvailable())
                SetColor(pixel_left - offset, color, alpha);
            return;
        }
        SetColor(pixel_right + offset, color, alpha);
        SetColor(pixel_left - offset, color, alpha);
    }


    float curveDuration;
    private float elapsedTime;
    float curvePosible;
    void SetNextPath()
    {
        if(distance<2)
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
        curvePosible = 0;
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
    void CalculateCurve()
    {
        float curve = UnityEngine.Random.Range(-curvePosible, curvePosible);

        if ((curve + vanishingPointTarget) > (totalPixels - 50))
            CalculateCurve();
        else if ((curve + vanishingPointTarget) < 50)
            CalculateCurve();
        else if (Mathf.Abs(curve) < minCurvePossible)
            CalculateCurve();
        else
        {
            vanishingPointTarget += curve;
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
        curveDuration = UnityEngine.Random.Range(randomToCurveDuration.x*5, randomToCurveDuration.x * 5) / aceleration;
        if (curvePosible == 0) curveDuration /= 5; // si es una recta:
    }
    void SetVanishingPoint()
    {
        elapsedTime += Time.deltaTime;
        float progress = Mathf.Clamp01(elapsedTime / curveDuration);
        float easedProgress = EaseInOut(progress);
        float currentValue = Mathf.Lerp(vanishingPoint, vanishingPointTarget, easedProgress);

        if (progress >= 0.15f)
            SetNextPath();
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
    float direction;
    public void Move(float value)
    {
        if (distance < 2) value = 0;
        if (state == 1) value = 0;
        this.direction = value;
        carPos -= carSpeed * value * Time.deltaTime;
    }
    void SetCar()
    {
        // SetColor((int)carPos-1, Color.yellow, 1);
        // SetColor((int)carPos+1, Color.yellow, 1);
        SetColor((int)carPos, Color.yellow, 1);
      //  AddCarPerspective();
    }
    //void AddCarPerspective()
    //{
    //    float alpha = Mathf.Abs((direction*5)/100);
    //    if (alpha > 1) alpha = 1;
    //    if (direction > 5)
    //    {
    //        SetColor((int)carPos -1, Color.yellow, alpha);
    //    } else if (direction < -5)
    //    {
    //        SetColor((int)carPos + 1, Color.yellow, alpha);
    //    }
    //}

    //CRASH:
    float crashTimer = 0;
    int crashLoops;
    void Crash()
    {
        if (distance < 4) return;
        if (state == 1) return;
        crashTimer = 0;
        state = 1;
        crashLoops = 0;
    }
    void UpdateCrash()
    {
        crashTimer += Time.deltaTime;
        if (crashLoops > 5)
        {
            Restart();
        }
        else
        {
            if (crashTimer > 0.3f)
            {
                crashLoops++;
                crashTimer = 0;
            }
            if (crashTimer > 0.15f)
                Draw();
            else
                SetAllPixelsTo(Color.red, 1);
        }
    }
}
