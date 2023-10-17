import pygame
from pygame.sprite import Sprite

class T_Laser_Left(Sprite):
    ''' Una clase para gestionar los laser disparados desde la nave '''

    def __init__(self, ai_game):
        ''' Crea un objeto para el laser en la posición actual de la nave '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.laser_color

        # Crea un rectangulo para el laser izquierdo en (0, 0) y luego establece la posición corecta
        self.rect = pygame.Rect(0, 0, self.settings.laser_width, self.settings.laser_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Guarda la posición del laser como valor decimal
        self.x = float(self.rect.x)


    def update(self):
        ''' Mueve los laser hacia la izquierda y derecha por la pantalla '''
        # Actualiza la posición decimal de la bala
        self.x -= self.settings.laser_speed
        # Actualiza la posiciób del rectangulo
        self.rect.x = self.x


    def draw_laser(self):
        ''' Dibuja la bala en la pantalla'''
        pygame.draw.rect(self.screen, self.color, self.rect)