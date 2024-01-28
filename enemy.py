from mob import Mob
import pygame


class Enemy(Mob):
    def __init__(self, char_type, x, y, scale, speed, animation_types, groups, game):
        super().__init__(char_type, x, y, scale, speed, animation_types, groups, game)
        self.damage_cd = 200
        self.damage_time = pygame.time.get_ticks()
        self.damage = 2

    def update(self, game):
        super().update(game.screen)
        chase_left = False
        chase_right = False
        chase_up = False
        chase_down = False
        if game.player.rect.centerx < self.rect.centerx:
            chase_left = True
            self.flip = True
        elif game.player.rect.centerx > self.rect.centerx:
            chase_right = True
            self.flip = False
        if game.player.rect.centery < self.rect.centery:
            chase_up = True
        elif game.player.rect.centery > self.rect.centery:
            chase_down = True

        move = pygame.math.Vector2(chase_right - chase_left, chase_down - chase_up)
        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            self.rect.move_ip(round(move.x + game.ss_x), round(move.y + game.ss_y))

        # si choca contra una pared, se cancela el movimiento
        if pygame.sprite.spritecollide(self, game.wall_group, False):
            self.rect.move_ip(round(-move.x * 4), round(-move.y * 2))

        # si toca al jugador
        if pygame.sprite.spritecollide(self, game.player_group, False):
            self.rect.move_ip(round(-move.x), round(-move.y))
            if pygame.time.get_ticks() - self.damage_time > self.damage_cd:
                self.damage_time = pygame.time.get_ticks()
                game.player.hp -= self.damage
                print(game.player.hp)
