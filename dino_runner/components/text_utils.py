import pygame



FONT_STYLE = "freesansbold.ttf"
black_color = (0,0,0)

def get_score_element(points):
    font = pygame.font.Font(FONT_STYLE, 20)

    text = font.render("Score: " + str(points), True, black_color)
    text_rect = text.get_rect()
    text_rect.center = (900,30)

    return text, text_rect