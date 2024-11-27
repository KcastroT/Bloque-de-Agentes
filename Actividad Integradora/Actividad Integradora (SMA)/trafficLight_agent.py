from mesa import Agent

class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, color="green"):
        super().__init__(unique_id, model)
        self.color = color
        self.timer = 0
        self.green_duration = 8
        self.red_duration = 10

    def can_pedestrian_cross(self):
        # Suponiendo que cuando el semáforo está en rojo para coches, está en verde para peatones
        return self.color == "red"

    def step(self):
        self.timer += 1
        if self.color == "green" and self.timer >= self.green_duration:
            self.color = "red"
            self.timer = 0
        elif self.color == "red" and self.timer >= self.red_duration:
            self.color = "green"
            self.timer = 0