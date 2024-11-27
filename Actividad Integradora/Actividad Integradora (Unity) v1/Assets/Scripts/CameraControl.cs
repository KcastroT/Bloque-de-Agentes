using UnityEngine;

public class CameraControl : MonoBehaviour
{
    public float moveSpeed = 10f; // Speed of the camera movement

    void Update()
    {
        // Get input from WASD or arrow keys
        float moveHorizontal = Input.GetAxis("Horizontal"); // A/D or Left/Right Arrow
        float moveVertical = Input.GetAxis("Vertical");     // W/S or Up/Down Arrow


        // Calculate movement
        Vector3 movement = new Vector3(moveHorizontal, 0, moveVertical) * moveSpeed * Time.deltaTime;

        // Apply movement to the camera
        transform.Translate(movement, Space.World);
    }
}
