import mesa

class TrafficLight(mesa.Agent):
    def __init__(self, model, direction):
        super().__init__(model)
        self.direction = direction  # e.g., "left", "right", "up", "down"