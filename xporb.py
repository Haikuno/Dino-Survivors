from pickup import Pickup
import pygame

class XPOrb(Pickup):
    def __init__(self, game, x, y):
        image = pygame.image.load(f"img/icons/xp.png").convert_alpha()
        super().__init__(game, image, x, y)

    def pickup(self):
        self.game.player.xp += 40
        self.kill()

    def update(self):
        super().update()