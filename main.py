import random
import time
import pygame
from os import path
from button import Button
from enemy import Enemy
from player import Player
from wall import Wall
from map import Map


class Game:
    def __init__(self):
        pygame.init()

        # inicializacion de pantalla
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Survivors")

        # imagenes

        self.bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()

        self.shooting_cd_img = pygame.image.load("img/buttons/cadencia.png").convert_alpha()
        self.start_img = pygame.image.load("img/buttons/empezar.png").convert_alpha()
        self.continue_img = pygame.image.load("img/buttons/continuar.png").convert_alpha()
        self.damage_img = pygame.image.load("img/buttons/daño.png").convert_alpha()
        self.menu_img = pygame.image.load("img/buttons/fondo.png").convert_alpha()
        self.menu_img = pygame.transform.scale(
            self.menu_img, (self.menu_img.get_width() * 1.15, self.menu_img.get_height() * 1.15)
        )
        self.map_img = pygame.image.load("img/map/map.png").convert_alpha()
        self.map_img = pygame.transform.scale(
            self.map_img, (self.map_img.get_width() * 4, self.map_img.get_height() * 4)
        )
        self.exit_img = pygame.image.load("img/buttons/salir.png").convert_alpha()
        self.play_again_img = pygame.image.load("img/buttons/volver a jugar.png").convert_alpha()
        self.go_back_img = pygame.image.load("img/buttons/volver al menu.png").convert_alpha()


        # fuente
        self.font = pygame.font.Font("freesansbold.ttf", 16)

        # layers
        self.WALL_LAYER = 3
        self.MOB_LAYER = 2
        self.OBJ_LAYER = 1
        self.GROUND_LAYER = 0

        # framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # botones
        self.start_button = Button(
            self.SCREEN_WIDTH // 2 - 80,
            self.SCREEN_HEIGHT // 2 + 75,
            self.start_img,
            1,
        )
        self.exit_button = Button(
            self.SCREEN_WIDTH // 2 - 80,
            self.SCREEN_HEIGHT // 2 + 200,
            self.exit_img,
            1,
        )

        self.continue_button = Button(
            self.SCREEN_WIDTH // 2 - 80,
            self.SCREEN_HEIGHT // 2 + 75,
            self.continue_img,
            1,
        )

        self.damage_button = Button(
            self.SCREEN_WIDTH // 2,
            self.SCREEN_HEIGHT // 20,
            self.damage_img,
            0.5,
        )
        self.shooting_cd_button = Button(
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 + 100,
            self.shooting_cd_img,
            0.5,
        )

        # colores
        self.BG = (58, 190, 65)
        self.RED = (255, 0, 0)
        # 3ABE41

        self.won = False

    def load(self):
        # variables de juego
        self.spawn_cd = 2500
        self.won = False
        self.strongie_spawn_cd = 3500
        self.spawn_time = pygame.time.get_ticks()
        self.strongie_spawn_time = pygame.time.get_ticks()
        self.spawn_strongies = False
        self.ss_x = 0  # screen_scroll x
        self.ss_y = 0  #      ""       y
        self.bg_scroll_x = 0
        self.bg_scroll_y = 0
        self.start_game = False
        self.pause_game = False
        self.max_enemies = 10
        self.difficulty = 0
        self.time_passed = 0
        self.seconds = 0

        # variables de movimiento
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

        # grupos
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.obj_group = pygame.sprite.Group()

        # map
        self.TILESIZE = 64
        self.wall_coords = []
        game_dir = path.dirname(__file__)
        self.map = Map(path.join(game_dir, "map.txt"))

        X_OFFSET = -30
        Y_OFFSET = -10

        for i, row in enumerate(self.map.data):
            for j, column in enumerate(row):
                if column == "*":
                    Wall(self, j + X_OFFSET, i + Y_OFFSET)

        # player

        self.player = Player(
            char_type="player",
            x=self.SCREEN_WIDTH // 2 - 20,
            y=self.SCREEN_HEIGHT // 2 - 50,
            scale=3,
            speed=3,
            animation_types=["idle", "moving"],
            groups=(self.all_sprites, self.player_group),
            game=self,
            damage=25,
        )

    def draw_bg(self):
        self.screen.fill(self.BG)
        self.screen.blit(
            self.map_img, (-1850 - self.bg_scroll_x, -450 + self.bg_scroll_y)
        )

    def increase_difficulty(self):
        self.difficulty = self.seconds // 30
        self.max_enemies = 10 + self.difficulty
        self.spawn_cd = 2500 - self.difficulty * 200
        self.strongie_spawn_cd = 3500 - self.difficulty * 200
        if self.seconds >= 120:
            self.spawn_strongies = True

    def get_coords(self):
        x_coords = (
            random.choice([random.randrange(200, 250), random.randrange(750, 800)]),
        )
        y_coords = (
            random.choice([random.randrange(200, 250), random.randrange(750, 800)]),
        )
        return (x_coords[0], y_coords[0])

    def spawn_enemy(self):
        if (
            pygame.time.get_ticks() - self.spawn_time > self.spawn_cd
            and len(self.enemy_group) < self.max_enemies
        ):
            self.spawn_time = pygame.time.get_ticks()
            x, y = self.get_coords()
            enemy = Enemy(
                char_type="enemy",
                x=x,
                y=y,
                scale=2,
                speed=1,
                animation_types=["moving"],
                groups=(self.all_sprites, self.enemy_group),
                game=self,
            )
            while pygame.sprite.spritecollide(enemy, game.wall_group, False):
                x, y = self.get_coords()
                enemy.rect.center = x, y

        if (
            pygame.time.get_ticks() - self.strongie_spawn_time > self.strongie_spawn_cd
            and len(self.enemy_group) < self.max_enemies
            and self.spawn_strongies
        ):
            self.strongie_spawn_time = pygame.time.get_ticks()
            x, y = self.get_coords()
            enemy = Enemy(
                char_type="strongie",
                x=x,
                y=y,
                scale=3,
                speed=2,
                animation_types=["moving"],
                groups=(self.all_sprites, self.enemy_group),
                game=self,
            )
            while pygame.sprite.spritecollide(enemy, game.wall_group, False):
                x, y = self.get_coords()
                enemy.rect.center = x, y

    def run(self):
        self.load()

        run = True
        while run:
            self.clock.tick(self.FPS)

            # menú principal
            if not self.start_game or not self.player.alive:
                self.screen.blit(self.menu_img, (-5,0))

                if self.start_button.draw(self.screen):
                    self.load()
                    self.start_game = True
                if self.exit_button.draw(self.screen):
                    run = False

            # pausa
            elif self.pause_game and not self.won:
                self.screen.blit(self.menu_img, (-5,0))
                if self.continue_button.draw(self.screen):
                    self.pause_game = False
                if self.exit_button.draw(self.screen):
                    run = False

            # levelup
            elif self.player.leveling_up and not self.won:
                self.screen.fill(self.BG)
                dmgtext = self.font.render(
                    f"Damage : {self.player.damage}", True, (255, 255, 255), (0, 0, 0)
                )
                speedtext = self.font.render(
                    f"Shooting Cooldown : {self.player.shooting_cd}",
                    True,
                    (255, 255, 255),
                    (0, 0, 0),
                )
                dmgrect = dmgtext.get_rect()
                speedrect = speedtext.get_rect()
                dmgrect.center = (self.SCREEN_WIDTH // 6, self.SCREEN_HEIGHT // 3)
                speedrect.center = (self.SCREEN_WIDTH // 6, self.SCREEN_HEIGHT // 4)
                self.screen.blit(dmgtext, dmgrect)
                self.screen.blit(speedtext, speedrect)
                if self.damage_button.draw(self.screen):
                    self.player.damage += 5
                    self.player.leveling_up = False
                elif self.shooting_cd_button.draw(self.screen):
                    self.player.shooting_cd -= 30
                    self.player.leveling_up = False

            elif self.won:
                self.screen.fill((255, 255, 255))

            else:
                self.increase_difficulty()

                # spawn enemigo
                self.spawn_enemy()

                # update player actions
                if self.player.alive:
                    self.player.shoot(game=self)

                    if (
                        self.moving_left
                        or self.moving_right
                        or self.moving_up
                        or self.moving_down
                    ):
                        self.player.update_action(1)
                    else:
                        self.player.update_action(0)

                    self.ss_x, self.ss_y = self.player.move(game)

                # update and draw groups
                self.draw_bg()
                self.wall_group.update()

                self.obj_group.update()
                self.obj_group.draw(self.screen)

                self.bullet_group.update()
                self.bullet_group.draw(self.screen)

                self.enemy_group.update(self)
                self.player.update(self.screen)

                # TIME
                current_time = pygame.time.get_ticks()
                if current_time > self.time_passed + 1500:
                    self.time_passed = current_time
                elif current_time > self.time_passed + 1000:
                    self.seconds += 1
                    self.time_passed = current_time
                    if self.seconds >= 300:
                        self.won = True

                timetext = self.font.render(
                    f"{time.strftime('%M:%S', time.gmtime(self.seconds))}",
                    True,
                    (255, 255, 255),
                )
                timerect = timetext.get_rect()
                timerect.centerx = self.SCREEN_WIDTH // 2 + 5
                timerect.centery += 8
                self.screen.blit(timetext, timerect)

            for event in pygame.event.get():
                # Cerrar el juego
                if event.type == pygame.QUIT:
                    run = False

                # KEYDOWN
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause_game = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.moving_left = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.moving_up = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.moving_down = True

                # KEYUP
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.moving_left = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.moving_right = False
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.moving_up = False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.moving_down = False

            pygame.display.update()

        pygame.quit()


game = Game()

game.run()
