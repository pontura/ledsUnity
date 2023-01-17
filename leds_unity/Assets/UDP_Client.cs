using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using UnityEngine;
using System.Collections.Generic;

public class UDP_Client : MonoBehaviour
{
    string result;
    static UdpClient socket;
    void FixedUpdate()
    {
        Create();
        BeginReceive();
    }
    public static void Create()
    {
        if (socket == null)
            socket = new UdpClient(5555);
    }
    public static void BeginReceive()
    {
        socket.BeginReceive(new AsyncCallback(OnUdpData), socket);
    }
    private static void OnUdpData(IAsyncResult result)
    {
        UdpClient socket = result.AsyncState as UdpClient;
        IPEndPoint source = new IPEndPoint(0, 0);
        byte[] message = socket.EndReceive(result, ref source);
        string returnData = Encoding.ASCII.GetString(message);
        // string returnData = Encoding.ASCII.GetString(message);

        string[] arr = returnData.Split("|"[0]);
        Color color = new Color();
        List<Color> list = new List<Color>();
        foreach (string s in arr)
        {
            string[] c = s.Split(","[0]);
            if (c.Length > 1)
            {
                color.r = 255;
                color.g = (int.Parse(c[1]));
                color.b =(int.Parse(c[2]));
                color.a = 1;
                list.Add(color);
            }
        }

        CircularView.Instance.OnUpdate(list);
    }
}