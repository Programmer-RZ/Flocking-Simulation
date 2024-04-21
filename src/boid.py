import pygame
import math
from random import randint, uniform

from variables import *
from tools import *

class Boid:
    def __init__(self, color, triangleScale, triangleCenter) -> None:
        self.color = color

        # triangle
        self.triangleRotation = 0
        self.triangleScale = triangleScale
        self.trianglePoints = []

        # move
        self.center = triangleCenter
        self.velocity = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        self.acceleration = pygame.math.Vector2()
        self.maxSpeed = 2

        # view distance
        self.viewDistance = 40
        self.avoidDistance = 20

        # separation
        self.separationValue = 0.3

        # alignment
        self.alignmentValue = 0.5

        # cohesion
        self.cohesionValue = 0.1
        
        # screen edges
        self.turnfactor = 0.2
    
    def update(self, boids):
        # sort the boids from closest to farthest in distance
        neiBoids = sorted(boids,
                          key=lambda b: b.center.distance_to(self.center))
        
        # reset acceleration
        self.acceleration.x = 0
        self.acceleration.y = 0
        
        # separation
        avoid = self.separation(boids)
        avoid *= self.separationValue
        self.acceleration += avoid
        
        # cohesion
        coh = self.cohesion(boids)
        coh *= self.cohesionValue
        self.acceleration += coh

        # alignment
        align = self.alignment(boids)
        align *= self.alignmentValue
        self.acceleration += align
        
        # screen_edges
        self.screen_edges()
    
    def check_in_view(self, distance):
        if distance < self.viewDistance:
            return True
        else:
            return False
            
    def screen_edges(self):
        if self.center.x < LEFT_MARGIN:
            self.acceleration.x += self.turnfactor
        if self.center.x > RIGHT_MARGIN:
            self.acceleration.x -= self.turnfactor
        if self.center.y > BOTTOM_MARGIN:
            self.acceleration.y -= self.turnfactor
        if self.center.y < TOP_MARGIN:
            self.acceleration.y += self.turnfactor 
    
    def separation(self, boids):
        totalSeparations = 0
        steering = pygame.math.Vector2()

        for b in boids:
            distance = abs(self.center.distance_to(b.center))
            if b is not self and distance < self.avoidDistance:
                temp = self.center - b.center
                if distance != 0:
                    temp /= distance**2
                steering += temp
                totalSeparations += 1
        
        if totalSeparations > 0:
            steering /= totalSeparations
            steering = steering.normalize()
            steering *= self.maxSpeed
            steering -= self.velocity
            limitVector(steering, 1)
        
        return steering
    
    def alignment(self, boids):
        totalAlignments = 0
        steering = pygame.math.Vector2()

        for b in boids:
            distance = abs(self.center.distance_to(b.center))
            if b is not self and self.check_in_view(distance):
                vel = b.velocity.normalize()
                steering += vel

                totalAlignments += 1
        
        if totalAlignments > 0:
            steering /= totalAlignments
            steering = steering.normalize()
            steering *= self.maxSpeed
            steering -= self.velocity.normalize()
            limitVector(steering, 1)
        
        return steering
    
    def cohesion(self, boids):
        totalCohesions = 0
        steering = pygame.math.Vector2()

        for b in boids:
            distance = abs(self.center.distance_to(b.center))
            if b is not self and self.check_in_view(distance):
                steering += b.center

                totalCohesions += 1
        
        if totalCohesions > 0:
            steering /= totalCohesions
            steering -= self.center
            steering = steering.normalize()
            steering *= self.maxSpeed
            steering -= self.velocity
            limitVector(steering, 1)
        
        return steering

    
    def moveTriangle(self):
        self.center += self.velocity
        self.velocity += self.acceleration

        # limit velocity to max speed
        limitVector(self.velocity, self.maxSpeed)

        # calculate rotation
        self.triangleRotation = math.degrees(math.atan2(self.velocity.y, self.velocity.x))

        # walls
        '''
        if self.center.x < 0 : self.center.x = WIDTH; self.center.y = HEIGHT - self.center.y
        elif self.center.x > WIDTH : self.center.x = 0; self.center.y = HEIGHT - self.center.y
        
        if self.center.y < 0 : self.center.y = HEIGHT; self.center.x = WIDTH - self.center.x
        elif self.center.y > HEIGHT : self.center.y = 0; self.center.x = WIDTH - self.center.x
        '''
    
    def makeTriangle(self):
        # preprogrammed points of the triangle
        points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]

        # rotate points
        rotated_points = [pygame.math.Vector2(p).rotate(self.triangleRotation) for p in points]
        
        self.trianglePoints = [(self.center + p*self.triangleScale) for p in rotated_points]
    
    def draw(self, window) -> None:
        pygame.draw.polygon(window, self.color, self.trianglePoints)