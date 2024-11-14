from agents.car_agent import CarAgent
from structures.building import Building
from structures.parking_lot import ParkingLot
from structures.roundabout import Roundabout
from structures.traffic_light import TrafficLight

def agent_portrayal(agent):
    if isinstance(agent, CarAgent):
        return {"color": "black", "size": 10, "shape": "circle"}
    elif isinstance(agent, Building):
        return {"Color": "blue", "Shape": "rect","Filled":"True","Layer":0,"w":1,"h":1}
    elif isinstance(agent, ParkingLot):
        return {"color": "yellow", "Shape":"rect", "size": 50}
    elif isinstance(agent, Roundabout):
        return {"color": "brown", "Shape": "rect", "size": 50}
    elif isinstance(agent, TrafficLight):
        return {"color": "red", "Shape": "rect", "size": 50}
    return {"color": "green", "Shape": "rect", "size": 50}  # Por defecto, cuadrado para otros agentes