using System;
using System.Text;
using System.Net;
using System.Net.Sockets;
using UnityEngine;
 
public class UDP_Client : MonoBehaviour
{

    void FixedUpdate()
    {
        PUdp.Create();
        PUdp.BeginReceive();
    }
}

internal static class PUdp
{
    private static UdpClient socket;
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
        Debug.Log("Data: " + returnData.ToString() + " from " + source);
    }
}