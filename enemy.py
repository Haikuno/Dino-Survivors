from mob import Mob
import pygame
import math

class Enemy(Mob):
    def __init__(self, char_type, x, y, scale, speed, animation_types, groups, game):
        super().__init__(char_type, x, y, scale, speed, animation_types, groups, game)
        self.damage_cd = 200
        self.damage_time = pygame.time.get_ticks()
        self.damage = 2

        if self.char_type == "strongie":
            self.max_hp = 200
            self.hp = self.max_hp
            self.damage = 5

    def update(self, game):
        super().update(game.screen)
        self.target = game.player.rect.center

        self.angle = math.atan2(self.target[1] - self.rect.y, self.target[0] - self.rect.x) # Estas operaciones matematicas son necesarias para garantizar una correcta trayectoria
        self.rotation = int(self.angle * 180 / math.pi)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed

        move = pygame.math.Vector2(self.dx, self.dy)

        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            sim_move_x = self.rect.move(round(move.x), 0)
            sim_move_y = self.rect.move(0, round(move.y))
            x_move_valid = True
            y_move_valid = True

            # si choca contra una pared, se cancela el movimiento
            if pygame.sprite.spritecollide(self, game.wall_group, False):
                for wall in game.wall_group:
                    if wall.rect.colliderect(sim_move_x):
                        x_move_valid = False
                    if wall.rect.colliderect(sim_move_y):
                        y_move_valid = False

            if x_move_valid:
                self.rect.move_ip(round(move.x), 0)
                if self.dx > 0:
                    self.flip = False
                else:
                    self.flip = True

            if y_move_valid:
                self.rect.move_ip(0, round(move.y))

            self.rect.move_ip(round(game.ss_x), round(game.ss_y))


        # si toca al jugador
        if pygame.sprite.spritecollide(self, game.player_group, False):
            self.rect.move_ip(round(-move.x), round(-move.y))
            if pygame.time.get_ticks() - self.damage_time > self.damage_cd:
                self.damage_time = pygame.time.get_ticks()
                game.player.hp -= self.damage
