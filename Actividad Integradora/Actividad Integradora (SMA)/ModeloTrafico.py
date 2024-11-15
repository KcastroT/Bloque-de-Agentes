import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from mesa import Agent, Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from heapq import heappush, heappop
import random


# Define Agent Types
class BuildingAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, color="green"):
        super().__init__(unique_id, model)
        self.color = color
        self.timer = 0
        self.green_duration = 8
        self.red_duration = 10

    def step(self):
        self.timer += 1
        if self.color == "green" and self.timer >= self.green_duration:
            self.color = "red"
            self.timer = 0
        elif self.color == "red" and self.timer >= self.red_duration:
            self.color = "green"
            self.timer = 0

class ParkingLotAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class VerticalRidgeAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class HorizontalRidgeAgent(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass


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
class TrafficModel(Model):
    def __init__(self, width, height):
        super().__init__()
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)

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

        # Adding parking lots
        self.parking_lot_positions = [(4,4),(8,9),(2,8),(4,11),(9,2),(11,6),(10,11),(17,2),(18,11),(20,8),(20,5),(3,17),(10,16),(4,20),(9,21),(17,17),(21,20)]
        for i, pos in enumerate(self.parking_lot_positions):
            parking_lot = ParkingLotAgent(f"parking_{i}", self)
            self.grid.place_agent(parking_lot, pos)
            self.schedule.add(parking_lot)

        occupied_parking_lots = set()  # Track which parking lots are occupied

        for i in range(5):  # Spawn 5 cars

            available_parking_lots = [pos for pos in self.parking_lot_positions if pos not in occupied_parking_lots]
        
            if not available_parking_lots:
                break
            start = random.choice(available_parking_lots)
            occupied_parking_lots.add(start)
            destination = random.choice([pos for pos in self.parking_lot_positions if pos != start])
            
            # Create the car agent and place it on the grid
            car = CarAgent(f"car_{i}", self, start, destination)
            self.grid.place_agent(car, start)
            self.schedule.add(car)

            self.add_ridges()
    
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

    def step(self):
        self.schedule.step()



def render(ax):
    """Render the model on the given Matplotlib Axes."""
    ax.clear()  # Clear the previous frame
    ax.set_xlim(0, model.grid.width)
    ax.set_ylim(0, model.grid.height)

    # Draw the grid and agents
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            ax.add_patch(Rectangle((x, y), 1, 1, edgecolor="gray", facecolor="white"))

    for agent in model.schedule.agents:
        if isinstance(agent, CarAgent) and agent.reached_destination:
            continue  # Don't render cars that have despawned
        x, y = agent.pos
        if isinstance(agent, BuildingAgent):
            ax.add_patch(Rectangle((x, y), 1, 1, color="blue"))
        elif isinstance(agent, TrafficLightAgent):
            color = "green" if agent.color == "green" else "red"
            ax.add_patch(Rectangle((x, y), 1, 1, color=color))
        elif isinstance(agent, ParkingLotAgent):
            ax.add_patch(Rectangle((x, y), 1, 1, color="yellow"))
        elif isinstance(agent, CarAgent):
            ax.add_patch(Rectangle((x, y), 1, 1, color="black"))
        elif isinstance(agent, VerticalRidgeAgent):
            ax.add_patch(Rectangle((x, y), 0.3, 1, color="brown"))
        elif isinstance(agent, HorizontalRidgeAgent):
            ax.add_patch(Rectangle((x, y), 1, 0.3, color="brown"))

    ax.set_xticks(range(model.grid.width + 1))
    ax.set_yticks(range(model.grid.height + 1))
    ax.grid(True)
    ax.invert_yaxis()


def update(frame):
    """Update function for FuncAnimation."""
    model.step()  
    render(ax)    


def render_model():
    """Set up and run the animation."""
    global fig, ax
    fig, ax = plt.subplots(figsize=(8, 8))  

    render(ax)
    plt.draw() 


    anim = FuncAnimation(
        fig, update, frames=100, interval=500, repeat=False, blit=False
    )  
    plt.show()



model = TrafficModel(width=24, height=24)
render_model()