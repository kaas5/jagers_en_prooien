from simulation import Simulation
import random

class EA:
    def fitness(param_set):
        window = (500, 500)
        margin =   420
        nr_agents = 20
        render_screen = True
        log_to_console = False
        run_for_ticks = 5000
        max_fps=120
        print(param_set)
        simulation = Simulation(window, margin, nr_agents, render_screen, run_for_ticks = run_for_ticks, param_set = param_set, max_fps=max_fps, log_to_console=log_to_console)
        fitness = simulation.run()
        return fitness

    def init_population(N):
        population = []
        for _ in range(N):
            """ self.separation_factor = param_set[0]
                self.alignment_factor = param_set[1]
                self.cohesion_factor = param_set[2]
                self.visual_range = param_set[4]"""
            individual = [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1),random.uniform(0,100)]
            population.append(individual)
        return population

    def ea(population):
        scores = []

        for individual in population:
            scores.append(fitness(individual))

        a = np.array(scores)
        index = np.argmax(a)
        print('de beste', population[index], scores[index])