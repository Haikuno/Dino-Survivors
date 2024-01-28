import pygame

class Pickup(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y):
        self.game = game
        self._layer = game.OBJ_LAYER
        self.groups = game.all_sprites, game.obj_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.height = game.TILESIZE / 4
        self.width = game.TILESIZE / 4
        self.image = pygame.transform.scale(image, (game.TILESIZE/4, game.TILESIZE/4))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pickup(self):
        raise NotImplementedError("Implementar pickup.")

    def update(self):
        self.rect.move_ip(round(self.game.ss_x), round(self.game.ss_y))
        if pygame.sprite.spritecollide(self, self.game.player_group, False):
            self.pickup()