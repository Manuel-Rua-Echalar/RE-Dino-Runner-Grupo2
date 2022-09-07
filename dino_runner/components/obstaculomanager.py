from random import random
import pygame

from dino_runner.components.cactus import Cactus
from dino_runner.utils.constants import SMALL_CACTUS

from dino_runner.components.birds import Bird
from dino_runner.utils.constants import BIRD

import random

class Obstacle_manager():

    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 1) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS) )
            else:
                self.obstacles.append(Bird(BIRD) )    

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if(game.player.dino_rect.colliderect(obstacle.rect) ):
                pygame.time.delay(500)
                game.playing = False
                break    

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)