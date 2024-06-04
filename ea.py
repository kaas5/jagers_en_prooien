from simulation import Simulation
import random
import numpy as np
import time

import multiprocessing as mp

class EA:

    def fitness(param_set, q):
        nr_prey = 20
        predator_strategy = 'strat1'
        #obstacle_positions = [(200, 200), (100, 400), (400, 400), (400, 100)]  # Obstacle positions
        #obstacle_radii = [50, 50, 50, 50]  # Obstacle radii
        obstacle_positions = None
        obstacle_radii = None



        window = (500, 500)
        margin =   420
        render_screen = False
        log_to_console = False
        run_for_ticks = 5000
        simulation = Simulation(window, margin, nr_prey, predator_strategy=predator_strategy, 
                                obstacle_positions=obstacle_positions, obstacle_radii=obstacle_radii,
                                param_set=param_set, 
                                render_screen=render_screen, log_to_console=log_to_console, run_for_ticks=run_for_ticks)
        fitness = simulation.run()
        q.put_nowait(fitness)
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
    
    @staticmethod
    def select_parents(population, scores, num_parents):
        parents = list(zip(population, scores))
        parents.sort(key=lambda x: x[1], reverse=True)  # Higher fitness is better
        selected_parents = [parents[i][0] for i in range(num_parents)]
        return selected_parents
    
    @staticmethod
    def crossover(parents, offspring_size):
        offspring = []
        num_parents = len(parents)
        for k in range(offspring_size):
            parent1_index = k % num_parents
            parent2_index = (k + 1) % num_parents
            parent1 = parents[parent1_index]
            parent2 = parents[parent2_index]
            child = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]
            offspring.append(child)
        return offspring
    
    @staticmethod
    def mutate(offspring, sd, mutation_rate=0.2):
        for individual in offspring:
            for i in range(len(individual)):
                if random.random() < mutation_rate:
                    if i < 3:
                        individual[i] += np.random.normal(individual[i], sd[i])
                        individual[i] = max(0, min(1, individual[i]))
                    else:
                        individual[i] += np.random.normal(individual[i], sd[i])
                        individual[i] = max(0, min(100, individual[i]))
        return offspring

    @staticmethod
    def get_sd(population):
        res = []
        for i in range(len(population[0])):
            l = []
            for individual in population:
                l.append(individual[i])
            res.append(np.std(l))
        return res

    @staticmethod
    def mutate2(offspring, covmat, mutation_rate=0.5):
        for individual in offspring:
            for i in range(len(individual)):
                if random.random() < mutation_rate:

                    hoi = np.random.multivariate_normal(individual, covmat)
                    individual[i] = hoi[i]
                    if i < 3:
                        individual[i] = max(0, min(1, individual[i]))
                    else:
                        individual[i] = max(0, min(100, individual[i]))
        return offspring

    @staticmethod
    def get_sd2(population):
        bla = np.array(population)
        covmat = np.cov(bla, rowvar=False)
        return covmat

    @staticmethod
    def ea(population_size, generations, selection):
        population = EA.init_population(population_size)
        out_filename = f'out/scores_{int(time.time())}.txt'
        best_params = None
        best_score = float('-inf')

        for generation in range(generations):
            scores = []
            print(f"Generation {generation}")
            for individual in population:
                
                q = mp.Queue()
                processpool_size = 5
                processes = []
                
                for _ in range(processpool_size):
                    processes.append(mp.Process(target=EA.fitness, args=(individual, q)))
                    processes[-1].start()

                accum = 0
                for t in processes:
                    t.join()
                    accum += q.get_nowait()

                avg_score = accum / processpool_size
                scores.append(avg_score)
            
            best_generation_score = max(scores)
            best_generation_params = population[np.argmax(scores)]
            print(f"Best scores: {sorted(scores, reverse=True)[:selection]}")
            with open(out_filename, 'a') as f:
                f.write(f'{generation},{best_generation_score},{sum(scores) / len(scores)}\n')            

            if best_generation_score > best_score:
                best_score = best_generation_score
                best_params = best_generation_params
            
            sd = EA.get_sd2(population)
            print(sd)
            print('bestetot nu toe', best_score, best_params)
            best_individuals = EA.select_parents(population, scores, selection)
            offspring_size = population_size - selection
            offspring = EA.crossover(best_individuals, offspring_size)
            offspring = EA.mutate2(offspring, sd)
            population = best_individuals + offspring

        return best_params, best_score
    
if __name__ == "__main__":
    nr_agents = 10
    generations = 5
    selection = 3
    best_params, best_score = EA.ea(nr_agents, generations, selection)
    print(f"Best parameters: {best_params}")
    print(f"Best score: {best_score}")