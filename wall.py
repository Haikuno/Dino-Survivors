import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = game.WALL_LAYER
        self.groups = game.all_sprites, game.wall_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * game.TILESIZE
        self.y = y * game.TILESIZE
        self.width = game.TILESIZE
        self.height = game.TILESIZE
        img = pygame.image.load(f'img/icons/grass2.png').convert_alpha()
        self.image = pygame.transform.scale(img, (game.TILESIZE, game.TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        game.wall_coords.append(self.rect.center)



    def update(self):
        self.rect.move_ip(round(self.game.ss_x), round(self.game.ss_y))