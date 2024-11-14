import mesa
from agents.car_agent import CarAgent
from structures.building import Building
from structures.parking_lot import ParkingLot
from structures.roundabout import Roundabout
from structures.traffic_light import TrafficLight

class CiudadModelo(mesa.Model):
    def __init__(self, n=2, width=23, height=23, seed=None):
        super().__init__(seed=seed)
        self.grid = mesa.space.MultiGrid(width, height, torus=True)

        # Place static structures according to the map layout
        self.setup_map()

        # Add car agents
        for _ in range(n):
            CarAgent(self)

    def setup_map(self):
        # Define edicifios
        building_positions = [(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(8,2),(10,2),
                              (2,3),(3,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),

                              (2,6),(4,6),(5,6),(6,6),(7,6),(8,6),(9,6),(10,6),
                              (2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(10,7),

                              (15,2),(16,3),(15,3),(16,2),(19,2),(20,2),(19,3),

                              (15,6),(19,6),(20,6),
                              (15,7),(19,7),(20,7),(16,7),

                              (2,12),(3,12),(5,12),(8,12),(9,12),(10,12),
                              (2,13),(3,13),(4,13),(5,13),
                              (2,14),(3,14),(4,14),(5,14),
                              (2,15),(3,15),(4,15),(5,15),
                              (2,16),(3,16),(4,16),(5,16),

                              (2,19),(3,19),(5,19),
                              (2,20),(3,20),(4,20),(5,20),
                              (2,21),(3,21),(4,21),(5,21),
                              (8,12),(9,12),(11,12),
                              (8,13),(9,13),(10,13),(11,13),
                              (8,14),(9,14),(10,14),(11,14),
                              (8,15),(9,15),(10,15),(11,15),
                              (8,16),(9,16),(10,16),(11,16),
                              (8,17),(9,17),(10,17),
                              (8,18),(9,18),(10,18),(11,18),
                              (8,19),(9,19),(10,19),(11,19),
                              (8,20),(9,20),(10,20),(11,20),
                              (8,21),(10,21),(11,21),

                              (16,12),(17,12),(19,12),(20,12),(21,12),
                              (16,13),(17,13),(18,13),(19,13),(20,13),(21,13),
                              (16,14),(17,14),(18,14),(19,14),(20,14),(21,14),
                              (16,15),(17,15),(18,15),(19,15),(21,15),

                              (16,18),(17,18),(21,18),
                              (16,19),(17,19),(20,19),(21,19),
                              (16,20),(17,20),(20,20),(21,20),
                              (16,21),(20,21),(21,21)
                              ]
        for pos in building_positions:
            building = Building(self)
            self.grid.place_agent(building, pos)

        # Define estacionamientos
        parking_positions = [(4,3),(9,2),(3,6),(9,7),(20,3),
                             (16,6),(4,12),(2,15),(4,19),(10,12),
                             (8,14),(11,17),(9,21),(18,12),(20,15),
                             (20,18),(17,21)
                             ]
        for pos in parking_positions:
            parking = ParkingLot(self)
            self.grid.place_agent(parking, pos)

        # Define el roundabout en varias posiciones
        roundabout_positions = [(13, 9), (14, 9), (13, 10), (14, 10)]
        for pos in roundabout_positions:
            roundabout = Roundabout(self)
            self.grid.place_agent(roundabout, pos)


        # Define traffic lights with directions (add coordinates and directions as needed)
        traffic_light_positions = {
            # (x, y): "direction",  # Replace with actual coordinates and direction
        }
        for pos, direction in traffic_light_positions.items():
            light = TrafficLight(self, direction)
            self.grid.place_agent(light, pos)

    def step(self):
        for agent in self.grid.agents:
            if isinstance(agent, CarAgent):
                agent.step()