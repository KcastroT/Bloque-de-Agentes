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
        # Obtener los agentes en la celda actual
        cellmates = self.model.grid.get_cell_list_contents([self.current_pos])
        traffic_light = next((agent for agent in cellmates if isinstance(agent, TrafficLightAgent)), None)

        if traffic_light:
            if traffic_light.can_pedestrian_cross():
                self.crossing = True
                self.waiting = False
                if not self.cross_path:
                    # Generar la ruta de cruce desde la posición actual
                    self.cross_path = self.get_crossing_path(self.current_pos, self.current_pos)
            else:
                # Mover fuera del semáforo si no puede cruzar
                self.crossing = False
                self.waiting = True
                self.move_off_traffic_light()
                return  # Terminar el movimiento aquí
        else:
            self.waiting = False

        if self.crossing and self.cross_path:
            next_pos = self.cross_path.pop(0)

            # Verificar si el próximo movimiento es hacia un semáforo y está adyacente
            cellmates_next = self.model.grid.get_cell_list_contents([next_pos])
            traffic_light_next = next((agent for agent in cellmates_next if isinstance(agent, TrafficLightAgent)), None)

            if traffic_light_next:
                # Obtener la posición dos pasos adelante en la misma dirección
                direction = (next_pos[0] - self.current_pos[0], next_pos[1] - self.current_pos[1])
                double_step_pos = (next_pos[0] + direction[0], next_pos[1] + direction[1])

                if self.can_move_to(double_step_pos):
                    # Realizar el salto de dos pasos
                    self.model.grid.move_agent(self, double_step_pos)
                    self.current_pos = double_step_pos
                    return  # Terminar el movimiento aquí

            # Movimiento normal de un paso si no puede hacer el salto
            if self.can_move_to(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.current_pos = next_pos
            else:
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
            if not self.crossing:
                # Movimiento aleatorio si no está esperando
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
