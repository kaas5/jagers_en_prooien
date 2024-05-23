import numpy as np
import pygame

from tools import NEIGHBORHOOD_RADIUS, Vector, getDistance, getDistanceSquared

class Predator():

    def __init__(self, window, field_of_view=np.pi/2):
        # alles random
        self.x = np.random.uniform(0, window[0])
        self.y = np.random.uniform(0, window[1])
        self.vx = np.random.uniform(-1, 1)
        self.vy = np.random.uniform(-1, 1)

        self.ax = 0.0
        self.ay = 0.0

        self.visual_predation = 99999
        self.direction = np.arctan2(self.vy, self.vx)
        self.predation_detected = False
        self.centroid = [self.x, self.y]
        self.eating = False
        self.eating_duration = 0
        self.max_eating_duration = 50
        self.field_of_view = field_of_view
        self.visual_indices = []

        self.target_prey = None
        self.max_target_timeout = 0
        self.target_timeout = 0

    def strat1(self, visual_indices, preys):
        closest_prey_index = min(visual_indices, key=lambda i: np.linalg.norm(np.array([preys[i].x, preys[i].y]) - np.array([self.x, self.y])))
        return preys[closest_prey_index]

    def strat3(self, visual_indices, preys):
        visual_preys = [preys[index] for index in visual_indices]
        preys_x = list(p.x for p in visual_preys)
        preys_y = list(p.y for p in visual_preys)
        preys_in_range = np.array([preys_x, preys_y])
        accum = []

        # schuif de array van preys 'langs elkaar', bereken distance in bulk en sla op
        for j in range(len(visual_indices) - 1): 
            compare_preys_in_range = np.roll(preys_in_range, j + 1, axis=1)
            distances = np.sum(np.square(preys_in_range - compare_preys_in_range), axis=0)
            accum.append(distances)

        # je wil de maximum van elke individuele minimum distance!!!
        if len(accum) == 0: return visual_preys[0] # anders doet np.stack() moeilijk
        accum = np.stack(accum)
        min_distance = np.min(accum, axis=0)
        max_distance_index = np.argmax(min_distance)
        return visual_preys[max_distance_index]
    
    def strat3_1(self, visual_indices, preys):
        if len(visual_indices) == 1:
            return preys[0]
        
        visual_preys = [preys[index] for index in visual_indices]
        preys_x = list(p.x for p in visual_preys)
        preys_y = list(p.y for p in visual_preys)
        preys_in_range = np.array([preys_x, preys_y])
        preys_in_range = np.tile(np.array([preys_x, preys_y]), (len(visual_indices) - 1, 1, 1))
        preys_in_range_compare = np.empty((preys_in_range.shape[0], preys_in_range.shape[1], preys_in_range.shape[2]))

        # schuif de array van preys 'langs elkaar'
        for j in range(len(visual_indices) - 1): 
            preys_in_range_compare[j,:,:] = np.roll(preys_in_range[j,:,:], j + 1, axis=1)

        # bereken distance in bulk en sla op
        distances = np.sum(np.square(preys_in_range - preys_in_range_compare), axis=1)
        min_distance = np.min(distances, axis=0)
        max_distance_index = np.argmax(min_distance)
        return visual_preys[max_distance_index]

    def filter_indices_in_fov(self, visual_indices, preys):
        filtered_visual_indices = []

        for index in visual_indices:
            prey = preys[index]
            angle_to_prey = np.arctan2(prey.y - self.y, prey.x - self.x)
            angle_fov = np.arctan2(self.vy, self.vx)

            # we draaien de boel zodat je niet met de tipping point te maken hebt tussen -pi en pi, maakt de if statement overzichtelijk
            angle_to_prey_transformed = angle_to_prey - angle_fov
            if self.field_of_view / 2 > angle_to_prey_transformed and angle_to_prey_transformed > -self.field_of_view / 2:
                filtered_visual_indices.append(index)

        return filtered_visual_indices

    def tracking_behaviour(self, kdtree, preys):
        self.centroid = [self.x, self.y]
        speed_norm = np.sqrt(self.vx**2 + self.vy**2)

        self.visual_indices = kdtree.query_ball_point((self.x, self.y), self.visual_predation)
        if len(self.visual_indices) != 0:
            self.visual_indices = self.filter_indices_in_fov(self.visual_indices, preys)
        
        if len(self.visual_indices) == 0 and self.predation_detected == True :
            # Any prey can't be seen, so the predator is randomly moving
            self.vx = self.vx + np.random.uniform(-0.1, 0.1)
            self.vy = self.vy + np.random.uniform(-0.1, 0.1)

        if len(self.visual_indices) != 0:
            self.predation_detected = True #If a prey is detected, the flag is set to True 
            
            
            # Use a strategy to find the prefered prey
            #selected_prey = self.strat1(self.visual_indices, preys)
            #selected_prey = self.strat3(self.visual_indices, preys)
            selected_prey = self.strat3_1(self.visual_indices, preys) # niet perse sneller :(

            if selected_prey != self.target_prey and self.target_prey is not None:
                self.target_timeout += 1
                if self.target_timeout > self.max_target_timeout:
                    # nu mag je wisselen
                    self.target_prey = selected_prey
                    self.target_timeout = 0
            else:
                self.target_prey = selected_prey
                self.target_timeout = 0
            
            angle_to_prey = np.arctan2(self.target_prey.y - self.y, self.target_prey.x - self.x)
            
            # Update the predator's speed
            self.vx = speed_norm * np.cos(angle_to_prey)
            self.vy = speed_norm * np.sin(angle_to_prey)
            self.direction = angle_to_prey

            self.closest_prey = self.target_prey
            self.centroid = [self.target_prey.x, self.target_prey.y]
            
            #If the prey is closed to the predator, the prey is eaten
            if np.linalg.norm(np.array([self.x, self.y]) - np.array([self.target_prey.x, self.target_prey.y])) < 5:
                preys.remove(self.target_prey)
                self.target_prey = None
                self.visual_indices = [] # dit updaten voor 1 frame is erg veel gedoe aangezien de indices nu zijn verschoven, dus skippen we
                self.eating = True
            
                    
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


    def draw_triangle(self):
        center = (self.x, self.y)
        side_length = 8
        angle_radians = np.arctan2(self.vy, self.vx) + np.pi/2
        triangle = np.array([
            [-side_length / 2, side_length / 2],
            [side_length / 2, side_length / 2],
            [0, -side_length / 1]])
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]])
        
        rotated_triangle = np.dot(triangle, rotation_matrix.T) + center

        return [(int(point[0]), int(point[1])) for point in rotated_triangle]

    def speed_limit(self):
        v_max = 1.68
        v_min = 1.68
        vel_norm = np.sqrt(self.vx**2 + self.vy**2)        
        
        if vel_norm > v_max:
            self.vx = (self.vx/vel_norm)*v_max
            self.vy = (self.vy/vel_norm)*v_max
            
        if vel_norm < v_min:
            self.vx = (self.vx/vel_norm)*v_min
            self.vy = (self.vy/vel_norm)*v_min

        if self.eating:
            self.vx, self.vy = 0,0
        
    def uptate(self, window, turnfactor, kdtree, boids, obstacles):

        self.ax = 0.0
        self.ay = 0.0

        self.tracking_behaviour(kdtree, boids)
        self.potential_repulsion(window, turnfactor, obstacles)
        
        self.vx += self.ax
        self.vy += self.ay
        self.speed_limit()
        self.x += self.vx
        self.y += self.vy

        if self.eating:
            if self.eating_duration < self.max_eating_duration:
                self.eating_duration += 1
                self.eating = True
                self.vx = (self.vx)*0.0
                self.vy = (self.vy)*0.0
            else:
                self.eating = False
                self.eating_duration = 0

if __name__ == "__main__":
    predator = Predator((1000,1000))