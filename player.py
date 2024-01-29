from mob import Mob
from bullet import Bullet
import pygame


class Player(Mob):
    def __init__(
        self, char_type, x, y, scale, speed, animation_types, groups, game, damage
    ):
        super().__init__(char_type, x, y, scale, speed, animation_types, groups, game)
        self.xp = 0
        self.xp_levelup = 100
        self.shooting_cd = 700
        self.level = 1
        self.leveling_up = False
        self.damage = damage

    def shoot(self, game):
        if pygame.time.get_ticks() - self.update_shooting_time > self.shooting_cd:
            pos = pygame.math.Vector2(self.rect.x, self.rect.y)
            try:
                closest_enemy = min(
                    [e for e in game.enemy_group.sprites()],
                    key=lambda e: pos.distance_to(
                        pygame.math.Vector2(e.rect.x, e.rect.y)
                    ),
                )
            except:
                closest_enemy = "none"
            if closest_enemy != "none":
                self.update_shooting_time = pygame.time.get_ticks()
                Bullet(
                    x=self.rect.centerx,
                    y=self.rect.centery,
                    target=closest_enemy.rect.center,
                    speed=4,
                    bullet_img=game.bullet_img,
                    game=game,
                    damage=self.damage,
                )

    def move(self, game):
        # direction
        if game.moving_left:
            self.direction = -1
            self.flip = True
        else:
            self.direction = 1
            self.flip = False
        # update rectangle pos
        move = pygame.math.Vector2(
            game.moving_right - game.moving_left, game.moving_down - game.moving_up
        )

        ss_x = 0
        ss_y = 0

        if move.length_squared() > 0:
            move.scale_to_length(self.speed)
            sim_move = self.rect.move(round(move.x), round(move.y))

            ss_x = self.rect.x - sim_move.x
            ss_y = self.rect.y - sim_move.y

            for wall in game.wall_group:
                if sim_move.colliderect(wall.rect):
                    ss_x = 0
                    ss_y = 0

            game.bg_scroll_x -= ss_x
            game.bg_scroll_y += ss_y

        return (ss_x, ss_y)

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_levelup
        self.xp_levelup += 5
        self.leveling_up = True

    def update_action(self, new_action):
        # si nueva accion es diferente a la anterior
        if new_action != self.action:
            self.action = new_action

    def draw(self, screen):
        super().draw(screen)
        if self.hp != self.max_hp:
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (self.rect.centerx - self.hp / 2 - 2, self.rect.bottom + 3, self.hp + 4, 12),
            )  # borde vida
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                (self.rect.centerx - self.hp / 2, self.rect.bottom + 5, self.hp, 8),
            )  # vida
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (10-2, 10-2, self.xp_levelup+4, 20),
        )  # borde XP maxima
        pygame.draw.rect(
            screen,
            (90, 90, 255),
            (10, 10, self.xp_levelup, 16),
        )  # XP maxima
        pygame.draw.rect(
            screen,
            (0, 0, 200),
            (10, 10, self.xp_levelup * self.xp / self.xp_levelup, 16),
        )  # XP actual

    def update(self, screen):
        super().update(screen)
        if self.xp >= self.xp_levelup:
            self.level_up()
