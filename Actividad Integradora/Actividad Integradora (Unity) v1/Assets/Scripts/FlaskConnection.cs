// este código no está en uso, pero se deja como referencia

using UnityEngine;
using UnityEngine.Networking;  // Para solicitudes HTTP
using System.Collections;

public class FlaskConnection : MonoBehaviour
{
    private string flaskUrl = "http://127.0.0.1:5000"; // Dirección del servidor Flask

    // Método para obtener coordenadas desde Flask
    public IEnumerator GetCoordinatesFromFlask()
    {
        UnityWebRequest request = UnityWebRequest.Get($"{flaskUrl}/get_coordinates");
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResult = request.downloadHandler.text;
            Coordinates coords = JsonUtility.FromJson<Coordinates>(jsonResult);

            Debug.Log($"Received coordinates: X={coords.x}, Y={coords.y}, Z={coords.z}");

            // Usa las coordenadas para mover un objeto en Unity
            Vector3 position = new Vector3(coords.x, coords.y, coords.z);
            transform.position = position;
        }
        else
        {
            Debug.LogError($"Error fetching coordinates: {request.error}");
        }
    }

    // Método para enviar coordenadas a Flask
    public IEnumerator SendCoordinatesToFlask(Vector3 coordinates)
    {
        Coordinates coords = new Coordinates
        {
            x = coordinates.x,
            y = coordinates.y,
            z = coordinates.z
        };

        string json = JsonUtility.ToJson(coords);
        byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(json);

        UnityWebRequest request = UnityWebRequest.Put($"{flaskUrl}/send_coordinates", jsonToSend);
        request.SetRequestHeader("Content-Type", "application/json");
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Coordinates sent successfully!");
        }
        else
        {
            Debug.LogError($"Error sending coordinates: {request.error}");
        }
    }
}

// Clase para manejar las coordenadas como JSON
[System.Serializable]
public class Coordinates
{
    public float x;
    public float y;
    public float z;
}