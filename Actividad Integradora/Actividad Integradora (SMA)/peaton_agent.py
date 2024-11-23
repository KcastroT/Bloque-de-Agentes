from mesa import Agent
import random
from collections import deque

class PedestrianAgent(Agent):
    """Agente que representa a un peatón que se mueve a lo largo de caminos predefinidos."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.destination = None
        self.path = []

    def step(self):
        if not self.path:
            self.set_new_destination()

        if self.path:
            next_pos = self.path.pop(0)
            # Verificar si la posición está libre
            cellmates = self.model.grid.get_cell_list_contents([next_pos])
            if any(isinstance(agent, PedestrianAgent) for agent in cellmates):
                # No puede moverse; esperar o recalcular
                self.path = []
            else:
                self.model.grid.move_agent(self, next_pos)
        else:
            # No hay camino disponible; esperar o buscar nuevo destino
            pass

    def set_new_destination(self):
        # Escoger un destino aleatorio diferente a la posición actual
        possible_destinations = list(self.model.pedestrian_walkable_positions - {self.pos})
        if possible_destinations:
            self.destination = random.choice(possible_destinations)
            self.path = self.bfs_shortest_path(self.pos, self.destination)
        else:
            self.destination = self.pos
            self.path = []

    def bfs_shortest_path(self, start, goal):
        adjacency = self.model.pedestrian_adjacency
        queue = deque()
        queue.append((start, [start]))
        visited = set()
        visited.add(start)
        while queue:
            current_position, path = queue.popleft()
            if current_position == goal:
                return path[1:]  # Excluir la posición actual
            for neighbor in adjacency.get(current_position, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []  # No se encontró camino
