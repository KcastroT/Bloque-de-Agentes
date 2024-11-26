using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CarSpawner : MonoBehaviour
{
    [System.Serializable]
    public class Position
    {
        public float x;
        public float y;
    }

    [System.Serializable]
    public class Car
    {
        public string carId;
        public List<Position> positions;
    }

    [System.Serializable]
    public class CarList
    {
        public List<Car> cars;
    }

    public string dataUrl = "http://127.0.0.1:5000/run_simulation";

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(FetchCarData());
    }

    IEnumerator FetchCarData()
    {
        using (UnityWebRequest webRequest = UnityWebRequest.Get(dataUrl))
        {
            yield return webRequest.SendWebRequest();

            if (webRequest.result == UnityWebRequest.Result.ConnectionError ||
                webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"Error fetching data: {webRequest.error}");
            }
            else
            {
                // Parse JSON response using Unity's JsonUtility
                string jsonResponse = webRequest.downloadHandler.text;
                Debug.Log($"JSON Response: {jsonResponse}");

                // Wrap the JSON array in a root object (necessary for JsonUtility to work)
                string wrappedJson = "{\"cars\":" + jsonResponse + "}";

                // Deserialize the JSON response
                CarList carList = JsonUtility.FromJson<CarList>(wrappedJson);

                Debug.Log($"Car Count: {carList.cars.Count}");

                // Log each car and its positions
                foreach (var car in carList.cars)
                {
                    Debug.Log($"Car ID: {car.carId}");
                    foreach (var position in car.positions)
                    {
                        // Log the positions as floats
                        Debug.Log($"Position: ({position.x}, {position.y})");
                    }
                }
            }
        }
    }
}