from boids import Boid
from simulation import Simulation
import random
import numpy as np

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

population = []

if __name__ == "__main__":
    window = (500, 500)
    margin =   420
    nr_agents = 200
    render_screen = True
    take_screenshots = False
    log_to_console = True
    run_for_ticks = None
    max_fps=120
    
    obstacle_positions = [(250, 250)]#[(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
    obstacle_radii = [200]#[50, 50, 50, 50]  # Obstacle radii

    #obstacle_positions = [(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
    #obstacle_radii = [50, 50, 50, 50]  # Obstacle radii

    simulation = Simulation(window, margin, nr_agents, render_screen, 
                            obstacle_positions=obstacle_positions, obstacle_radii=obstacle_radii, take_screenshots=take_screenshots,
                            run_for_ticks = run_for_ticks, param_set = None, max_fps=max_fps, log_to_console=log_to_console)
    simulation.run()

    #population = init_population(50)
    #ea(population)
    
    # dit is een parameterset gevonden door ea (predator strat 3)
    #fitness([0.45032842831746867, 0.9974261280840703, 0.385890816004285, 15.017958115507913])

    #fitness([0.5578438491551201, 0.6380603538167519, 0.05248130582120869, 49.47000131049404])
