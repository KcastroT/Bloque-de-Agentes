using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class TrafficLightSpawner : MonoBehaviour
{
    public GameObject pointLightPrefab;  // Prefab for the point light (can be any light you want to spawn)

    [System.Serializable]
    public class Position
    {
        public float x;
        public float y;
        public string color;  // Add color to the position
    }

    [System.Serializable]
    public class TrafficLight
    {
        public List<Position> positions;  // List of positions over time
        public int[] trafficLightId;      // Coordinates [x, y] of the traffic light
    }

    [System.Serializable]
    public class TrafficLightList
    {
        public List<TrafficLight> trafficLights; // List of traffic lights
    }

    public string dataUrl = "http://127.0.0.1:5000/lights";  // URL where the traffic light data is fetched

    void Start()
    {
        StartCoroutine(FetchTrafficLightData());
    }

    IEnumerator FetchTrafficLightData()
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

                string wrappedJson = "{\"trafficLights\":" + jsonResponse + "}";
                TrafficLightList trafficLightList = JsonUtility.FromJson<TrafficLightList>(wrappedJson);

                Debug.Log($"Traffic Light Count: {trafficLightList.trafficLights.Count}");

                processTrafficLightList(trafficLightList);
            }
        }
    }

    void processTrafficLightList(TrafficLightList trafficLightList)
    {
        foreach (var trafficLight in trafficLightList.trafficLights)
        {
            // Get the coordinates of the traffic light
            int x = trafficLight.trafficLightId[0];
            int y = trafficLight.trafficLightId[1];

            // Instantiate a point light at the specified position
            Vector3 position = new Vector3(x, 1, y * -1);  // Y value can be adjusted based on your scene setup
            GameObject spawnedLight = Instantiate(pointLightPrefab, position, Quaternion.identity);

            // Start cycling through traffic light colors
            StartCoroutine(CycleTrafficLight(spawnedLight, trafficLight.positions));
        }
    }

    IEnumerator CycleTrafficLight(GameObject trafficLight, List<Position> positions)
    {
        if (positions == null || positions.Count == 0)
            yield break;

        Light lightComponent = trafficLight.GetComponent<Light>();

        // Debug the initial state of the light


        // Set the initial color based on the first position's color
        string initialColor = positions[0].color;  // Assuming you want to parse 'green' or 'red' from color property
        if (initialColor == "green")
        {
            lightComponent.color = Color.green;
        }
        else if (initialColor == "red")
        {
            lightComponent.color = Color.red;
        }

        // Cycle through the positions list, switching light colors
        for (int i = 1; i < positions.Count; i++)
        {
            string colorState = positions[i].color; // Get the color state from the JSON data


            // Change the light color based on the current state
            if (colorState == "green")
            {
                lightComponent.color = Color.green;
            }
            else if (colorState == "red")
            {
                lightComponent.color = Color.red;
            }

            // Debug the color change


            // Simulate the duration for the traffic light state (adjust for smoother transitions)
            float elapsedTime = 0f;
            float duration = 0.25f; // Duration of each light cycle (in seconds)

            while (elapsedTime < duration)
            {
                elapsedTime += Time.deltaTime;
                yield return null;
            }
        }
    }
}