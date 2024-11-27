using UnityEngine;

public class LightController : MonoBehaviour
{
    public Light targetLight; // Asigna la luz direccional que representa el sol
    public Color dayColor = Color.white; // Color de la luz durante el día
    public Color nightColor = Color.black; // Color de la luz durante la noche
    public float cycleDuration = 5f; // Duración total del ciclo día-noche (en segundos)
    public bool rotateLight = true; // Simula el movimiento del sol si es true

    private float timer = 0f; // Temporizador interno

    void Start()
    {
        if (targetLight == null)
        {
            Debug.LogError("No se asignó una luz al script.");
            return;
        }
    }

    void Update()
    {
        // Incrementa el temporizador con el tiempo transcurrido
        timer += Time.deltaTime;

        // Calcula el progreso del ciclo de día-noche (entre 0 y 1)
        float cycleProgress = Mathf.PingPong(timer / cycleDuration, 1);

        // Interpola el color de la luz entre día y noche
        targetLight.color = Color.Lerp(nightColor, dayColor, cycleProgress);

        // Si rotateLight está habilitado, rota la luz para simular el movimiento del sol
        if (rotateLight)
        {
            float angle = cycleProgress * 360f - 90f; // Gira entre -90° y 270°
            targetLight.transform.rotation = Quaternion.Euler(new Vector3(angle, 0, 0));
        }
    }
}
