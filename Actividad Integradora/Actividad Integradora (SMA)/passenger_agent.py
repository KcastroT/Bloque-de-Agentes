from mesa import Agent

class PassengerAgent(Agent):
    def __init__(self, unique_id, model, start_pos):
        super().__init__(unique_id, model)
        self.current_pos = start_pos
        self.waiting = True  # Passenger is waiting for a taxi

    def step(self):
        # Passenger does not move; waits for taxi
        pass
