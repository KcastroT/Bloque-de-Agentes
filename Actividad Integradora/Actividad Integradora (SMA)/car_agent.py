from mesa import Agent
from heapq import heappush, heappop
import random
from horizontalRidge_agent import HorizontalRidgeAgent
from verticalRidge_agent import VerticalRidgeAgent
from building_agent import BuildingAgent
from trafficLight_agent import TrafficLightAgent

class CarAgent(Agent):
    def __init__(self, unique_id, model, start, destination):
        super().__init__(unique_id, model)
        self.start = start
        self.destination = destination
        self.path = []
        self.reached_destination = False
        self.previous_position = None
        self.visited_positions = set()
        self.steps_since_move = 0
        self.intersections_graph = {
            # Dos carriles izquierdos
            (0,0): [(0,1)],
            (0,1): [(0,2)],
            (0,2): [(0,3)],
            (0,3): [(0,4)],
            (0,4): [(0,5)],
            (0,5): [(0,6)],
            (0,6): [(0,7)],
            (0,7): [(0,8)],
            (0,8): [(0,9), (1,8)], # Estacionamiento
            (0,9): [(0,10)],
            (0,10): [(0,11)],
            (0,11): [(0,12)],
            (0,12): [(0,13)],
            (0,13): [(0,14)],
            (0,14): [(0,15), (1,14)], # Esquina
            (0,15): [(0,16), (1,15)], # Esquina
            (0,16): [(0,17)],
            (0,17): [(0,18)],
            (0,18): [(0,19), (1,18)], # Esquina
            (0,19): [(0,20), (1,19)], # Esquina
            (0,20): [(0,21)],
            (0,21): [(0,22)],
            (0,22): [(0,23), (1,22)], # Esquina
            (0,23): [(1,23)], # Esquina Inferior
            (1,0): [(1,1)],
            (1,1): [(1,2)],
            (1,2): [(1,3)],
            (1,3): [(1,4)],
            (1,4): [(1,5)],
            (1,5): [(1,6)],
            (1,6): [(1,7)],
            (1,7): [(1,8)],
            (1,8): [(1,9), (2,8)], # Estacionamiento
            (1,9): [(1,10)],
            (1,10): [(1,11)],
            (1,11): [(1,12)],
            (1,12): [(1,13)],
            (1,13): [(1,14)],
            (1,14): [(1,15), (2,14)], # Esquina
            (1,15): [(1,16), (2,15)], # Esquina
            (1,16): [(1,17)],
            (1,17): [(1,18)],
            (1,18): [(1,19), (2,18)], # Esquina
            (1,19): [(1,20), (2,19)], # Esquina
            (1,20): [(1,21)],
            (1,21): [(1,22)],
            (1,22): [(1,23), (2,22)], # Esquina
            (1,23): [(2,23)], # Esquina Inferior
            
            # Dos carriles inferiores
            (2,22): [(3,22)],
            (2,23): [(3,23)],

            (3,22): [(4,22)],
            (3,23): [(4,23)],

            (4,22): [(5,22)],
            (4,23): [(5,23)],

            (5,22): [(6,22)],
            (5,23): [(6,23)],

            (6,22): [(7,22)],
            (6,23): [(7,23)],
            
            (7,22): [(8,22)],
            (7,23): [(8,23)],

            (8,22): [(9,22)],
            (8,23): [(9,23)],

            (9,22): [(10,22), (9,21)], # Estacionamiento
            (9,23): [(9,22), (10,23)],

            (10,22): [(11,22)],
            (10,23): [(11,23)],
            
            (11,22): [(12,22)],
            (11,23): [(12,23)],

            (12,22): [(13,22)],
            (12,23): [(13,23)],

            (13,22): [(14,22)],
            (13,23): [(14,23)],

            (14,22): [(15,22), (14,21)], # Esquina
            (14,23): [(15,23), (14,22)], # Esquina

            (15,22): [(16,22), (15,21)], # Esquina
            (15,23): [(16,23), (15,22)], # Esquina

            (16,22): [(17,22)],
            (16,23): [(17,23)],

            (17,22): [(18,22)],
            (17,23): [(18,23)],

            (18,22): [(19,22)],
            (18,23): [(19,23)],

            (19,22): [(20,22)],
            (19,23): [(20,23)],

            (20,22): [(21,22)],
            (20,23): [(21,23)],

            (21,22): [(22,22)],
            (21,23): [(22,23)],

            (22,22): [(23,22), (22,21)], # Esquina
            (22,23): [(23,23), (22,22)], # Esquina

            (23,22): [(23,21)], # Esquina Inferior
            (23,23): [(23,22)], # Esquina Inferior

            # Dos carriles derechos
            (22,21): [(22,20)],
            (23,21): [(23,20)],

            (22,20): [(22,19), (21,20)], # Estacionamiento
            (23,20): [(23,19), (22,20)], # Estacionamiento

            (22,19): [(22,18), (21,19)], # Esquina
            (23,19): [(23,18), (22,19)], # Esquina

            (22,18): [(22,17), (21,18)], # Esquina
            (23,18): [(23,17), (22,18)], # Esquina
            
            (22,17): [(22,16)],
            (23,17): [(23,16)],

            (22,16): [(22,15)],
            (23,16): [(23,15)],

            (22,15): [(22,14)],
            (23,15): [(23,14)],

            (22,14): [(22,13)],
            (23,14): [(23,13)],

            (22,13): [(22,12), (21,13)], # Esquina
            (23,13): [(23,12), (22,13)], # Esquina

            (22,12): [(22,11), (21,12)], # Esquina
            (23,12): [(23,11), (22,12)], # Esquina

            (22,11): [(22,10)],
            (23,11): [(23,10)],

            (22,10): [(22,9)],
            (23,10): [(23,9)],

            (22,9): [(22,8)],
            (23,9): [(23,8)],

            (22,8): [(22,7)],
            (23,8): [(23,7)],

            (22,7): [(22,6)],
            (23,7): [(23,6)],

            (22,6): [(22,5)],
            (23,6): [(23,5)],

            (22,5): [(22,4)],
            (23,5): [(23,4)],

            (22,4): [(22,3)],
            (23,4): [(23,3)],

            (22,3): [(22,2)],
            (23,3): [(23,2)],

            (22,2): [(22,1)],
            (23,2): [(23,1)],

            (22,1): [(22,0), (21,1)], # Esquina
            (23,1): [(23,0), (22,1)], # Esquina

            (22,0): [(21,0)], # Esquina Superior
            (23,0): [(22,0)], # Esquina Superior

            # Dos carriles superiores
            (21,0): [(20,0)],
            (21,1): [(20,1)],

            (20,0): [(19,0)],
            (20,1): [(19,1)],

            (19,0): [(18,0)],
            (19,1): [(18,1)],

            (18,0): [(17,0)],
            (18,1): [(17,1)],

            (17,0): [(16,0), (17,1)], # Estacionamiento
            (17,1): [(16,1), (17,2)], # Estacionamiento

            (16,0): [(15,0)],
            (16,1): [(15,1)],

            (15,0): [(14,0)],
            (15,1): [(14,1)],

            (14,0): [(13,0)],
            (14,1): [(13,1)],

            (13,0): [(12,0), (13,1)], # Interseccion
            (13,1): [(12,1), (13,2)], # Interseccion

            (12,0): [(11,0), (12,1)], # Interseccion
            (12,1): [(11,1), (12,2)], # Interseccion

            (11,0): [(10,0)],
            (11,1): [(10,1)],

            (10,0): [(9,0), (10,1)], # Estacionamiento
            (10,1): [(9,1), (9,2)], #Estacionamiento

            (9,0): [(8,0)],
            (9,1): [(8,1)],

            (8,0): [(7,0)],
            (8,1): [(7,1)],

            (7,0): [(6,0), (7,1)], # Interseccion
            (7,1): [(6,1), (7,2)], # Interseccion

            (6,0): [(5,0), (6,1)], # Interseccion
            (6,1): [(5,1), (6,2)], # Interseccion

            (5,0): [(4,0)],
            (5,1): [(4,1)],

            (4,0): [(3,0)],
            (4,1): [(3,1)],

            (3,0): [(2,0)],
            (3,1): [(2,1)],

            (2,0): [(1,0)],
            (2,1): [(1,1)],

            # Parte central

            # Carriles horizontales
            # De izquierda a derecha
            # Carril inferior izquierdo
            (2,18): [(3,18)],
            (2,19): [(3,19)],

            (3,18): [(4,18), (3,17)], # Estacionamiento
            (3,19): [(4,19), (3,18)], # Estacionamiento

            (4,18): [(5,18), (4,19)], # Estacionamiento
            (4,19): [(5,19), (4,20)], # Estacionamiento

            (5,18): [(6,18)],
            (5,19): [(6,19)],

            (6,18): [(7,18)],
            (6,19): [(7,19)],

            (7,18): [(8,18)],
            (7,19): [(8,19)],

            (8,18): [(9,18)],
            (8,19): [(9,19)],

            (9,18): [(10,18)],
            (9,19): [(10,19)],

            (10,18): [(11,18)],
            (10,19): [(11,19)],

            (11,18): [(12,18)],
            (11,19): [(12,19)],

            # Carril medio izquierdo
            (2,14): [(3,14)],
            (2,15): [(3,15)],

            (3,14): [(4,14)],
            (3,15): [(4,15)],

            (4,14): [(5,14)],
            (4,15): [(5,15)],

            (5,14): [(6,14)],
            (5,15): [(6,15)],

            (6,14): [(7,14)],
            (6,15): [(7,15)],

            (7,14): [(8,14)],
            (7,15): [(8,15)],

            (8,14): [(9,14)],
            (8,15): [(9,15)],

            (9,14): [(10,14)],
            (9,15): [(10,15)],

            (10,14): [(11,14), (10,15)], # Estacionamiento
            (10,15): [(11,15), (10,16)], # Estacionamiento

            (11,14): [(12,14)],
            (11,15): [(12,15)],

            # Carril izquierdo pequeño superior de derecha a izquierda
            (5,5): [(4,5)],
            (5,6): [(4,6)],

            (4,5): [(3,5), (4,4)], # Estacionamiento
            (4,6): [(3,6), (4,5)], # Estacionamiento

            (3,5): [(2,5)],
            (3,6): [(2,6)],

            (2,5): [(1,5)],
            (2,6): [(1,6)],

            # Carril izquierdo de derecha a izquierda
            (11,12): [(10,12)],
            (11,13): [(10,13)],

            (10,12): [(9,12), (10,11)], # Estacionamiento
            (10,13): [(9,13), (10,12)], # Estacionamiento

            (9,12): [(8,12)],
            (9,13): [(8,13)],

            (8,12): [(7,12)],
            (8,13): [(7,13)],

            (7,12): [(6,12)],
            (7,13): [(6,13)],

            (6,12): [(5,12)],
            (6,13): [(5,13)],

            (5,12): [(4,12)],
            (5,13): [(4,13)],

            (4,12): [(3,12), (4,11)], # Estaionamiento
            (4,13): [(3,13), (4,12)], # Estacionamiento

            (3,12): [(2,12)],
            (3,13): [(2,13)],

            (2,12): [(1,12)],
            (2,13): [(1,13)],

            # Carril izquierdo de arriba a abajo
            (7,2): [(7,3)],
            (6,2): [(6,3)],

            (7,3): [(7,4)],
            (6,3): [(6,4)],

            (7,4): [(7,5)],
            (6,4): [(6,5)],

            (7,5): [(7,6), (6,5)], # Interseccion
            (6,5): [(6,6), (5,5)], # Interseccion

            (7,6): [(7,7), (6,6)], # Interseccion
            (6,6): [(6,7), (5,6)], # Interseccion

            (7,7): [(7,8)],
            (6,7): [(6,8)],

            (7,8): [(7,9)],
            (6,8): [(6,9)],

            (7,9): [(7,10), (8,9)], # Estacionamiento
            (6,9): [(6,10), (7,9)], # Estacionamiento

            (7,10): [(7,11)],
            (6,10): [(6,11)],

            (7,11): [(7,12)],
            (6,11): [(6,12)],

            # Carril medio de arriba a abajo
            (13,2): [(13,3)],
            (12,2): [(12,3)],

            (13,3): [(13,4)],
            (12,3): [(12,4)],
            
            (13,4): [(13,5)],
            (12,4): [(12,5)],

            (13,5): [(13,6)],
            (12,5): [(12,6)],

            (13,6): [(13,7), (12,6)], # Estacionamiento
            (12,6): [(12,7), (11,6)], # Estacionamiento

            (13,7): [(13,8)],
            (12,7): [(12,8)],

            (13,8): [(13,9)],
            (12,8): [(12,9)],

            (13,9): [(13,10)],
            (12,9): [(12,10)],

            (13,10): [(13,11)],
            (12,10): [(12,11)],

            (13,11): [(13,12)],
            (12,11): [(12,12)],

            (13,12): [(12,12)], # Rotonda/Glorieta
            (12,12): [(12,13), (11,12)], # Rotonda/Glorieta
            (12,13): [(12,14), (11,13)], # Rotonda/Glorieta

            (12,14): [(12,15)], # Rotonda/Glorieta
            (12,15): [(12,16), (13,15)], # Rotonda/Glorieta ##########

            (12,16): [(12,17)],
            (12,17): [(12,18)],
            (12,18): [(12,19)],
            (12,19): [(12,20)],
            (12,20): [(12,21)],
            (12,21): [(12,22)],
            
            (13,15): [(13,16), (14,15)], # Rotonda/Glorieta
            (13,16): [(13,17)],
            (13,17): [(13,18)],
            (13,18): [(13,19)],
            (13,19): [(13,20)],
            (13,20): [(13,21)],
            (13,21): [(13,22)],

            # Carril medio de abajo a arriba

            (14,21): [(14,20)],
            (14,20): [(14,19)],
            (14,19): [(14,18)],
            (14,18): [(14,17)],
            (14,17): [(14,16)],
            (14,16): [(14,15)],
            (14,15): [(15,15)], # Rotonda/Glorieta

            (15,21): [(15,20)],
            (15,20): [(15,19)],
            (15,19): [(15,18)],
            (15,18): [(15,17)],
            (15,17): [(15,16)],
            (15,16): [(15,15)],

            (15,15): [(16,15), (15,14)], # Rotonda/Glorieta
            (15,14): [(16,14), (15,13)], # Rotonda/Glorieta
            (15,13): [(15,12)], # Rotonda/Glorieta
            (15,12): [(15,11), (14,12)], # Rotonda/Glorieta
            (14,12): [(14,11)],

            (14,11): [(14,10)],
            (14,10): [(14,9)],
            (14,9): [(14,8)],
            (14,8): [(14,7)],
            (14,7): [(14,6), (15,7)], # Interseccion
            (14,6): [(14,5), (15,6)], # Interseccion
            (14,5): [(14,4)],
            (14,4): [(14,3)],
            (14,3): [(14,2)],
            (14,2): [(14,1)],

            (15,11): [(15,10)],
            (15,10): [(15,9)],
            (15,9): [(15,8)],
            (15,8): [(15,7)],
            (15,7): [(15,6), (16,7)], # Interseccion
            (15,6): [(15,5), (16,6)], # Interseccion
            (15,5): [(15,4)],
            (15,4): [(15,3)],
            (15,3): [(15,2)],
            (15,2): [(15,1)],


            # Carril arriba a la derecha de izquierda a derecha
            (16,7): [(17,7)],
            (16,6): [(17,6)],

            (17,7): [(18,7)],
            (17,6): [(18,6)],

            (18,7): [(19,7), (18,6)], # Interseccion
            (18,6): [(19,6), (18,5)], # Interseccion

            (19,7): [(20,7), (19,6)], # Interseccion
            (19,6): [(20,6), (19,5)], # Interseccion

            (20,7): [(21,7), (20,8), (20,6)], # Estacionamientos
            (20,6): [(21,6), (20,5)], # Estacionamientos

            (21,7): [(22,7)],
            (21,6): [(22,6)],

            (19,5): [(19,4), (20,5)], # Estacionamiento
            (18,5): [(18,4), (19,5)], # Estacionamiento

            (19,4): [(19,3)],
            (18,4): [(18,3)],

            (19,3): [(19,2)],
            (18,3): [(18,2)],

            (19,2): [(19,1)],
            (18,2): [(18,1)],

            # Carril central a la derecha de derecha a izquierda
            (21,12): [(20,12)],
            (21,13): [(20,13)],

            (20,12): [(19,12)],
            (20,13): [(19,13)],

            (19,12): [(18,12)],
            (19,13): [(18,13)],

            (18,12): [(17,12), (18,11)], # Estacionamiento
            (18,13): [(17,13), (18,12)], # Estacionamiento

            (17,12): [(16,12)],
            (17,13): [(16,13)],

            (16,12): [(15,12)],
            (16,13): [(15,13)],

            # Carril central a la derecha de izquierda a derecha
            (16,14): [(17,14)],
            (16,15): [(17,15)],

            (17,14): [(18,14)],
            (17,15): [(18,15)],

            (18,14): [(19,14), (18,15)], # Interseccion
            (18,15): [(19,15), (18,16)], # Interseccion

            (19,14): [(20,14), (19,15)], # Interseccion
            (19,15): [(20,15), (19,16)], # Interseccion

            (20,14): [(21,14)],
            (20,15): [(21,15)],

            (21,14): [(22,14)],
            (21,15): [(22,15)],
            
            # Carril vertical abajo a la derecha de arriba a abajo
            (18,16): [(18,17)],
            (19,16): [(19,17)],

            (18,17): [(18,18), (17,17)], # Estacionamiento
            (19,17): [(19,18), (18,17)], # Estacionamiento

            (21,18): [(20,18), (21,19)], # Estacionamiento
            (21,19): [(20,19), (21,20)], # Estacionamiento

            (20,18): [(19,18)],
            (20,19): [(19,19)],

            (19,18): [(18,18), (19,19)],
            (19,19): [(18,19), (19,20)],

            (18,18): [(17,18), (18,19)],
            (18,19): [(17,19), (18,20)],

            (17,18): [(16,18), (17,17)], # Estacionamiento
            (17,19): [(16,19)], # Estacionamiento

            (16,18): [(15,18)],
            (16,19): [(15,19)],

            (19,20): [(19,21)],
            (18,20): [(18,21)],

            (19,21): [(19,22)],
            (18,21): [(18,22)],

            # Salidas de los estacionamientos
            (17,2): [(17,1), (18,2)],
            (9,2): [(9,1)],
            (4,4): [(4,5)],
            (20,5): [(20,6), (19,5)],
            (11,6): [(12,6)],
            (2,8): [(1,8)],
            (20,8): [(20,7)],
            (8,9): [(7,9)],
            (4,11): [(4,12)],
            (10,11): [(10,12)],
            (18,11): [(18,12)],
            (10,16): [(10,15)],
            (3,17): [(3,18)],
            (17,17): [(17,18)],
            (4,20): [(4,19)],
            (21,20): [(21,19), (22,20)],
            (9,21): [(9,22)],
}

    def step(self):
        """
        Lógica principal del agente.
        """
        # Verificar si el agente ya alcanzó el destino
        if self.reached_destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        # Calcular la ruta si aún no existe
        if not self.path:
            self.path = self.find_path(self.pos, self.destination)

        # Si no se encuentra un camino, moverse aleatoriamente
        if not self.path:
            self.move_randomly()
            return

        # Tomar el siguiente nodo en el camino
        next_pos = self.path.pop(0)

        # Verificar si puede moverse a la posición
        if self.can_move_to(next_pos):
            self.model.grid.move_agent(self, next_pos)  # Mover el agente
        else:
            # Si no puede moverse, recalcular la ruta
            self.path = self.find_path(self.pos, self.destination)

        # Verificar si llegó al destino
        if self.pos == self.destination:
            self.reached_destination = True

    def can_move_to(self, position):
        """
        Verifica si el agente puede moverse a la posición dada.
        Evita chocar con otros carros y respeta semáforos en rojo.
        """
        cellmates = self.model.grid.get_cell_list_contents([position])
        # Bloquear si hay otro auto en la posición
        if any(isinstance(agent, CarAgent) for agent in cellmates):
            return False
        # Verificar si hay un semáforo en rojo en la posición
        for agent in cellmates:
            if isinstance(agent, TrafficLightAgent) and agent.color == "red":
                return False
        return True

    def find_path(self, start, destination):
        """
        Encuentra el camino más corto en el grafo usando BFS.
        """
        graph = self.intersections_graph

        # Verificar que los nodos existan en el grafo
        if start not in graph or destination not in graph:
            return []

        # Implementación de BFS
        from collections import deque
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            current_node = path[-1]

            if current_node == destination:
                return path[1:]  # Excluir la posición actual

            if current_node not in visited:
                visited.add(current_node)
                for neighbor in graph.get(current_node, []):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)

        return []

    def move_randomly(self):
        """
        Si no hay camino, moverse aleatoriamente.
        """
        neighbors = self.get_neighbors(self.pos)
        valid_moves = [pos for pos in neighbors if self.can_move_to(pos)]
        if valid_moves:
            next_move = random.choice(valid_moves)
            self.model.grid.move_agent(self, next_move)

    def get_neighbors(self, position):
        """
        Devuelve los vecinos válidos desde el grafo.
        """
        return self.intersections_graph.get(position, [])