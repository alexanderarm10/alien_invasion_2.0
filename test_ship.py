import pygame
from pygame.sprite import Sprite

class T_Ship(Sprite):
    ''' Clase para gestionar la nave '''
    
    def __init__(self, ai_game):
        super().__init__()
        ''' inicializa la nave y configura su posición '''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # carga la imagen de la nave y obtiene su rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Coloca inicialmente cada nave nueva en el centro inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda un valor decimal para la posicion horizontal de la nave
        self.x = float(self.rect.x)

        # Guarda un valor decimal para la posición vertical de la nave
        self.y = float(self.rect.y)

        # Bandera de movimiento
        self.moving_rigth = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update(self):
        ''' Atualiza la posición de la nave en función de la bandera de movimiento '''
        # Actualiza el valor x de la nave, no el rect
        if self.moving_rigth and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_x
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_x
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_y
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed_y

        # Actualiza el objeto rect de self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        ''' Dibuja la nave en su ubicación actual'''
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)