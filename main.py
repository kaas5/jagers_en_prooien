from boids import Boid
from simulation import Simulation
from ea import EA
import random
import numpy as np

import os
os.environ['SDL_AUDIODRIVER'] = 'directx'

def do_ea():
    population_size = 50
    generations = 10
    selection = 5
    best_params, best_score = EA.ea(population_size, generations, selection)
    print(f"Best parameters: {best_params}")
    print(f"Best score: {best_score}")


def do_iets():
    window = (500, 500)
    margin =   420
    nr_agents = 20
    render_screen = True
    take_screenshots = False
    log_to_console = True
    run_for_ticks = None
    max_fps=120
    
    #obstacle_positions = [(250, 250)]#[(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
    #obstacle_radii = [200]#[50, 50, 50, 50]  # Obstacle radii

    #obstacle_positions = [(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
    #obstacle_radii = [50, 50, 50, 50]  # Obstacle radii

    obstacle_positions = None
    obstacle_radii = None

    #params = [0.3960813864618293, 0.35390929788813874, 0.7653877011377689, 65.48370666069839]
    #params = [0.511976052604978,  0.6345727757488085,  0.6603680719815939, 70.61169784812101]
    params = [0.07418464119893287, 0.5633488593935208, 0.012327049680472046, 61.01179559354861]
    params =  [0.6259512077058313, 0.5927905302925731, 0.3823014073924705, 59.48995404592102]
    #params = None
    simulation = Simulation(window, margin, nr_agents, render_screen, 
                            obstacle_positions=obstacle_positions, obstacle_radii=obstacle_radii, take_screenshots=take_screenshots,
                            run_for_ticks = run_for_ticks, param_set = params, max_fps=max_fps, log_to_console=log_to_console)
    simulation.run()

if __name__ == "__main__":
    #do_iets()
    do_ea()
