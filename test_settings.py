class T_Settings:
    ''' Clase que guarda la configuración del juego '''
    
    def __init__(self) -> None:
        ''' Inicia la configuración del juego '''
        # Configuración de la pantalla
        self.screen_width = 1600
        self.screen_higth = 800
        self.bg_color = (9, 34, 79)

        # Configuración de las balas
        self.bullet_width = 2
        self.bullet_height = 12
        self.bullet_color = (217, 243, 19)
        self.bullet_allowed = 3

        # Configuración de laser
        self.laser_width = 30
        self.laser_height = 3
        self.laser_color = (231, 41, 1)
        self.laser_allowed = 2
        self.laser_limit = 5

        # Configuración del alien
        self.fleet_drop_speed = 10

        # Configuración de la nave
        self.ship_limit = 2

        # Rapidez con la que se acelera el juego
        self.speedup_scale = 1.1

        # Lo rápido que aumenta el valor en puntos de los aliens
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        ''' Inicializa las configuraciones que cambian durante el juego '''
        self.ship_speed_x = 1.5
        self.ship_speed_y = 1
        self.bullet_speed = 1.5
        self.laser_speed = 3
        self.alien_speed = 0.5

        # fleet_direction de 1 representa derecha, -1 representa izquierda
        self.fleet_direction = 1

        # Puntuación por alien
        self.alien_points = 30

    def incrase_speed(self):
        ''' incrementa las configuraciones de velocidad '''
        self.ship_speed_x *= self.speedup_scale
        self.ship_speed_y *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.laser_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)