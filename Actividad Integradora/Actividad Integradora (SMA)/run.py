from ModeloTrafico import TrafficModel
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from car_agent import CarAgent
from building_agent import BuildingAgent
from trafficLight_agent import TrafficLightAgent
from parkingLot_Agent import ParkingLotAgent
from verticalRidge_agent import VerticalRidgeAgent
from horizontalRidge_agent import HorizontalRidgeAgent

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