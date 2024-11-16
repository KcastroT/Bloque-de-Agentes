import mesa

class CarAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        x, y = self.random.randint(0, model.grid.width - 1), self.random.randint(0, model.grid.height - 1)
        self.model.grid.place_agent(self, (x, y))

    def step(self):
        self.avanzar()

    def avanzar(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)