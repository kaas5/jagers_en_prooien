import numpy as np
from predator import Predator
import matplotlib.pyplot as plt

from tools import NEIGHBORHOOD_RADIUS, Vector, getDistance, getDistanceSquared

class Boid():

    def __init__(self, window, margin, field_of_view = np.pi / 2, visual_range = 40):
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.random.randint(0, (margin)*0.2)
        self.x, self.y = (
            window[0]//2 + int(r * np.cos(angle)),
            window[0]//2 + int(r * np.sin(angle)))
        self.vx = np.random.uniform(-1, 1)
        self.vy = np.random.uniform(-1, 1)
        self.vx_prev = 0
        self.vy_prev = 0
        self.ax = 0
        self.ay = 0
        
        self.stress = 0.0 #1.0 if the boid is stressed
        
        self.visual_range = visual_range
        self.field_of_view = field_of_view

    def potential_repulsion(self, window, turning_factor, obstacles):

        if self.x != 0 and self.x != window[0]:
            self.ax += turning_factor*(1/(self.x**2) - 1/((self.x - window[0])**2))
        if self.y != 0 and self.y != window[1]:
            self.ay += turning_factor*(1/(self.y**2) - 1/((self.y - window[1])**2))

        for obstacle in obstacles:
            to_center = Vector(obstacle.x - self.x, obstacle.y - self.y)
            distance = to_center.magnitude() - obstacle.radius 

            # Calculate the direction of repulsion force
            repulsion = Vector(self.x - obstacle.x, self.y - obstacle.y)
            repulsion.normalize()

            # de boid zit in de obstacle, zet m erbuiten
            if distance < 0:
                self.x += repulsion.x * (-distance + 1)
                self.y += repulsion.y * (-distance + 1)
                continue

            if distance < obstacle.radius + 100:
                # nu de 2 orthogonal vectoren pakken
                v1 = Vector(repulsion.y, -repulsion.x)
                v2 = Vector(-repulsion.y, repulsion.x)
                heading = Vector(self.vx + self.ax, self.vy + self.ay)
                # kijken welke het meeste op de huidige trajectory ligt
                if getDistanceSquared(v1, heading) < getDistanceSquared(v2, heading):
                    repulsion = v1
                else:
                    repulsion = v2

                # dot product om te kijken of we op de obstacle af gaan of dat we er van weg bewegen
                to_center.normalize()
                heading.normalize()
                dot = to_center.x * heading.x + to_center.y * heading.y
                dot = max(0.0, dot)

                # Calculate the magnitude of repulsion force
                repulsion_magnitude = turning_factor * (1 / ((distance + 1) ** 2)) * dot
                self.ax += repulsion.x * repulsion_magnitude
                self.ay += repulsion.y * repulsion_magnitude
        
    def is_predator_in_fov(self, predator):
        angle_to_prey = np.arctan2(predator.y - self.y, predator.x - self.x)
        angle_fov = np.arctan2(self.vy, self.vx)

        # we draaien de boel zodat je niet met de tipping point te maken hebt tussen -pi en pi, maakt de if statement overzichtelijk
        angle_to_prey_transformed = angle_to_prey - angle_fov
        return self.field_of_view / 2 > angle_to_prey_transformed and angle_to_prey_transformed > -self.field_of_view / 2

    def separation(self, close_neighbours):
        close_dx, close_dy = 0, 0
        total_close = 0
        for boid in close_neighbours:
            close_dx +=  - boid.x + self.x
            close_dy += - boid.y + self.y
            total_close += 1
        if total_close == 0:
            return (0,0)
        return (close_dx / total_close, close_dy / total_close)
    
    def cohesion(self, visual_neighbours):
        x_avg, y_avg, total = 0, 0, 0
        for boid in visual_neighbours:
            x_avg += boid.x
            y_avg += boid.y
            total += 1
        if total > 0:
            x_avg /= total
            y_avg /= total
        else :
            return (0, 0)
        return (x_avg - self.x, y_avg - self.y)
    
    def alignment(self, visual_neighbours):
        vx_avg, vy_avg, total = 0, 0, 0

        for boid in visual_neighbours:
            if boid.stress != 0.0:
                if boid.stress > self.stress:
                    self.stress = boid.stress
                #else:
                #    self.stress = self.stress - 1/200#- boid.stress/1000
            vx_avg += boid.vx
            vy_avg += boid.vy
            total += 1
        if total > 0:
            vx_avg /= total
            vy_avg /= total
        else :
            return (0, 0)
        return (vx_avg, vy_avg)
    
    def predator_interaction(self, predator):
        if self.is_predator_in_fov(predator) or self.stress > 0.0:

            predator_dx = predator.x - self.x #Positif si au dessus
            predator_dy = predator.y - self.y #Positif si à droite

            predator_dist = predator_dx**2 + predator_dy**2
            predatorturnfactor = 0.2

            if predator_dist < self.visual_range**2: 

                self.stress = 1.0    #If the boid can see the predator, it is fully stress
                if predator_dy > 0:  # predator above boid
                    self.vy -= predatorturnfactor
                if predator_dy < 0:  # predator below boid
                    self.vy += predatorturnfactor
                if predator_dx > 0:  # predator left of boid
                    self.vx -= predatorturnfactor
                if predator_dx < 0:  # predator right of boid
                    self.vx += predatorturnfactor

        #else: #The prey doesn't see the predator anymore, it starts to destress and the stress is a linear function, maybe it could be great to find a paper about it ? 
        self.stress = self.stress - 1/500 #It should take 30 seconds to distess
        if self.stress < 0.0:
            self.stress = 0.0


    def speed_limit(self):        
        velocity_length = np.sqrt(self.vx**2 + self.vy**2)
        v_min = 1.0
        v_max = 1.6
        hier = v_min + self.stress * (v_max - v_min)
        if velocity_length > hier:
            self.vx = (self.vx/velocity_length)*hier
            self.vy = (self.vy/velocity_length)*hier
        if velocity_length < v_min:
            self.vx = (self.vx/velocity_length)*v_min
            self.vy = (self.vy/velocity_length)*v_min        

    def draw_triangle(self):
        center = (self.x, self.y)
        side_length = 6
        angle_radians = np.arctan2(self.vy, self.vx) + np.pi/2
        triangle = np.array([
            [-side_length / 2, side_length / 2],
            [side_length / 2, side_length / 2],
            [0, -side_length / 1]
        ])
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]
        ])
        rotated_triangle = np.dot(triangle, rotation_matrix.T) + center
        return [(int(point[0]), int(point[1])) for point in rotated_triangle]

    def update(self, window, turning_factor, separation_factor, cohesion_factor, alignment_factor,kd_tree, boids, predator, obstacles):
        
        # This line keep the cohesion at the beginning of the simulation to have a herd
        #if predation_detected == False:
        #    cohesion_factor = 0.013

        self.ax = 0.0
        self.ay = 0.0

        #Mandatory, the edges of the simulator should be always active
        self.potential_repulsion(window, turning_factor, obstacles)

        #Close neighbours ()
        #close_indices = kd_tree.query_ball_point((self.x, self.y), 15)
        #close_neighbours = [boids[i] for i in close_indices]
        
        # We determine the visual neighbours
        visual_indices = kd_tree.query_ball_point((self.x, self.y), self.visual_range)
        visual_neighbours = [boids[i] for i in visual_indices]

        # Flocking Behaviour in general
        s = self.separation(visual_neighbours)
        self.ax += separation_factor * s[0]
        self.ay += separation_factor * s[1]

        # Cohesion and alignment
        c = self.cohesion(visual_neighbours)
        self.ax += cohesion_factor * c[0]
        self.ay += cohesion_factor * c[1]

        a = self.alignment(visual_neighbours)
        self.ax += alignment_factor * a[0]
        self.ay += alignment_factor * a[1]
    
        random_factor = 0.02
        self.ax += np.random.uniform(-random_factor, random_factor)
        self.ay += np.random.uniform(-random_factor, random_factor)

        #Predator interaction
        self.predator_interaction(predator)

        self.vx += self.ax
        self.vy += self.ay
        #Finally we applied a speed limit to prevent the animals from going faster than the speed of light
        self.speed_limit()
        self.x += self.vx
        self.y += self.vy

        

        