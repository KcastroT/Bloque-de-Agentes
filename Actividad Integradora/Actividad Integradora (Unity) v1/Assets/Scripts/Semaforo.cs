using UnityEngine;

public class Semaforo : MonoBehaviour
{
    public Material luzRoja;
    public Material luzAmarilla;
    public Material luzVerde;

    public float tiempoRojo = 3f;
    public float tiempoAmarillo = 2f;
    public float tiempoVerde = 3f;

    private float temporizador;
    private enum EstadoSemaforo { Rojo, Amarillo, Verde }
    private EstadoSemaforo estadoActual;

    void Start()
    {
        estadoActual = EstadoSemaforo.Rojo;
        temporizador = tiempoRojo;
        ActualizarLuces();
        Debug.Log("El semáforo inició en rojo.");
    }

    void Update()
    {
        temporizador -= Time.deltaTime;
        Debug.Log($"Temporizador: {temporizador}, Estado: {estadoActual}");

        if (temporizador <= 0)
        {
            CambiarEstado();
        }
    }

    void CambiarEstado()
    {
        switch (estadoActual)
        {
            case EstadoSemaforo.Rojo:
                estadoActual = EstadoSemaforo.Verde;
                temporizador = tiempoVerde;
                break;
            case EstadoSemaforo.Verde:
                estadoActual = EstadoSemaforo.Amarillo;
                temporizador = tiempoAmarillo;
                break;
            case EstadoSemaforo.Amarillo:
                estadoActual = EstadoSemaforo.Rojo;
                temporizador = tiempoRojo;
                break;
        }

        Debug.Log($"Cambio a estado: {estadoActual}");
        ActualizarLuces();
    }

    void ActualizarLuces()
    {
        luzRoja.DisableKeyword("_EMISSION");
        luzAmarilla.DisableKeyword("_EMISSION");
        luzVerde.DisableKeyword("_EMISSION");

        switch (estadoActual)
        {
            case EstadoSemaforo.Rojo:
                luzRoja.EnableKeyword("_EMISSION");
                Debug.Log("Luz roja encendida");
                break;
            case EstadoSemaforo.Amarillo:
                luzAmarilla.EnableKeyword("_EMISSION");
                Debug.Log("Luz amarilla encendida");
                break;
            case EstadoSemaforo.Verde:
                luzVerde.EnableKeyword("_EMISSION");
                Debug.Log("Luz verde encendida");
                break;
        }
    }
}
