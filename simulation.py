import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np
from boids import Boid
from scipy.spatial import KDTree
from predator import Predator

time = 120
class Simulation():
    def __init__(self, window, margin, Number_of_agents,
            separation_factor = 0.039,
            alignment_factor = 0.5,
            cohesion_factor = 0.002,
            turnfactor = 100,
            visual_range = 25,
        ):
        self.draw_fps = True
        self.log_to_console = True

        self.window = window
        self.margin = margin
        self.Number_of_agents = Number_of_agents

        self.boids =  [Boid(window,margin) for _ in range(Number_of_agents)]
        self.predator = Predator(window)
        self.update_tick = 0 

        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])

        self.separation_factor = separation_factor
        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor
        self.turnfactor = turnfactor
        self.visual_range = visual_range

    def init_graphics(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        pygame.display.set_caption("Predator Prey Simulation")
        self.clock = pygame.time.Clock()  # create pygame clock object 
        self.font = pygame.font.Font(None, 18)  # Create a font object

    def update(self):


        self.predator.uptate(self.window, 50, self.kdtree, self.boids)
        self.Number_of_agents = len(self.boids)
        
        if self.Number_of_agents == 0:
            # alles weg
            return self.update_tick
        
        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])            
        
        for boid in self.boids:
            boid.update(self.window, self.turnfactor, self.separation_factor, self.cohesion_factor, self.alignment_factor, self.kdtree, self.boids, self.visual_range, self.predator, self.predator.predation_detected)
        
        # logging
        if self.log_to_console and self.update_tick % 100 == 0:
            print(f'tick {self.update_tick}: nr_boids={self.Number_of_agents}')
        self.update_tick += 1

    def render(self):
        # mooie spaghetti hehe
        events = pygame.event.get()
        for events in pygame.event.get():  # loop through all events
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
        
        self.clock.tick(time) # voor het regelen van fps
        #self.clock.tick()

