from boids import Boid
from simulation import Simulation
from ea import EA
import random
import numpy as np

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

def execute_ea( population_size = 50,
                generations = 20,
                selection = 10):
    best_params, best_score = EA.ea(population_size, generations, selection)
    print(f"Best parameters: {best_params}")
    print(f"Best score: {best_score}")

def show_simulation():
    window = (500, 500)
    margin =   420
    nr_agents = 20
    render_screen = True
    take_screenshots = False
    log_to_console = True
    run_for_ticks = None
    max_fps=120

    #obstacle_positions = [(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
    #obstacle_radii = [50, 50, 50, 50]  # Obstacle radii
    obstacle_positions = None
    obstacle_radii = None

    #params = [0.5788127947585386, 0.2457762774523715, 0.5377364142585395, 83.47942892085453]
    params = None

    simulation = Simulation(window, margin, nr_agents, render_screen, 
                            obstacle_positions=obstacle_positions, obstacle_radii=obstacle_radii, take_screenshots=take_screenshots,
                            run_for_ticks = run_for_ticks, param_set = params, max_fps=max_fps, log_to_console=log_to_console)
    simulation.run()

if __name__ == "__main__":
    show_simulation()
    #execute_ea()
