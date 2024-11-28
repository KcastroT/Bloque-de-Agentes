from flask import Flask, jsonify
from traffic_model import TrafficModel
import re

app = Flask(__name__)

# Create and run the model globally
model = TrafficModel(width=24, height=24, steps=1500)
model.run_model()

# Precompute the data
car_movements = model.get_car_positions()
traffic_light_states = model.get_traffic_light_colors()
pedestrian_positions = model.get_pedestrian_positions()
taxi_positions = model.get_taxi_positions()
passenger_positions = model.get_passenger_positions()




@app.route('/cars', methods=['GET'])
def get_car_movements():
    formatted_movements = []
    for car_id, positions in car_movements.items():
        formatted_positions = [{"x": pos[0], "y": pos[1]} for pos in positions]
        formatted_movements.append({
            "carId": car_id,
            "positions": formatted_positions
        })

    return jsonify(formatted_movements)

@app.route('/lights', methods=['GET'])
def get_traffic_light_states():
    formatted_states = []

    # Iterate through traffic_light_states where each key is a light ID
    for light_id, color_history in traffic_light_states.items():
        # Use regex to extract coordinates (x, y)
        match = re.search(r"\((\d+),\s*(\d+)\)", light_id)
        if match:
            x = int(match.group(1))  # Extracted x coordinate
            y = int(match.group(2))  # Extracted y coordinate
        
            # Append the light data with coordinate as trafficLightId
            formatted_states.append({
                "positions": [{"step": step, "color": color} for step, color in enumerate(color_history)],
                "trafficLightId": [x, y]
            })

    return jsonify(formatted_states)

@app.route('/pedestrians', methods=['GET'])
def get_pedestrian_positions():
    formatted_states = []
    for pedestrian_id, positions in pedestrian_positions.items():
        formatted_positions = [{"x": pos[0], "y": pos[1]} for pos in positions]
        formatted_states.append({
            "pedestrianId": pedestrian_id,
            "positions": formatted_positions
        })

    return jsonify(formatted_states)

@app.route('/taxis', methods=['GET'])
def get_taxi_positions():
    formatted_states = []
    for taxi_id, positions in taxi_positions.items():
        formatted_positions = [{"x": pos[0], "y": pos[1]} for pos in positions]
        formatted_states.append({
            "taxiId": taxi_id,
            "positions": formatted_positions
        })

    return jsonify(formatted_states)

@app.route('/passengers', methods=['GET'])
def get_passenger_positions():
    formatted_states = []
    for passenger_id, positions in passenger_positions.items():
        formatted_positions = [{"x": pos[0], "y": pos[1]} for pos in positions]
        formatted_states.append({
            "passengerId": passenger_id,
            "positions": formatted_positions
        })

    return jsonify(formatted_states)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)