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

    def step(self):
        if self.reached_destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        if not self.path:
            self.path = self.find_path(self.start, self.destination)

        if not self.path:  # No valid path found, move randomly
            self.move_randomly()
        else:
            next_pos = self.path.pop(0)

            # If the next position is blocked (such as by a ridge), recalculate the path
            if not self.can_move_to(next_pos):
                self.path = self.find_path(self.pos, self.destination)
                return  # Exit this step to allow the recalculation to happen

            # Move to the next valid position
            if self.can_move_to(next_pos):
                self.model.grid.move_agent(self, next_pos)
                self.previous_position = self.pos
                self.visited_positions.add(self.pos)
                self.steps_since_move = 0  # Reset step counter since car moved

        if self.pos == self.destination:
            self.reached_destination = True

        # If the car hasn't moved for too many steps, recalculate the path
        self.steps_since_move += 1
        if self.steps_since_move > 20:  # Adjust the threshold as needed
            self.recalculate_path()
            self.steps_since_move = 0

    def can_move_to(self, position):
        """Check if the car can move to the given position."""
        cellmates = self.model.grid.get_cell_list_contents([position])

        # Avoid crossing ridges (horizontal or vertical)
        for agent in cellmates:
            if isinstance(agent, VerticalRidgeAgent):
                # Block horizontal movement across vertical ridges
                if self.pos[0] != position[0]:  # if moving horizontally
                    return False
            if isinstance(agent, HorizontalRidgeAgent):
                # Block vertical movement across horizontal ridges
                if self.pos[1] != position[1]:  # if moving vertically
                    return False

        # Block if there's a building or another car in the way
        if any(isinstance(agent, (BuildingAgent, CarAgent)) for agent in cellmates):
            return False

        # Block if the traffic light is red
        for agent in cellmates:
            if isinstance(agent, TrafficLightAgent) and agent.color == "red":
                return False

        return True

    def move_randomly(self):
        """Move to a random valid neighboring cell if no path is available."""
        neighbors = self.get_neighbors(self.pos)
        valid_moves = [pos for pos in neighbors if self.can_move_to(pos) and pos != self.previous_position]
        if valid_moves:
            self.model.grid.move_agent(self, random.choice(valid_moves))
            self.previous_position = self.pos
            self.visited_positions.add(self.pos)

    def get_neighbors(self, position):
        """Returns valid neighboring positions."""
        neighbors = []
        x, y = position
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in possible_moves:
            if 0 <= nx < self.model.grid.width and 0 <= ny < self.model.grid.height:
                cellmates = self.model.grid.get_cell_list_contents([(nx, ny)])
                if all(not isinstance(agent, (BuildingAgent, CarAgent)) for agent in cellmates):
                    neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start, destination):
        """Uses A* to find the shortest path to the destination."""
        grid = self.model.grid
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, destination)}

        while open_set:
            _, current = heappop(open_set)

            if current == destination:
                return self.reconstruct_path(came_from, current)

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                # Skip neighbors that are blocked (such as by ridges)
                if not self.can_move_to(neighbor):
                    continue
                
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, destination)
                    if neighbor not in [i[1] for i in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No valid path found

    def heuristic(self, a, b):
        """Heuristic function for A* (Manhattan distance)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        """Reconstructs the path from A*."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def recalculate_path(self):
        """Recalculate the path to avoid getting stuck."""
        self.path = self.find_path(self.pos, self.destination)
    def __init__(self, unique_id, model, start, destination):
        super().__init__(unique_id, model)
        self.start = start
        self.destination = destination
        self.path = []
        self.reached_destination = False
        self.previous_position = None
        self.visited_positions = set()
        self.loop_detection = set()  # Track positions visited recently to avoid loops
        self.steps_since_move = 0

    def step(self):
        if self.reached_destination:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            return

        if not self.path:
            self.path = self.find_path(self.start, self.destination)

        if not self.path:  
            self.move_randomly()
        else:
            next_pos = self.path.pop(0)

            
            if next_pos in self.loop_detection:
                self.reset_path()  
                self.move_randomly()  
                return


            if next_pos == self.previous_position:
                self.move_randomly()
            else:
                if self.can_move_to(next_pos):
                    self.model.grid.move_agent(self, next_pos)
                    self.visited_positions.add(self.pos)
                    self.previous_position = self.pos
                    self.loop_detection.add(self.pos)  
                    self.steps_since_move = 0  
                else:
                    self.path = self.find_path(self.pos, self.destination)  

        if self.pos == self.destination:
            self.reached_destination = True


        self.steps_since_move += 1
        if self.steps_since_move > 10:  
            self.recalculate_path() 
            self.steps_since_move = 0

    def can_move_to(self, position):
        """Check if the car can move to the given position."""
        cellmates = self.model.grid.get_cell_list_contents([position])

        if any(isinstance(agent, (BuildingAgent, CarAgent,VerticalRidgeAgent,HorizontalRidgeAgent)) for agent in cellmates):
            return False

        # Block if the traffic light is red
        for agent in cellmates:
            if isinstance(agent, TrafficLightAgent) and agent.color == "red":
                return False

        return True

    def move_randomly(self):
        """Move to a random valid neighboring cell if no path is available."""
        neighbors = self.get_neighbors(self.pos)
        valid_moves = [pos for pos in neighbors if self.can_move_to(pos) and pos != self.previous_position]
        if valid_moves:
            self.model.grid.move_agent(self, random.choice(valid_moves))
            self.previous_position = self.pos
            self.visited_positions.add(self.pos)

    def get_neighbors(self, position):
        """Returns valid neighboring positions."""
        neighbors = []
        x, y = position
        possible_moves = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in possible_moves:
            if 0 <= nx < self.model.grid.width and 0 <= ny < self.model.grid.height:
                cellmates = self.model.grid.get_cell_list_contents([(nx, ny)])
                if all(not isinstance(agent, (BuildingAgent, CarAgent,VerticalRidgeAgent,HorizontalRidgeAgent)) for agent in cellmates):
                    neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start, destination):

        grid = self.model.grid
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, destination)}

        while open_set:
            _, current = heappop(open_set)

            if current == destination:
                return self.reconstruct_path(came_from, current)

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                # Skip neighbors that are in the loop detection set (indicating a loop)
                if neighbor in self.loop_detection:
                    continue
                
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, destination)
                    if neighbor not in [i[1] for i in open_set]:
                        heappush(open_set, (f_score[neighbor], neighbor))

        return []  # No valid path found

    def heuristic(self, a, b):
        """Heuristic function for A* (Manhattan distance)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        """Reconstructs the path from A*."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def recalculate_path(self):
        """Recalculate the path to avoid getting stuck."""
        self.path = self.find_path(self.pos, self.destination)
        self.loop_detection.clear()  # Clear the loop detection set