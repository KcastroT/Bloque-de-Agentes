from mesa import Agent
from collections import deque
from trafficLight_agent import TrafficLightAgent
from car_agent import CarAgent

class PedestrianAgent(Agent):
    def __init__(self, unique_id, model, start_pos):
        super().__init__(unique_id, model)
        self.start_pos = start_pos
        self.current_pos = start_pos

        # Inicializar atributos antes de usarlos
        self.traffic_lights = [(2, 5), (2, 6)]  # Puedes mover esta lista al modelo si prefieres tenerla centralizada.
        
        # Inicializar la ruta al semáforo más cercano
        self.path = self.find_nearest_traffic_light_dfs(start_pos)  
        
        self.reached_traffic_light = False
        self.crossing_traffic_light = False
        self.cross_path = []

    def find_nearest_traffic_light_dfs(self, start):
        # Implementación de DFS para encontrar el semáforo más cercano
        graph = self.model.banquetota  # Acceder al grafo desde el modelo
        if start not in graph:
            return []

        stack = [[start]]
        visited = set()

        while stack:
            path = stack.pop()
            current_node = path[-1]

            if current_node in self.traffic_lights:
                return path[1:]  # Excluir la posición actual

            if current_node not in visited:
                visited.add(current_node)
                for neighbor in graph.get(current_node, []):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        stack.append(new_path)

        return []

    def move(self):
        if len(self.path) > 0 and not self.crossing_traffic_light:
            # Moverse hacia el semáforo
            next_pos = self.path.pop(0)
            self.model.grid.move_agent(self, next_pos)
            self.current_pos = next_pos
        elif self.crossing_traffic_light and len(self.cross_path) > 0:
            # Cruzar completamente el semáforo
            next_pos = self.cross_path.pop(0)
            if self.can_move_to(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.current_pos = next_pos
            if len(self.cross_path) == 0:
                # Termina de cruzar
                self.crossing_traffic_light = False
        else:
            # Esperar a que el semáforo esté en rojo y preparar la secuencia para cruzar
            cellmates = self.model.grid.get_cell_list_contents([self.current_pos])
            for agent in cellmates:
                if isinstance(agent, TrafficLightAgent) and agent.color == "red":
                    # Encontrar la secuencia completa para cruzar el semáforo
                    self.cross_path = self.get_crossing_path(self.current_pos)
                    self.crossing_traffic_light = True

    def step(self):
        if not self.reached_traffic_light and len(self.path) > 0:
            # Moverse hacia el semáforo
            self.move()
            if self.current_pos in self.traffic_lights:
                # Cuando llegue a la posición del semáforo
                self.reached_traffic_light = True
        else:
            # Cruzar el semáforo si ya llegó
            self.move()

    def get_crossing_path(self, current_pos):
        # Define la secuencia de posiciones que cruzan completamente el semáforo
        graph = self.model.banquetota
        if current_pos not in graph:
            return []

        crossing_path = []
        neighbors = graph.get(current_pos, [])
        for neighbor in neighbors:
            if neighbor not in self.traffic_lights:
                crossing_path.append(neighbor)

        return crossing_path

    def can_move_to(self, pos):
        # Verificar que la posición está libre de otros peatones o coches
        cellmates = self.model.grid.get_cell_list_contents([pos])
        return not any(isinstance(other_agent, (CarAgent)) for other_agent in cellmates)
