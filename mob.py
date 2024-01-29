import pygame
import os
from xporb import XPOrb


class Mob(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, animation_types, groups, game):
        self.game = game
        self.groups = groups
        self._layer = game.MOB_LAYER
        self.char_type = char_type
        self.alive = True
        self.max_hp = 100
        self.hp = self.max_hp
        self.armor = 0
        self.speed = speed
        self.direction = 1
        self.shooting_direction = (0, 0)
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.frame_mod = 0
        self.action = 0  # 0 = idle, 1 = moving
        self.update_animation_time = pygame.time.get_ticks()
        self.update_shooting_time = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self, self.groups)

        for animation in animation_types:
            temp_list = []
            dir = self.game.resource_path(f"img/{self.char_type}/{animation}")
            num_of_frames = len(os.listdir(dir))
            for i in range(num_of_frames):
                img = pygame.image.load(
                    f"{dir}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (img.get_width() * scale, img.get_height() * scale)
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update_animation(self):
        self.animation_cooldown = 300
        if (
            pygame.time.get_ticks() - self.update_animation_time
            > self.animation_cooldown
        ):
            self.update_animation_time = pygame.time.get_ticks()
            if (
                self.frame_index + self.frame_mod
                > len(self.animation_list[self.action]) - 1
                or self.frame_index + self.frame_mod < 0
            ):
                self.frame_mod = -self.frame_mod
            self.frame_index += self.frame_mod
        self.image = self.animation_list[self.action][self.frame_index]
        if self.frame_mod == 0:
            self.frame_mod = 1

    def check_alive(self):
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.speed = 0
            if self.char_type == "enemy":
                XPOrb(self.game, self.rect.x, self.rect.y, self.game.xporb_img, self.game.xporb_value)
            elif self.char_type == "strongie":
                XPOrb(self.game, self.rect.x, self.rect.y, self.game.xporb2_img, self.game.xporb2_value)
            self.kill()

    def update(self, screen):
        self.update_animation()
        self.check_alive()
        self.draw(screen)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
