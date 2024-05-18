from boids import Boid
from simulation import Simulation

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

time = 50
visual_range = 0
projected_range = 20
separation_factor = 0
alignment_factor = 0
cohesion_factor = 0
turnfactor = 0

if __name__ == "__main__":
    window = (250, 250)
    margin =   420
    simulation = Simulation(window, margin, 50)
    simulation.init_graphics() # voor als je de zooi wil zien op een scherm
    while True:
        simulation.update()
        simulation.render() # voor als je de zooi wil zien op een scherm
