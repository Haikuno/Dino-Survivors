import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target, speed, bullet_img, game, damage):
        self.game = game
        self.speed = speed
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target

        self.angle = math.atan2(target[1] - self.rect.y, target[0] - self.rect.x) # Estas operaciones matematicas son necesarias para garantizar una correcta trayectoria
        self.rotation = int(self.angle * 180 / math.pi)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        self.damage = damage
        self.groups = game.all_sprites, game.bullet_group
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.rect.x += self.dx + self.game.ss_x # Mover la bala teniendo en cuenta el screen_scroll
        self.rect.y += self.dy + self.game.ss_y

        # si salio de la pantalla
        if (
            self.rect.right < -self.game.SCREEN_WIDTH * 0.1
            or self.rect.left > self.game.SCREEN_WIDTH * 1.1
        ):
            self.kill()
        if (
            self.rect.top < -self.game.SCREEN_HEIGHT * 0.1
            or self.rect.top > self.game.SCREEN_HEIGHT * 1.1
        ):
            self.kill()

        # si toca a un enemigo
        for enemy in self.game.enemy_group:
            if pygame.sprite.spritecollide(enemy, self.game.bullet_group, False):
                if enemy.alive:
                    enemy.hp -= self.damage
                    self.kill()

        # si choca contra una pared
        if pygame.sprite.spritecollide(self, self.game.wall_group, False):
            self.kill()
