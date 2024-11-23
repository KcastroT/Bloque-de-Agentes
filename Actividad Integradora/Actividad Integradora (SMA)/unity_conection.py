from flask import Flask, request, jsonify
from threading import Thread
import time

from traffic_model import TrafficModel

app = Flask(__name__)
model = TrafficModel(width=24, height=24)

running = True

def run_model():
    """
    Función que ejecuta el modelo de Mesa en un hilo separado.
    """
    while running:
        time.sleep(1)
        model.step()

model_thread = Thread(target=run_model)
model_thread.start()

@app.route('/get_agent_coordinates', methods=['GET'])
def get_agent_coordinates():
    agent_positions = model.get_agent_positions()
    return jsonify(agent_positions)

@app.route('/send_coordinates', methods=['POST'])
def send_coordinates():
    data = request.json
    print(f"Coordenadas recibidas de Unity: {data}")
    return jsonify({'message': 'Coordenadas recibidas exitosamente'})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    """
    Ruta para detener el servidor y el modelo de Mesa de manera segura.
    """
    global running
    running = False
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()
    return 'Servidor detenido.'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        running = False
        model_thread.join()

