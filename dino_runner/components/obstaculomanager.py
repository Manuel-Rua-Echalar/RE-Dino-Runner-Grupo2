import pygame

from dino_runner.components.big_cactus import Big_Cactus
from dino_runner.utils.constants import LARGE_CACTUS

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
            if random.randint(0, 2) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS) )
            elif random.randint(0, 2) == 1:
                self.obstacles.append(Bird(BIRD) )
            else:
                self.obstacles.append(Big_Cactus(LARGE_CACTUS) ) 

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.shield:
                    if not game.player.has_lives:
                        game.player_heart_manager.reduce_heart_count()
                        if game.player_heart_manager.heart_count > 0:
                            game.player.has_lives = True
                            self.obstacles.pop()
                            start_transition_time = pygame.time.get_ticks()
                            game.player.lives_transition_time = start_transition_time + 100
                        else:
                            # self.obstacles.remove(obstacle)
                            pygame.time.delay(500)
                            game.playing = False
                            game.death_count += 1
                            game.player_heart_manager.heart_count = 6
                else:
                    self.obstacles.remove(obstacle)            


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)