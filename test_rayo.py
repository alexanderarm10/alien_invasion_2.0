import pygame
from pygame.sprite import Sprite

class T_Rayo(Sprite):
    ''' Clase para gestionar la imagen de los laser '''
    
    def __init__(self, ai_game):
        super().__init__()
        ''' inicializa el rayo y configura su posición '''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # carga la imagen de la nave y obtiene su rect
        self.image = pygame.image.load('images/rayo.bmp')
        self.rect = self.image.get_rect()