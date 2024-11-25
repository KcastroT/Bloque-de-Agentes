using UnityEngine;

public class Semaforo : MonoBehaviour
{
    // Referencias a los materiales de las luces
    public Material luzRoja;
    public Material luzAmarilla;
    public Material luzVerde;

    // Tiempo que cada luz estará encendida
    public float tiempoRojo = 5f;
    public float tiempoAmarillo = 2f;
    public float tiempoVerde = 5f;

    private float temporizador;
    private enum EstadoSemaforo { Rojo, Amarillo, Verde }
    private EstadoSemaforo estadoActual;

    // Start se ejecuta al inicio
    void Start()
    {
        estadoActual = EstadoSemaforo.Rojo; // Comienza en rojo
        temporizador = tiempoRojo;
        ActualizarLuces();
    }

    // Update se llama una vez por frame
    void Update()
    {
        temporizador -= Time.deltaTime;

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

        ActualizarLuces();
    }

    void ActualizarLuces()
    {
        // Apaga todas las luces al inicio
        luzRoja.DisableKeyword("_EMISSION");
        luzAmarilla.DisableKeyword("_EMISSION");
        luzVerde.DisableKeyword("_EMISSION");

        // Enciende la luz correspondiente al estado actual
        switch (estadoActual)
        {
            case EstadoSemaforo.Rojo:
                luzRoja.EnableKeyword("_EMISSION");
                break;
            case EstadoSemaforo.Amarillo:
                luzAmarilla.EnableKeyword("_EMISSION");
                break;
            case EstadoSemaforo.Verde:
                luzVerde.EnableKeyword("_EMISSION");
                break;
        }
    }
}
