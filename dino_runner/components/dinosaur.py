from mimetypes import init
import pygame
from signal import default_int_handler
from dino_runner.utils.constants import RUNNING, DUCKING, JUMPING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, RUNNING_SHIELD, JUMPING_SHIELD

class Dinosaur():
    X_POS = 80
    Y_POS = 310
    JUMP_VEL  = 8.5
    Y_POS_DUCK = 340

    def __init__(self) -> None:
        self.duck_img = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
        self.run_img = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
        self.jump_img = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
        self.type = DEFAULT_TYPE
        self.image = self.run_img[self.type][0]

        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
       
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.jump_vel = self.JUMP_VEL 

        self.setup_state_boolean()

        self.has_lives = False
        self.lives_transition_time = 0 

    def setup_state_boolean(self):
        self.has_powerup = False 
        self.shield =False 
        self.show_text=False 
        self.shield_time_up=0       

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
            self.dino_fast = False
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
            self.dino_fast = False

        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_jump = False
            self.dino_run = True
            self.dino_fast = False    



    def draw(self, screen):
        screen.blit(self.image,(self.dino_rect.x, self.dino_rect.y))

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1]
        self.dino_rect = self.image.get_rect()
        
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        
        self.step_index += 1    

    def duck(self):
        self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1


    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 5
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL 

    def check_lives(self):
        if self.has_lives:
            transition_time = round(((self.lives_transition_time - pygame.time.get_ticks()) / 1000))
            if transition_time < 0:
                self.has_lives = False

    def check_visibility(self,screen):
        if self.shield:
            time_to_show = round( (self.shield_time_up - pygame.time.get_ticks())/1000,2 )
            if(time_to_show>=0):
                fond = pygame.font.Font('freesansbold.ttf',18)
                text = fond.render(f'shield enable for {time_to_show}',True,(0,0,0))
                textRect = text.get_rect()
                textRect.center = (500,40)
                screen.blit(text,textRect)
            else:
                self.shield = False 
                self.update_to_default(SHIELD_TYPE)

    def update_to_default(self, current_type):
        if(self.type == current_type):
            self.type = DEFAULT_TYPE            
