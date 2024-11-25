from flask import Flask, jsonify
from traffic_model import TrafficModel  # Import your model here

app = Flask(__name__)

@app.route('/run_simulation', methods=['GET'])
def run_simulation():
    # Initialize the model
    model = TrafficModel(width=24, height=24, steps=100)

    # Run the model to completion
    model.run_model()

    # Retrieve car movements
    movements = model.get_car_positions()

    # Prepare JSON response
    response = {
        "steps": model.steps,
        "car_movements": movements
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)