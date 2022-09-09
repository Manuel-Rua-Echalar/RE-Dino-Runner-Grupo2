import pygame
from dino_runner.components.obstaculo import obstacle
import random
class Big_Cactus(obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300