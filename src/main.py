
import pygame
import sys
from random import randint
from copy import deepcopy

from variables import *
from boid import Boid

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


boids = [
    Boid(color=(70, 50, 180),
         triangleScale=8,
         triangleCenter=pygame.math.Vector2(randint(LEFT_MARGIN, RIGHT_MARGIN), randint(TOP_MARGIN, BOTTOM_MARGIN)))

    for i in range(100)
    ]

def main() -> None:
    global boids
    
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        window.fill((0, 0, 0))
        
        for b in boids:
            b.update(boids)
        
        for b in boids:
            b.moveTriangle()
            b.makeTriangle()
                  
            b.draw(window)
        

        pygame.display.update()

if __name__ == "__main__":
    main()