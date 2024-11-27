from mesa import Agent
from collections import deque
from trafficLight_agent import TrafficLightAgent
from car_agent import CarAgent

class PedestrianAgent(Agent):
    def __init__(self, unique_id, model, start_pos):
        super().__init__(unique_id, model)
        # Asegurarse de que los peatones no empiecen en una posición con semáforo
        traffic_light_positions = [agent.pos for agent in model.schedule.agents if isinstance(agent, TrafficLightAgent)]
        while start_pos in traffic_light_positions:
            start_pos = model.random_unoccupied_position()
        self.current_pos = start_pos
        self.crossing_traffic_light = False
        self.cross_path = []

    def move(self):
        if self.crossing_traffic_light and len(self.cross_path) > 0:
            # Cruzar completamente el semáforo
            next_pos = self.cross_path.pop(0)
            if self.can_move_to(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.current_pos = next_pos
            if len(self.cross_path) == 0:
                # Termina de cruzar
                self.crossing_traffic_light = False
        else:
            # Buscar si hay un semáforo cercano y decidir si cruzar
            neighbors = self.get_neighbors(self.current_pos)
            for neighbor in neighbors:
                cellmates = self.model.grid.get_cell_list_contents([neighbor])
                for agent in cellmates:
                    if isinstance(agent, TrafficLightAgent) and agent.color == "red":
                        # Encontrar la secuencia completa para cruzar el semáforo
                        self.cross_path = [neighbor]
                        self.crossing_traffic_light = True
                        return
            # Si el semáforo está en verde y el peatón está en la posición del semáforo, moverse a una posición vecina
            cellmates = self.model.grid.get_cell_list_contents([self.current_pos])
            for agent in cellmates:
                if isinstance(agent, TrafficLightAgent) and agent.color == "green":
                    # Si el semáforo está en verde, el peatón debe moverse inmediatamente
                    valid_moves = [pos for pos in neighbors if self.can_move_to(pos)]
                    if valid_moves:
                        next_move = self.random.choice(valid_moves)
                        self.model.grid.move_agent(self, next_move)
                        self.current_pos = next_move
                        return
            # Si no hay semáforo, moverse a una posición vecina aleatoria
            valid_moves = [pos for pos in neighbors if self.can_move_to(pos)]
            if valid_moves:
                next_move = self.random.choice(valid_moves)
                self.model.grid.move_agent(self, next_move)
                self.current_pos = next_move

    def step(self):
        # Intentar moverse o cruzar el semáforo
        self.move()

    def get_crossing_path(self, current_pos, traffic_light_pos):
        # Define la secuencia de posiciones que cruzan completamente el semáforo
        graph = self.model.banquetota
        if traffic_light_pos not in graph:
            return []

        crossing_path = []
        neighbors = graph.get(traffic_light_pos, [])
        for neighbor in neighbors:
            if neighbor not in self.model.banquetota:
                crossing_path.append(neighbor)

        return crossing_path

    def can_move_to(self, pos):
        # Verificar que la posición está libre de otros peatones o coches
        cellmates = self.model.grid.get_cell_list_contents([pos])
        return not any(isinstance(other_agent, (CarAgent, PedestrianAgent)) for other_agent in cellmates)

    def get_neighbors(self, position):
        # Devuelve los vecinos válidos desde el grafo de banquetas
        return self.model.banquetota.get(position, [])
