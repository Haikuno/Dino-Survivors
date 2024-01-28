import random
import pygame
from button import Button
from enemy import Enemy
from player import Player
from wall import Wall
from map import Map
from os import path


class Game:
    def __init__(self):
        pygame.init()

        # inicializacion de pantalla
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)
        self.SCROLL_THRESH = 350

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Dino Survivors")

        # imagenes
        self.bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()
        self.start_img = pygame.image.load("img/buttons/start.png").convert_alpha()
        self.continue_img = pygame.image.load("img/buttons/continue.png").convert_alpha()
        self.exit_img = pygame.image.load("img/buttons/exit.png").convert_alpha()
        self.board_img = pygame.image.load("img/buttons/board.png").convert_alpha()
        self.dmg_img = pygame.image.load("img/buttons/dmg.png").convert_alpha()
        self.speed_img = pygame.image.load("img/buttons/speed.png").convert_alpha()

        # fuente
        self.font = pygame.font.Font('freesansbold.ttf', 16)

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
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 - 250,
            self.start_img,
            0.5,
        )
        self.exit_button = Button(
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 + 100,
            self.exit_img,
            0.5,
        )

        self.continue_button = Button(
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 - 250,
            self.continue_img,
            0.5,
        )

        self.board_button = Button(
            0,
            0,
            self.board_img,
            10,
        )

        self.dmg_button = Button(
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 - 250,
            self.dmg_img,
            0.5,
        )
        self.speed_button = Button(
            self.SCREEN_WIDTH // 2 - 215,
            self.SCREEN_HEIGHT // 2 + 100,
            self.speed_img,
            0.5,
        )

        # colores
        self.BG = (144, 201, 120)
        self.RED = (255, 0, 0)

    def load(self):  # variables de juego
        self.spawn_cd = 1000
        self.spawn_time = pygame.time.get_ticks()
        self.ss_x = 0  # screen_scroll x
        self.ss_y = 0  #      ""       y
        self.bg_scroll = 0
        self.start_game = False
        self.pause_game = False

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
        game_dir = path.dirname(__file__)
        self.map = Map(path.join(game_dir, "map.txt"))

        X_OFFSET = -20
        Y_OFFSET = -10

        for i, row in enumerate(self.map.data):
            for j, column in enumerate(row):
                if column == "*":
                    Wall(self, j + X_OFFSET, i + Y_OFFSET)

        # player

        self.player = Player(
            char_type="player",
            x=self.SCREEN_WIDTH / 2,
            y=self.SCREEN_HEIGHT / 2,
            scale=3,
            speed=3,
            animation_types=["idle", "moving"],
            groups=(self.all_sprites, self.player_group),
            game=self,
            damage=25,
        )

    def draw_bg(self):
        self.screen.fill(self.BG)

    def run(self):
        self.load()

        run = True
        while run:
            self.clock.tick(self.FPS)

            # menú principal
            if not self.start_game:
                self.screen.fill((100, 100, 100))
                if self.start_button.draw(self.screen):
                    self.load()
                    self.start_game = True
                if self.exit_button.draw(self.screen):
                    run = False

            # pausa
            elif self.pause_game:
                if self.continue_button.draw(self.screen):
                    self.pause_game = False
                if self.exit_button.draw(self.screen):
                    run = False

            # levelup
            elif self.player.leveling_up:
                self.screen.fill(self.BG)
                dmgtext = self.font.render(f"Damage : {self.player.damage}", True, (255,255,255), (0,0,0))
                speedtext = self.font.render(f"Shooting Cooldown : {self.player.shooting_cd}", True, (255,255,255), (0,0,0))
                dmgrect = dmgtext.get_rect()
                speedrect = speedtext.get_rect()
                dmgrect.center = (self.SCREEN_WIDTH // 5, self.SCREEN_HEIGHT // 3)
                speedrect.center = (self.SCREEN_WIDTH // 5, self.SCREEN_HEIGHT // 4)
                self.screen.blit(dmgtext, dmgrect)
                self.screen.blit(speedtext, speedrect)


                if self.dmg_button.draw(self.screen):
                    self.player.damage += 15
                    self.player.leveling_up = False
                elif self.speed_button.draw(self.screen):
                    self.player.shooting_cd -= 100
                    self.player.leveling_up = False

            else:
                self.draw_bg()

                # spawn enemigo

                if pygame.time.get_ticks() - self.spawn_time > self.spawn_cd:
                    self.spawn_time = pygame.time.get_ticks()
                    enemy = Enemy(
                        char_type="enemy",
                        x=random.choice(
                            [random.randrange(-600, -200), random.randrange(1000, 1200)]
                        ),
                        y=random.choice(
                            [random.randrange(-600, -200), random.randrange(600, 1200)]
                        ),
                        scale=2,
                        speed=1,
                        animation_types=["moving"],
                        groups=(self.all_sprites, self.enemy_group),
                        game=self,
                    )
                    while pygame.sprite.spritecollide(enemy, self.wall_group, False):
                        enemy.rect.centerx = random.choice(
                            [random.randrange(-200, -190), random.randrange(190, 200)]
                        )
                        enemy.rect.centery = random.choice(
                            [random.randrange(-200, -190), random.randrange(190, 200)]
                        )

                self.player.update(self.screen)
                self.enemy_group.update(self)

                # update and draw groups
                self.bullet_group.update()
                self.bullet_group.draw(self.screen)

                self.wall_group.update()
                self.wall_group.draw(self.screen)

                self.obj_group.update()
                self.obj_group.draw(self.screen)

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
                    if event.key == pygame.K_a or event.key == pygame.K_UP:
                        self.moving_up = True
                    if event.key == pygame.K_a or event.key == pygame.K_DOWN:
                        self.moving_down = True

                # KEYUP
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.moving_left = False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.moving_right = False
                    if event.key == pygame.K_a or event.key == pygame.K_UP:
                        self.moving_up = False
                    if event.key == pygame.K_a or event.key == pygame.K_DOWN:
                        self.moving_down = False

            pygame.display.update()

        pygame.quit()


game = Game()

game.run()
