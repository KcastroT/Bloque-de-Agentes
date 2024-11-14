import solara
from mesa.visualization import SolaraViz, make_space_component
from model.ciudad_modelo import CiudadModelo
from visualization.visualization import agent_portrayal

SpaceGraph = make_space_component(agent_portrayal)
model_instance = CiudadModelo(n=10, width=24, height=24)

page = SolaraViz(
    model_instance,
    components=[SpaceGraph],
    name="Simulación de Ciudad con Autos"
)