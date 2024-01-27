import pygame
import math
import os

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Survivors')

# framerate
clock = pygame.time.Clock()
FPS = 60


# variables de movimiento
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# cargar imagenes
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

# colores

BG=(144,201,120)

def draw_bg():
    screen.fill(BG)


class Mob(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, animation_types):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.alive = True
        self.max_hp = 100
        self.hp = self.max_hp
        self.armor = 0
        self.speed = speed
        self.direction = 1
        self.shooting_direction = (0,0)
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.frame_mod = 0
        self.action = 0 # 0 = idle, 1 = moving
        self.update_animation_time = pygame.time.get_ticks()
        self.update_shooting_time = pygame.time.get_ticks()


        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = img.get_rect()
        self.rect.center = (x, y)


    def move(self, moving_left, moving_right, moving_up, moving_down):
        #update rectangle pos
        move = pygame.math.Vector2(moving_right - moving_left, moving_down - moving_up)
        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            self.rect.move_ip(round(move.x), round(move.y))

    def shoot(self):
        if self.char_type == 'player':
            self.shooting_cooldown = 100
            if pygame.time.get_ticks() - self.update_shooting_time > self.shooting_cooldown:
                pos = pygame.math.Vector2(self.rect.x, self.rect.y)
                closest_enemy = min([e for e in enemy_group.sprites()], key=lambda e: pos.distance_to(pygame.math.Vector2(e.rect.x, e.rect.y)))
                self.update_shooting_time = pygame.time.get_ticks()
                bullet = Bullet(x=self.rect.centerx, y=self.rect.centery, target=closest_enemy.rect.center, speed=4)
                bullet_group.add(bullet)

    def update_animation(self):
        self.animation_cooldown = 300
        if pygame.time.get_ticks() - self.update_animation_time > self.animation_cooldown:
            self.update_animation_time = pygame.time.get_ticks()
            if self.frame_index + self.frame_mod > len(self.animation_list[self.action])-1 or self.frame_index + self.frame_mod < 0:
                self.frame_mod = -self.frame_mod
            self.frame_index += self.frame_mod
        self.image = self.animation_list[self.action][self.frame_index]
        if self.frame_mod == 0:
            self.frame_mod = 1

    def update_action(self, new_action):
        #si nueva accion es diferente a la anterior
        if new_action != self.action:
            self.action = new_action
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self, player):
        self.update_animation()
        chase_left = False
        chase_right = False
        chase_up = False
        chase_down = False
        if player.rect.centerx > self.rect.centerx:
            chase_left = True
        elif player.rect.centerx < self.rect.centerx:
            chase_right = True
        if player.rect.centery < self.rect.centery:
            chase_up = True
        elif player.rect.centery > self.rect.centery:
            chase_down = True

        move = pygame.math.Vector2(chase_left - chase_right, chase_down - chase_up)
        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            self.rect.move_ip(round(move.x), round(move.y))


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.angle = math.atan2(target[1] - self.rect.y, target[0] - self.rect.x)
        self.rotation = int(self.angle * 180 / math.pi)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed


    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        #si salio de la pantalla
        if self.rect.right < -SCREEN_WIDTH * 0.1 or self.rect.left > SCREEN_WIDTH * 1.1:
            self.kill()


# grupos
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Mob(char_type='player', x=200, y=200, scale=3, speed=3, animation_types = ['idle', 'moving'])
enemy = Mob(char_type='player', x=400, y=400, scale=2, speed=1, animation_types=['moving'])
enemy2 = Mob(char_type='player', x=700, y=700, scale=2, speed=1, animation_types=['moving'])

enemy_group.add(enemy)
enemy_group.add(enemy2)


run = True
while run:
    clock.tick(FPS)
    if moving_left or moving_right or moving_up or moving_down:
            player.update_action(1)
    else:
            player.update_action(0)
    draw_bg()

    player.draw()
    enemy_group.update(player)
    enemy_group.draw(screen)

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(screen)

    #update player actions
    if player.alive:
        player.shoot()

        if moving_left or moving_right or moving_up or moving_down:
            player.update_action(1)
        else:
            player.update_action(0)
        player.move(moving_left, moving_right, moving_up, moving_down)

    for event in pygame.event.get():

        # Cerrar el juego
        if event.type == pygame.QUIT:
            run = False<3

        # KEYDOWN
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_a or event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_a or event.key == pygame.K_DOWN:
                moving_down = True

        # KEYUP
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_a or event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_a or event.key == pygame.K_DOWN:
                moving_down = False

    pygame.display.update()

pygame.quit()