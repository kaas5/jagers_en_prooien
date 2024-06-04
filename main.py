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

    params = [0.5788127947585386, 0.2457762774523715, 0.5377364142585395, 83.47942892085453] # beste voor strat1 en (0,1; 0,1; 0,1; 0,100) paraminterval

    # 1e pogingen
    params = [0.0851232609321712, 0.016998488672687596, 0.08680035861522738, 70.80971481930916] # beste voor strat1 en (0,.1; 0,1; 0,.1; 0,100) paraminterval
    params = [0.0705874255870059, 0.38190287786556054, 0.0700662020592468, 66.66784081807292] # beste voor strat3 en (0,.1; 0,1; 0,.1; 0,100) paraminterval

    # 2e pogingen
    params = [0.058484415168636054, 0.2726436335765634, 0.0583633101801989, 78.549701308815] # beste voor strat1 en (0,.1; 0,1; 0,.1; 0,100) paraminterval
    params = [0.036144750344737554, 0.3352422452549675, 0.03580813075193681, 47.422502543158444] # beste voor strat3 en (0,.1; 0,1; 0,.1; 0,100) paraminterval
    #params = None



    simulation = Simulation(window, margin, nr_agents, render_screen, 
                            obstacle_positions=obstacle_positions, obstacle_radii=obstacle_radii, take_screenshots=take_screenshots,
                            run_for_ticks = run_for_ticks, param_set = params, max_fps=max_fps, log_to_console=log_to_console)
    simulation.run()

if __name__ == "__main__":
    #do_iets()
    do_ea()
