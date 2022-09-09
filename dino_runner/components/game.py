#from operator import truediv
from inspect import trace
import pygame
#from turtle import Screen
from dino_runner.components.player_lives.player_heart_manager import Player_Heart_Manager
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstaculomanager import Obstacle_manager
from dino_runner.components import text_utils
from dino_runner.components.clouds import Cloud
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = True
        self.death_count = 0
        self.game_speed = 20
        self.goal = 1000
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = Obstacle_manager()
        self.points = 0
        self.player_heart_manager = Player_Heart_Manager()
        self.cloud = Cloud()
        self.power_up_manager = PowerUpManager()

    def run(self):
        # Game loop: events - update - draw
        self.create_comment()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        #pygame.quit()

    def create_comment(self):
        self.power_up_manager.reset_power_ups(self.points)    

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.userInput = pygame.key.get_pressed()
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed, self.player)
        self.player.update(self.userInput)
        self.cloud.update(self.game_speed)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.player_heart_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.score()
        self.cloud.draw(self.screen)
        self.player.check_lives()

        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1
        if self.game_speed < 45:
            self.game_speed += 0.01
        if self.points > self.goal:
            self.player_heart_manager.heart_count += 1
            self.goal += 1000    

        score, score_rect = text_utils.get_score_element(self.points)
        self.player.check_visibility(self.screen)
        self.screen.blit(score, score_rect)

    def show_menu(self, death_count = 0):
        self.running = True

        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements(death_count)

        pygame.display.update()

        self.handle_key_events_on_menu()


    def print_menu_elements(self, death_count = 0):
        half_screen_height = SCREEN_HEIGHT // 2

        if death_count == 0:
            text, text_rect = text_utils.get_centered_message("Press any key to start")
            self.screen.blit(text, text_rect)    
        elif death_count > 0:
            text, text_rect = text_utils.get_centered_message("Press any key to restart")
            score, score_rect = text_utils.get_centered_message("Your score: " + str(self.points), half_screen_height+250, half_screen_height+200)
            self.screen.blit(text, text_rect)
            self.screen.blit(score, score_rect)


    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                self.points = 0
                self.run()    

