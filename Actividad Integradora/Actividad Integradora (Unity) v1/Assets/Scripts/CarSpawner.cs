using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class CarSpawner : MonoBehaviour
{
    public GameObject carPrefab;

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

                processCarList(carList);

            }
        }
    }

    void processCarList(CarList carList)
    {
        // Spawn a car for each car in the list and move them based on their positions
        foreach (var car in carList.cars)
        {
            // Instantiate a new car object
            GameObject carObject = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
            carObject.name = car.carId; // Assign a unique name to the car

            // Move the car according to its positions
            StartCoroutine(MoveCar(carObject, car.positions));
        }
    }

    // Coroutine to move a car through its list of positions in a 3D grid
    IEnumerator MoveCar(GameObject car, List<Position> positions)
    {
        // Ensure there are positions to move to
        if (positions == null || positions.Count == 0)
            yield break;

        // Set the initial position of the car
        Vector3 previousPosition = new Vector3(positions[0].x, 0, positions[0].y);
        car.transform.position = previousPosition;

        for (int i = 1; i < positions.Count; i++)
        {
            // Get the current target position
            Vector3 targetPosition = new Vector3(positions[i].x, 0, positions[i].y * -1);

            // Calculate the direction vector (current - previous)
            Vector3 direction = targetPosition - previousPosition;

            // Calculate the rotation angle in degrees (y-axis rotation in a 3D grid)
            float angle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg;

            // Apply rotation to the car
            car.transform.rotation = Quaternion.Euler(0, angle, 0);

            // Move the car to the target position
            car.transform.position = targetPosition;

            // Update the previous position
            previousPosition = targetPosition;

            // Wait for a short duration before moving to the next position
            yield return new WaitForSeconds(0.5f); // Adjust the delay as needed
        }
    }


}