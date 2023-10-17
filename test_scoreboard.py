import pygame.font
from pygame.sprite import Group
from test_ship import T_Ship
from test_rayo import T_Rayo

class T_Scoreboard:
    ''' Una clase para la información de la puntuación '''

    def __init__(self, ai_game):
        ''' Inicializa los atributos de la puntuación '''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Configuiración de fuente para la información de la puntuación
        self.text_color = (149, 219, 3)
        self.font = pygame.font.SysFont(None, 30)

        # Prepara las imagenes de las puntuaciones iniciales
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_rayo()

    
    def prep_score(self):
        ''' Convierte la puntuación en una imagen renderizada '''
        rounded_score = round(self.stats.score, -1)
        score_str = 'Score {:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, 
                                            self.settings.bg_color)

        # Muestra la puntuación en la parte superior derecha de la pantalla
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    
    def prep_high_score(self):
        ''' Convierte la puntuación en una imagen renderizada '''
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = 'Max score {:,}'.format(rounded_high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, 
                                                 self.settings.bg_color)

        # Muestra la puntuación en la parte superior derecha de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    
    def prep_level(self):
        ''' Convierte el nivel en una imagen renderizada '''
        level_str = 'Level ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, 
                                            self.settings.bg_color)
        
        # Muestra el nivel en la parte superior derecha y debajo de la puntuación
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        ''' Muestra cuantas naves quedan '''
        self.ships = Group()
        for ship_number in range(self.stats.ship_left + 1):
            ship = T_Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    
    def prep_rayo(self):
        self.rayos = Group()
        for rayo_number in range(self.stats.laser_left):
            rayo = T_Rayo(self.ai_game)
            rayo.rect.x = 110 + rayo_number * rayo.rect.width
            rayo.rect.y = 10
            self.rayos.add(rayo)

    
    def show_score(self):
        ''' Dibuja la puntuación en la pantalla '''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        self.rayos.draw(self.screen)

    
    def check_high_score(self):
        ''' Comprueba si hay una nueva puntuación más alta '''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()