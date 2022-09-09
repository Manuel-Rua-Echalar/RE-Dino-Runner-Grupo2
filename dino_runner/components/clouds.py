import pygame
from dino_runner.utils.constants import CLOUD
from dino_runner.utils.constants import SCREEN_WIDTH
import random


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50,300)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, game_speed):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(100, 300)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))