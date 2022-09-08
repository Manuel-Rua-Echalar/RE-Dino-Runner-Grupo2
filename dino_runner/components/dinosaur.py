from mimetypes import init
import pygame
from signal import default_int_handler
from dino_runner.utils.constants import RUNNING, JUMPING

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    JUMP_VEL  = 8.5

    def __init__(self) -> None:
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False


        # Definiendo la posición del dinosaurio
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL 

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()      
        if self.dino_run:
            self.run()   

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_jump = True
            self.dino_run = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True    



    def draw(self, screen):
        screen.blit(self.image,(self.dino_rect.x, self.dino_rect.y))

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        
        self.step_index += 1    

    def duck(self):
        pass

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL       