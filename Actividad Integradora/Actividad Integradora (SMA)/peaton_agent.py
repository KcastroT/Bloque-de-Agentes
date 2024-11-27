from mesa import Agent
from collections import deque
from trafficLight_agent import TrafficLightAgent
from car_agent import CarAgent

class PedestrianAgent(Agent):
    def __init__(self, unique_id, model, start_pos):
        super().__init__(unique_id, model)
        self.current_pos = start_pos
        self.crossing = False
        self.cross_path = []
        self.waiting = False

    def move(self):
        # Verificar si el peatón está sobre un semáforo
        cellmates = self.model.grid.get_cell_list_contents([self.current_pos])
        traffic_light = next((agent for agent in cellmates if isinstance(agent, TrafficLightAgent)), None)
        if traffic_light:
            if traffic_light.can_pedestrian_cross():
                # Si el semáforo permite cruzar, continuar cruzando
                self.crossing = True
                self.waiting = False
                if not self.cross_path:
                    # Generar la ruta de cruce desde la posición actual
                    self.cross_path = self.get_crossing_path(self.current_pos, self.current_pos)
            else:
                # Si el semáforo está en verde para coches, moverse fuera de la posición
                self.crossing = False
                self.waiting = True
                self.move_off_traffic_light()
                return  # Terminar el movimiento aquí
        else:
            self.waiting = False

        if self.crossing and self.cross_path:
            # Continuar cruzando
            next_pos = self.cross_path.pop(0)
            if self.can_move_to(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.current_pos = next_pos
            else:
                # No puede moverse, espera
                self.crossing = False
            if not self.cross_path:
                # Termina de cruzar
                self.crossing = False
        else:
            # Buscar semáforos en posiciones vecinas
            neighbors = self.get_neighbors(self.current_pos)
            for neighbor in neighbors:
                cellmates = self.model.grid.get_cell_list_contents([neighbor])
                traffic_light = next((agent for agent in cellmates if isinstance(agent, TrafficLightAgent)), None)
                if traffic_light:
                    if traffic_light.can_pedestrian_cross():
                        # Planificar la ruta de cruce
                        self.cross_path = self.get_crossing_path(self.current_pos, neighbor)
                        self.crossing = True
                        return
                    else:
                        # Esperar en el cruce
                        self.waiting = True
                        return
            if not self.crossing:
                # Moverse aleatoriamente si no está esperando
                valid_moves = [pos for pos in neighbors if self.can_move_to(pos)]
                if valid_moves:
                    next_move = self.random.choice(valid_moves)
                    self.model.grid.move_agent(self, next_move)
                    self.current_pos = next_move

    def move_off_traffic_light(self):
        # Encontrar una posición vecina que esté en component_positions y no sea un semáforo
        neighbors = self.get_neighbors(self.current_pos)
        valid_moves = [pos for pos in neighbors if self.can_move_to(pos)]
        for pos in valid_moves:
            cellmates = self.model.grid.get_cell_list_contents([pos])
            is_traffic_light = any(isinstance(agent, TrafficLightAgent) for agent in cellmates)
            if pos in self.model.component_positions and not is_traffic_light:
                # Mover al peatón a esta posición
                self.model.grid.move_agent(self, pos)
                self.current_pos = pos
                self.waiting = False
                return
        # Si no hay movimiento válido, el peatón permanece en su lugar

    def get_crossing_path(self, start_pos, traffic_light_pos):
        # Definir la ruta para cruzar el semáforo
        crossing_path = []
        crossing_path.append(traffic_light_pos)
        # Encontrar la posición opuesta al semáforo
        neighbors = self.model.intersections_graph.get(traffic_light_pos, [])
        for neighbor in neighbors:
            if neighbor != start_pos and neighbor not in self.model.banquetota:
                crossing_path.append(neighbor)
                break
        return crossing_path

    def step(self):
        self.move()

    def can_move_to(self, pos):
        # Verificar que la posición está libre de otros peatones o coches
        cellmates = self.model.grid.get_cell_list_contents([pos])
        return not any(isinstance(other_agent, CarAgent) for other_agent in cellmates)

    def get_neighbors(self, position):
        # Devuelve los vecinos válidos desde el grafo de banquetas
        return self.model.banquetota.get(position, [])
