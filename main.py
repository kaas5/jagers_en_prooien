from boids import Boid
from simulation import Simulation

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

population = []

def fitness(param_set):
    simulation = Simulation(window, margin, nr_agents, render_screen, run_for_ticks = 1000, param_set = param_set)
    fitness = simulation.run()
    
    return

if __name__ == "__main__":
    window = (250, 250)
    margin =   420
    nr_agents = 3
    render_screen = True
    simulation = Simulation(window, margin, nr_agents, render_screen, run_for_ticks = 1000)
    simulation.run()
