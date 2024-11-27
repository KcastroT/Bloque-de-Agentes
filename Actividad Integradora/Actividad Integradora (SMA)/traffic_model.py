from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
from building_agent import BuildingAgent
from trafficLight_agent import TrafficLightAgent
from parkingLot_Agent import ParkingLotAgent
from car_agent import CarAgent
from verticalRidge_agent import VerticalRidgeAgent
from horizontalRidge_agent import HorizontalRidgeAgent
import random
from peaton_agent import PedestrianAgent

class TrafficModel(Model):
    def __init__(self, width, height,steps = 100):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.steps = steps
        self.current_step = 0
        self.car_movements = {}
        self.traffic_lights = {}

         # Definir posiciones caminables para peatones (sin incluir semáforos)
        self.pedestrian_walkable_positions = set()
        self.component_positions = {
            #componente 1
            (2, 2): [(3, 2), (2, 3)],
            (3, 2): [(4, 2),(2,2)],
            (4, 2): [(5, 2),(3,2)],
            (5, 2): [(5, 3),(4,2)],
            (5, 3): [(5, 4),(5,2)],
            (5,4): [(5,3)],
            #esquina muerta
            (2, 3): [(2, 4),(2,2)],
            (3,4): [(2,4)],
            (2, 4): [(3, 4), (2,3)],
            
            #COMPONENTE 2
            (2,7):[(3,7)],
            (3,7):[(2,7),(4,7)],
            (4,7):[(5,7),(3,7)],
            (5,7):[(5,8),(4,7)],
            (5,8):[(5,9),(5,7)],
            (5,9):[(5,10),(5,8)],
            (5,10):[(5,11),(5,9)],
            #ESQUINA MUERTA
            (2,9):[(2,10)],
            (2,10):[(2,9),(2,11)],
            (2,11):[(2,10),(3,11)],
            (3,11):[(2,11)],
            
            
            #COMPONENTE 3
            (4,17):[(5,17)],
            (5,17):[(6,17),(4,17)],
            (6,17):[(7,17),(5,17)],
            (7,17):[(8,17),(6,17)],
            (8,17):[(9,17),(7,17)],
            (9,17):[(10,17),(8,17)],
            (10,17):[(11,17),(9,17)],
            (11,17):[(11,16),(10,17),(11,18)],
            (11,16):[(11,17)],
            
            (5,20):[(6,20)],
            (6,20):[(7,20),(5,20)],
            (7,20):[(8,20),(6,20)],
            (8,20):[(9,20),(7,20)],
            (9,20):[(10,20),(8,20)],
            (10,20):[(11,20),(9,20)],
            (11,20):[(10,20)],
            
             #LADO DERECHO
            # Componente 1
            (16, 2): [(16, 3)],
            (16, 3): [(16, 4), (16, 2)],
            (16, 4): [(16, 5), (16, 3)],

            # Componente 2

            (21, 2): [(21, 3)],
            (21, 3): [(21, 4), (21, 2)],
            (21, 4): [(21, 5), (21, 3)],
            (21, 5): [ (21, 4)], 
            (21, 8): [(21, 9)],
            (21, 9): [(21, 10), (21, 8)],
            (21, 10): [(21, 11), (21, 9)],
            (21, 11):[(21,10)],
            
            # Componente 2
            (16, 16): [(17, 16), (16,17)],
            (17, 16): [(16, 16)],
            (16, 17): [(16,16)],
            
            (20, 16): [(21, 16)],
            (21, 16): [(20, 16), (21, 17)],
            (21, 17): [(21, 16), (20, 17)],
            (20, 17): [(21, 17)],
            (20, 20): [(20, 21)],
            (20, 21): [(20, 20), (21, 21)],
            (21, 21):[(20,21)]   
        }
        self.banquetota = {
            # Banquetas
            
            #componente 1
            (2, 2): [(3, 2), (2, 3)],
            (3, 2): [(4, 2),(2,2)],
            (4, 2): [(5, 2),(3,2)],
            (5, 2): [(5, 3),(4,2)],
            (5, 3): [(5, 4),(5,2)],
            (5,4): [(5,3)],
            #esquina muerta
            (2, 3): [(2, 4),(2,2)],
            (3,4): [(2,4)],
            (2, 4): [(2, 5), (3, 4), (2,3)],
            
            #SEMAFORO
            (2,5):[(2,4), (2,6)],
            (2,6):[(2,5), (2,7)],
            
            #COMPONENTE 2
            (2,7):[(3,7),(2,6)],
            (3,7):[(2,7),(4,7)],
            (4,7):[(5,7),(3,7)],
            (5,7):[(5,8),(4,7)],
            (5,8):[(5,9),(5,7)],
            (5,9):[(5,10),(5,8)],
            (5,10):[(5,11),(5,9)],
            #ESQUINA MUERTA
            (2,9):[(2,10)],
            (2,10):[(2,9),(2,11)],
            (2,11):[(2,10),(3,11)],
            (3,11):[(2,11)],
            
            
            #COMPONENTE 3
            (4,17):[(5,17)],
            (5,17):[(6,17),(4,17)],
            (6,17):[(7,17),(5,17)],
            (7,17):[(8,17),(6,17)],
            (8,17):[(9,17),(7,17)],
            (9,17):[(10,17),(8,17)],
            (10,17):[(11,17),(9,17)],
            (11,17):[(11,16),(10,17),(11,18)],
            (11,16):[(11,17)],
            
            (5,20):[(6,20)],
            (6,20):[(7,20),(5,20)],
            (7,20):[(8,20),(6,20)],
            (8,20):[(9,20),(7,20)],
            (9,20):[(10,20),(8,20)],
            (10,20):[(11,20),(9,20)],
            (11,20):[(10,20),(11,19)],
            (11,19):[(11,20),(11,18)],
            (11,18):[(11,19),(11,17)],            
            #LADO DERECHO
            # Componente 1
            (16, 2): [(16, 3)],
            (16, 3): [(16, 4), (16, 2)],
            (16, 4): [(16, 5), (16, 3)],

            # Componente 2

            (21, 2): [(21, 3)],
            (21, 3): [(21, 4), (21, 2)],
            (21, 4): [(21, 5), (21, 3)],
            (21, 5): [(21, 6), (21, 4)],
            (21, 6): [(21, 7), (21, 5)], # SEMAFORO
            (21, 7): [(21, 8), (21, 6)], # SEMAFORO
            (21, 8): [(21, 9), (21, 7)],
            (21, 9): [(21, 10), (21, 8)],
            (21, 10): [(21, 11), (21, 9)],
            (21, 11):[(21,10)],
            
            # Componente 2
            (16, 16): [(17, 16), (16,17)],
            (17, 16): [(16, 16)],
            (16, 17): [(16,16)],
            
            (20, 16): [(21, 16)],
            (21, 16): [(20, 16), (21, 17)],
            (21, 17): [(21, 16), (20, 17)],
            (20, 17): [(21, 17), (20, 18)],
            (20, 18): [(20, 17), (20, 19)], # Semáforo
            (20, 19): [(20, 18), (20, 20)], #Semaforo
            (20, 20): [(20, 19), (20, 21)],
            (20, 21): [(20, 20), (21, 21)],
            (21, 21):[(20,21)]
        }

        self.intersections_graph = self.component_positions

        # Adding buildings
        building_positions = [(2,2), (2,3) 
                              ,(3,2),(3,3),
                              (4,2), (2,4),
                              (3,4), (5,4),
                              (4,3), (5,2),
                              (5,3), (8,2), (8,3),
                              (8,4), (8,5),
                              (8,6), (8,7),
                              (8,8), 
                              (8,10),(8,11),
                              (9,3), (9,4),
                              (9,5), (9,6),
                              (9,7), (9,8),
                              (9,9), (9,10),
                              (9,11), 
                              (10,2), (10,3),
                              (10,4), (10,5),
                              (10,6), (10,7),
                              (10,8), (10,9),
                              (10,10), (10,11),
                              (11,2), (11,3),
                              (11,4), (11,5),
                              (11,7), (11,8),
                              (11,9), (11,10), (11,11),

                              (2,7), (2,9),
                              (2,10), (2,11),
                              (3,7), (3,8),
                              (3,9), (3,10),
                              (3,11), (4,7),
                              (4,8), (4,9),
                              (4,10), (5,7),
                              (5,8), (5,9),
                              (5,10), (5,11),

                              (16,2), (16,3),
                              (16,4), (16,5),
                              (16,8), (16,9),
                              (16,10), (16,11),
                              (17,3), (17,4),
                              (17,5),
                              (17,8),(17,9),
                              (17,10), (17,11),

                              (18,8),(18,9),
                              (18,10),
                              (19,8),(19,9),
                              (19,10), (19,11),
                              (20,9),
                              (20,10), (20,11),
                              (21,8), (21,9),
                              (21,10), (21,11),

                              (20,2), (20,3),
                              (20,4),
                              (21,2), (21,3),
                              (21,4), (21,5),

                              (13,13), (13,14),
                              (14,14), (14,13),
                              (2,16),(2,17),
                              (3,16),
                              (4,16),(4,17),
                              (5,16),(5,17),
                              (6,16),(6,17),
                              (7,16),(7,17),
                              (8,16),(8,17),
                              (9,16),(9,17),
                              (10,17),
                              (11,16),(11,17),

                              (2,20),(2,21),
                              (3,20),(3,21),
                              (4,21),
                              (5,20),(5,21),
                              (6,20),(6,21),
                              (7,20),(7,21),
                              (8,20),(8,21),
                              (9,20),
                              (10,20),(10,21),
                              (11,20),(11,21),
                              (16,16),(16,17),
                              (17,16),

                              (16,20),(16,21),
                              (17,20),(17,21),
                              (20,16),(20,17),
                              (21,16),(21,17),

                              (20,20),(20,21),
                              (21,21),
                              
                              ]
        for pos in building_positions:
            building = BuildingAgent(f"building_{pos}", self)
            self.grid.place_agent(building, pos)
            self.schedule.add(building)

        # Adding traffic lights
        traffic_light_positions = {
            (0,3) : "green",
            (1,3) : "green",
            (2,5) : "red",
            (2,6) : "red",
            (18,2) : "green",
            (19,2) : "green",
            (20,0) : "red",
            (20,1) : "red",
            (21,6) : "red",
            (21,7) : "red",
            (18,2) : "green",
            (19,2) : "green",
            (22,8) : "green",
            (23,8) : "green",
            (12,17) : "green",
            (13,17) : "green",
            (11,18) : "red",
            (11,19) : "red",
            (18,17) : "green",
            (19,17) : "green",
            (20,18) : "red",
            (20,19) : "red",
        }

        for pos, color in traffic_light_positions.items():
            traffic_light = TrafficLightAgent(f"traffic_light_{pos}", self, color)
            self.grid.place_agent(traffic_light, pos)
            self.schedule.add(traffic_light)
            
            # Initialize the dictionary entry for each traffic light with an empty list
            self.traffic_lights[traffic_light.unique_id] = []

        # Adding parking lots
        
        self.parking_lot_positions = [(4,4), (8,9), (2,8), (4,11), (9,2), (11,6), (10,11), (17,2), (18,11), (20,8), (20,5), (3,17), (10,16), (4,20), (9,21), (17,17), (21,20)]
        for i, pos in enumerate(self.parking_lot_positions):
            parking_lot = ParkingLotAgent(f"parking_{i}", self)
            self.grid.place_agent(parking_lot, pos)
            self.schedule.add(parking_lot)

        occupied_parking_lots = set()  # Track which parking lots are occupied

        # Spawn 5 cars
        for i in range(25):
            available_parking_lots = [pos for pos in self.parking_lot_positions if pos not in occupied_parking_lots]
            
            if len(available_parking_lots) < 2:
                # No hay suficientes posiciones disponibles para generar autos (inicio y destino distintos)
                break

            start = random.choice(available_parking_lots)
            occupied_parking_lots.add(start)
            
            destination = random.choice([pos for pos in available_parking_lots if pos != start])

            # Create the car agent and place it on the grid
            car = CarAgent(f"car_{i}", self, start, destination)
            self.grid.place_agent(car, start)
            self.schedule.add(car)

            # Initialize movement tracking for this car
            self.car_movements[car.unique_id] = [start]

            # Verificación de asignación correcta de autos
            print(f"Car {i} created at {start} with destination {destination}")
        # Adding pedestrians
        pedestrian_graph_positions = list(self.banquetota.keys())  # Usar las posiciones del grafo (banquetota) del modelo
        traffic_light_positions = [pos for pos, _ in traffic_light_positions.items()]  # Obtener las posiciones de semáforos

        for i in range(15):  # Spawn 15 pedestrians at random nodes of the pedestrian graph
            # Filtrar posiciones para evitar semáforos
            available_positions = [pos for pos in pedestrian_graph_positions if pos not in traffic_light_positions]
            if not available_positions:
                print("No hay posiciones disponibles para peatones")
                break
            start = random.choice(available_positions)
            pedestrian = PedestrianAgent(f"pedestrian_{i}", self, start_pos=start)
            self.grid.place_agent(pedestrian, start)
            self.schedule.add(pedestrian)

            print(f"Pedestrian {i} created at {start}")
            print("\n\n\n\n\n\n\nDESDE AQUI VA EL START", start)
            print("\n\n\n\n\n\n\nDESDE AQUI VA EL DESTINATION", destination)
    
    def add_ridges(self):
        
        VerticalRidges = [
            (14,2),
            (14,3),
            (14,4),
            (14,5),
            (14,6),
            (14,7),
            (14,8),
            (14,9),
            (14,10),
            (14,11),
            (14,17),
            (14,18),
            (14,19),
            (14,20),
            (14,21),
        ]

        for pos in VerticalRidges:
            ridge = VerticalRidgeAgent(f"ridge_{pos}", self, pos)
            self.grid.place_agent(ridge, pos)
            self.schedule.add(ridge)

        HorizontalRidges = [
            (2,14),
            (3,14),
            (4,14),
            (5,14),
            (6,14),
            (7,14),
            (8,14),
            (9,14),
            (10,14),
            (11,14),
            (16,14),
            (17,14),
            (18,14),
            (19,14),
            (20,14),
            (21,14),
            (22,14)
        ]

        for pos in HorizontalRidges:
            ridge = HorizontalRidgeAgent(f"ridge_{pos}", self, pos)
            self.grid.place_agent(ridge, pos)
            self.schedule.add(ridge)
            

    def random_unoccupied_position(self):
        while True:
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            cellmates = self.grid.get_cell_list_contents([(x, y)])
            if not cellmates:
                return (x, y)
            
   
            
    def get_car_positions(self):
       return self.car_movements
    
    def get_traffic_light_colors(self):
        return self.traffic_lights

    def step(self):
        """
        Run one step of the simulation. This includes moving all agents
        and tracking car movements.
        """
        for agent in self.schedule.agents:
            if isinstance(agent, TrafficLightAgent):
                self.traffic_lights[agent.unique_id].append(agent.color)

        # Track car positions during the step
        for agent in self.schedule.agents:
            if isinstance(agent, CarAgent):
                self.car_movements[agent.unique_id].append(agent.pos)

        # Advance the simulation
        self.schedule.step()
        self.current_step += 1

    def run_model(self):
        """
        Run the model for the predefined number of steps.
        """
        while self.current_step < self.steps:
            self.step()