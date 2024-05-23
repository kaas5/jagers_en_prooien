import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
import numpy as np
import pyautogui
import time
from boids import Boid
from scipy.spatial import KDTree
from predator import Predator
from obstacles import Obstacle

class Simulation():
    def __init__(self, window, margin, nr_agents, render_screen, 
                obstacle_positions=None, obstacle_radii=None,
                run_for_ticks = None,
                draw_fps = True,
                log_to_console = True,
                max_fps = 60,
                take_screenshots = False,
                param_set = None):
        self.window = window
        self.margin = margin
        self.render_screen = render_screen # voor als je de zooi wil zien op een scherm
        self.take_screenshots = take_screenshots
        self.run_for_ticks = run_for_ticks
        
        self.draw_fps = draw_fps
        self.log_to_console = log_to_console
        self.max_fps = max_fps # werkt alleen als je de boel gaat renderen

        self.boids =  [Boid(window,margin) for _ in range(nr_agents)]
        self.predator = Predator(window, field_of_view=np.pi/2)
        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])
        self.tick = 0 
        self.time_between_screenshots = 300
        self.screenshot_counter = 0

        self.turnfactor = 100 # voor nu hardcoden

        # Initialize obstacles
        self.obstacles = []
        if obstacle_positions is not None and obstacle_radii is not None:
            for i in range(len(obstacle_positions)):
                self.obstacles.append(Obstacle(obstacle_positions[i][0], obstacle_positions[i][1], obstacle_radii[i]))


        if param_set == None:
            self.separation_factor = 0.039
            self.alignment_factor = 0.5
            self.cohesion_factor = 0.002
            self.visual_range = 25
        else:
            self.separation_factor = param_set[0]
            self.alignment_factor = param_set[1]
            self.cohesion_factor = param_set[2]
            self.visual_range = param_set[3]

        if self.log_to_console:
            print(f'parameters: {self.separation_factor},{self.alignment_factor},{self.cohesion_factor},{self.visual_range}')

        if self.render_screen: 
            self.init_graphics()
    
    def init_graphics(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.window)
        pygame.display.set_caption("Predator Prey Simulation")
        self.clock = pygame.time.Clock()  # create pygame clock object 
        self.font = pygame.font.Font(None, 18)  # Create a font object

    def run(self):
        while   ((self.run_for_ticks == None or self.tick < self.run_for_ticks) 
                and len(self.boids) > 0):
            self.update()
            if self.render_screen:
                self.render()
        return len(self.boids)

    def update(self):
        self.predator.uptate(self.window, 50, self.kdtree, self.boids, self.obstacles)
        if len(self.boids) == 0: # predator.uptate() kan boids verwijderen dus hier kunnen we pas checken of de lijst leeg is
            return
        
        self.kdtree = KDTree([[boid.x, boid.y] for boid in self.boids])
        for boid in self.boids:
            boid.update(self.window, self.turnfactor, self.separation_factor, self.cohesion_factor, self.alignment_factor, 
                        self.kdtree, self.boids, self.visual_range, self.predator, self.predator.predation_detected, self.obstacles)
        
        # logging
        if self.log_to_console and self.tick % 100 == 0:
            print(f'tick {self.tick}: nr_boids={len(self.boids)}')
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
        
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for boid in self.boids:
            pygame.draw.polygon(self.screen, 'red', boid.draw_triangle())
            
        pygame.draw.polygon(self.screen, 'blue', self.predator.draw_triangle())
        pygame.draw.circle(self.screen, 'green', self.predator.centroid, 5)
        for visible_prey_index in self.predator.visual_indices:
            prey = self.boids[visible_prey_index]
            pygame.draw.circle(self.screen, 'green', [prey.x, prey.y], 2)

        if self.draw_fps:
            fps = int(self.clock.get_fps())
            text_2 = self.font.render(f'fps: {fps}', True, (0, 0, 0))
            self.screen.blit(text_2, (5, 5))

        pygame.display.update()
        
        if self.take_screenshots:
            self.screenshot_counter += 1
            if self.screenshot_counter % self.time_between_screenshots == 0:
                self.screenshot()

        self.clock.tick(self.max_fps) # voor het regelen van fps

    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot_" + str(int(time.time())) + ".png")