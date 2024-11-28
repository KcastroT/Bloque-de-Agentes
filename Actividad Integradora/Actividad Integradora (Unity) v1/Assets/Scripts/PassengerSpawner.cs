using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class PassengerSpawner : MonoBehaviour
{
    public GameObject passengerPrefab;

    [System.Serializable]
    public class Position
    {
        public float x;
        public float y;
    }

    [System.Serializable]
    public class Passenger
    {
        public string passengerId;
        public List<Position> positions;
    }

    [System.Serializable]
    public class TaxiList
    {
        public List<Passenger> passengers;
    }

    public string dataUrl = "http://127.0.0.1:5000/passengers";

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
                string jsonResponse = webRequest.downloadHandler.text;
                Debug.Log($"JSON Response: {jsonResponse}");

                string wrappedJson = "{\"passengers\":" + jsonResponse + "}";
                TaxiList carList = JsonUtility.FromJson<TaxiList>(wrappedJson);

                Debug.Log($"Taxi Count: {carList.passengers.Count}");

                processCarList(carList);
            }
        }
    }

    void processCarList(TaxiList carList)
    {
        foreach (var car in carList.passengers)
        {

            // Instantiate the selected car model
            GameObject instantiatedPassenger = Instantiate(passengerPrefab, Vector3.zero, Quaternion.identity);
            StartCoroutine(MoveCar(instantiatedPassenger, car.positions));
        }
    }

    IEnumerator MoveCar(GameObject car, List<Position> positions)
    {
        if (positions == null || positions.Count == 0)
            yield break;

        Vector3 previousPosition = new Vector3(positions[0].x, 0f, positions[0].y);
        car.transform.position = previousPosition;



        for (int i = 1; i < positions.Count; i++)
        {
            Vector3 targetPosition = new Vector3(positions[i].x - 0.25f, 0f, positions[i].y * -1 - 0.25f);
            Vector3 direction = targetPosition - previousPosition;
            float angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;
            Quaternion targetRotation = Quaternion.Euler(0, angle, 0);

            float elapsedTime = 0f;
            float duration = 0.25f; // Adjust duration for smoothness

            while (elapsedTime < duration)
            {
                car.transform.position = Vector3.Lerp(previousPosition, targetPosition, elapsedTime / duration);
                car.transform.rotation = Quaternion.Lerp(car.transform.rotation, targetRotation, elapsedTime / duration);
                elapsedTime += Time.deltaTime;
                yield return null;
            }

            car.transform.position = targetPosition;
            car.transform.rotation = targetRotation;

            previousPosition = targetPosition;

            yield return null;
        }
    }
}