import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np
from boids import Boid
from scipy.spatial import KDTree
from predator import Predator

class Simulation():
    def __init__(self, window, margin, nr_agents, render_screen, run_for_ticks = None, param_set = None):
        self.window = window
        self.margin = margin
        self.nr_agents = nr_agents
        self.render_screen = render_screen
        self.run_for_ticks = run_for_ticks
        
        self.draw_fps = True
        self.log_to_console = True
        self.max_fps = 120 # werkt alleen als je de boel gaat renderen

        self.boids =  [Boid(window,margin) for _ in range(nr_agents)]
        self.predator = Predator(window)
        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])
        self.tick = 0 

        if param_set == None:
            self.separation_factor = 0.039
            self.alignment_factor = 0.5
            self.cohesion_factor = 0.002
            self.turnfactor = 100
            self.visual_range = 25
        else:
            self.separation_factor = param_set[0]
            self.alignment_factor = param_set[1]
            self.cohesion_factor = param_set[2]
            self.turnfactor = param_set[3]
            self.visual_range = param_set[4]

        if render_screen: # voor als je de zooi wil zien op een scherm
            self.init_graphics()

    def run(self):
        while self.run_for_ticks == None or self.tick < self.run_for_ticks: # ga oneindig door
            self.update()
            if self.render_screen:
                self.render()
        return self.nr_agents

    def init_graphics(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        pygame.display.set_caption("Predator Prey Simulation")
        self.clock = pygame.time.Clock()  # create pygame clock object 
        self.font = pygame.font.Font(None, 18)  # Create a font object

    def update(self):
        self.predator.uptate(self.window, 50, self.kdtree, self.boids)
        self.nr_agents = len(self.boids)
        
        if self.nr_agents == 0:
            # alles weg
            return self.tick
        
        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])            
        
        for boid in self.boids:
            boid.update(self.window, self.turnfactor, self.separation_factor, self.cohesion_factor, self.alignment_factor, self.kdtree, self.boids, self.visual_range, self.predator, self.predator.predation_detected)
        
        # logging
        if self.log_to_console and self.tick % 100 == 0:
            print(f'tick {self.tick}: nr_boids={self.nr_agents}')
        self.tick += 1

    def render(self):
        # begin mooie spaghetti hehe
        events = pygame.event.get()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame_widgets.update(events)
        # einde spaghetti

        # nu drawen
        self.screen.fill((255, 255, 255))          
        
        for boid in self.boids:
            pygame.draw.polygon(self.screen, 'red', boid.draw_triangle())
            
        pygame.draw.polygon(self.screen, 'blue', self.predator.draw_triangle())
        pygame.draw.circle(self.screen, 'green', self.predator.centroid, 5)

        if self.draw_fps:
            fps = int(self.clock.get_fps())
            text_2 = self.font.render(f'fps: {fps}', True, (0, 0, 0))
            self.screen.blit(text_2, (5, 5))

        pygame.display.update()
        
        self.clock.tick(self.max_fps) # voor het regelen van fps

