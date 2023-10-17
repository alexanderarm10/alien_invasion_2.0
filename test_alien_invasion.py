import sys
from time import sleep
import pygame
from test_settings import T_Settings
from test_ship import T_Ship
from test_bullet import T_Bullet
from test_laser import T_Laser
from test_laser_left import T_Laser_Left
from test_alien import T_Alien
from test_game_stats import GameStats
from test_button import T_Button
from test_scoreboard import T_Scoreboard

class T_AlienInvasion:
    ''' Clase que gestiona los recursos del juego '''
    
    def __init__(self) -> None:
        ''' Inicializa el juego y crea recursos '''
        pygame.init()
        self.settings = T_Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_higth))
        pygame.display.set_caption('Test Invasión Alienigena')
        # Crea una instancia para guardar las estadísticas del juego
        self.stats = GameStats(self)
        self.sb = T_Scoreboard(self)
        self.ship = T_Ship(self)
        self.bullets = pygame.sprite.Group()
        self.laser = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.sound_bullet = pygame.mixer.Sound('images/bullet.ogg')
        self.sound_laser = pygame.mixer.Sound('images/laser.ogg')
        self.sound_alien = pygame.mixer.Sound('images/alien.ogg')
        self.sound_ship = pygame.mixer.Sound('images/ship.ogg')
        
        self._create_fleet()

        # Crea el botón play
        self.play_button = T_Button(self, 'Play')


    def run_game(self):
        ''' Inicia el bucle principal del juego '''
        pygame.mixer.music.load('images/game.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_laser()
                self._update_aliens()
                
            self._update_screen()


    def _check_events(self):
        ''' Responde a pulsaciones del teclado y eventos del ratón '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos):
        ''' Inicial un juego nuevo cuando el jugador hace click en play '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Restablece las estadísticas del juego
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_rayo()

            # Se deshace de los aliens, balas y laser que quedan
            self.aliens.empty()
            self.bullets.empty()
            self.laser.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Oculta el cursor del mouse
            pygame.mouse.set_visible(False)


    def _check_keydown_event(self, event):
        ''' Responde a pulsaciones de teclas '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            self.sound_bullet.play()
        elif event.key == pygame.K_z:
            if self.stats.laser_left > 0:
                self._fire_laser()
                self.sound_laser.play()

    def _start_game(self):
        # Restablece las estadísticas del juego
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.sb.prep_rayo()

        # Se deshace de los aliens, balas y laser que quedan
        self.aliens.empty()
        self.bullets.empty()
        self.laser.empty()

        # Crea una flota nueva y centra la nave
        self._create_fleet()
        self.ship.center_ship()

        # Oculta el cursor del mouse
        pygame.mouse.set_visible(False)


    def _check_keyup_event(self, event):
        ''' Responde a liberaciones de teclas '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_rigth = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        

    def _fire_bullet(self):
        ''' Cerea una bala nueva y añade al grupo de balas '''
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = T_Bullet(self)
            self.bullets.add(new_bullet)
            

    def _fire_laser(self):
        ''' Cerea un laser y añade al grupo de lasers '''
        if len(self.laser) < self.settings.laser_allowed:
            new_laser = T_Laser(self)
            self.laser.add(new_laser)
            new_laser_left = T_Laser_Left(self)
            self.laser.add(new_laser_left)
        
        # Disminuye la cantidad de laser disponibles
        self.stats.laser_left -= 1
        self.sb.prep_rayo()
                

    def _update_bullets(self):
        ''' Actualiza la posición de las balas y se deshace de las viejas '''
        # Actualiza las posiciones de las balas
        self.bullets.update()
        # Se deshace de las balas que han desaparecido
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()


    def _update_laser(self):
        ''' Actualiza la posición del laser y se deshace de los viejos '''
        # Actualiza las posiciones de las balas
        self.laser.update()
        # Se deshace de las balas que han desaparecido
        screen_rect = self.screen.get_rect()
        for laser in self.laser.copy():
            if laser.rect.right >= screen_rect.right or laser.rect.left <=0:
                self.laser.remove(laser)
        
        self._check_laser_alien_collision()

        
    def _check_bullet_alien_collision(self):
        # Busca balas que hayan dado a aliens
        # Si hay, se deshace de la bala y el alien
        collisions_bullet = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions_bullet:
            self.sound_alien.play()
            for aliens in collisions_bullet.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
        if not self.aliens:
            # Destruye las balas existentes y crea una flota nueva
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.incrase_speed()

            # Aumenta el nivel
            self.stats.level += 1
            self.sb.prep_level()

            sleep(0.5)
            
    
    def _check_laser_alien_collision(self):
        # Busca laser que hayan dado a aliens
        # Si hay, se deshace del laser y el alien  
        collisions_laser = pygame.sprite.groupcollide(self.laser, self.aliens, False, True)
        if collisions_laser:
            self.sound_alien.play()
            for aliens in collisions_laser.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destruye laser existebtes y crea una flota nueva
            self.laser.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.incrase_speed()
            
            # Aumenta el nivel
            self.stats.level += 1
            self.sb.prep_level()

            sleep(0.5)

    
    def _update_aliens(self):
        ''' Comprueba si la flota está en un borde y 
        Actualiza las posiciones de todos los aliens de la flota '''
        self._check_fleet_edges()
        self.aliens.update()

        # Busca colisiones entre aliens y la nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.sound_ship.play()
            self._ship_hit()

        # Busca aliens llegando al fondo de la pantalla
        self._check_aliens_bottom()

    
    def _check_aliens_bottom(self):
        ''' Comprueba si algún alien ha llegado al fondo de la pantalla '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Trata esto como si fuera una colisión entre un alien y la nave
                self._ship_hit()
                break

    
    def _ship_hit(self):
        ''' Responde al impacto de un alien en la nave '''
        if self.stats.ship_left >0:
        # Disminuye ship_left
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Se deshace de los aliens, balas y laser restantes
            self.aliens.empty()
            self.bullets.empty()
            self.laser.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()
            
            # Pausa
            sleep(1.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _create_fleet(self):
        ''' Crea la flota de aliens '''
        # Crea un alien y halla el número de aliens en una fila
        # El espacio entre aliens es igual al ancho de un alien
        alien = T_Alien(self)
        alien_width, alien_height = alien.rect.size
        avalible_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avalible_space_x // (2 * alien_width)

        # Determina el número de filas de aliens que caben en la pantalla
        ship_height = self.ship.rect.height
        avalible_space_y = (self.settings.screen_higth - (5 * alien_height) - ship_height)
        number_rows = avalible_space_y // (2 * alien_height)

        # Crea la flota completa de aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    
    def _check_fleet_edges(self):
        ''' Responde adecuadamente si un alien ha llegado al borde '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        ''' Baja toda la flota y cambia su dirección '''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_alien(self, alien_number, row_number):
        ''' Crea un alien y lo pone en la fila '''
        alien = T_Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)


    def _update_screen(self):
        ''' Actualiza las imagenes en la pantalla y cambia a la pantalla nueva '''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for laser in self.laser.sprites():
            laser.draw_laser()
        
        self.aliens.draw(self.screen)

        # Dibuja la puntuación en la pantalla
        self.sb.show_score()

        # Dibuja el botón play en la pantalla
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Hace visible la última pantalla dibujada
        pygame.display.flip()


if __name__ == '__main__':
    ai = T_AlienInvasion()
    ai.run_game()