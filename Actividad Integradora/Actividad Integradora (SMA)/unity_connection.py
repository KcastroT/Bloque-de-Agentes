from flask import Flask, jsonify
from traffic_model import TrafficModel

app = Flask(__name__)

@app.route('/run_simulation', methods=['GET'])
def run_simulation():
    # Initialize the model
    model = TrafficModel(width=24, height=24, steps=100)
    model.run_model()
    movements = model.get_car_positions()

    formatted_movements = []
    for car_id, positions in movements.items():
        formatted_positions = [{"x": pos[0], "y": pos[1]} for pos in positions]
        formatted_movements.append({
            "carId": car_id,
            "positions": formatted_positions
        })

    response = formatted_movements

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)