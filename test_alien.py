import pygame
from pygame.sprite import Sprite
from random import randint

class T_Alien(Sprite):
    ''' Una clase para representar un alien en la flota '''

    def __init__(self, ai_game):
        ''' inicializa el alien y establece su posición inicial '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carga la imagen del alien y configura su atributo rect
        select_image = str(randint(1, 3))
        image_alien = 'images/alien_' + select_image + '.bmp'
        self.image = pygame.image.load(image_alien)
        self.rect = self.image.get_rect()

        # Inicia un nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height * 1.5

        # Guarda la posición horizontal exacta del alien
        self.x = float(self.rect.x)


    def check_edges(self):
        ''' Devuelve True si el alien está al borde de la pantalla '''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
   

    def update(self):
        ''' Mueve el alien hacia la derecha o hacia la izquierda '''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    

