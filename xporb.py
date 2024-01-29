from pickup import Pickup
import pygame

class XPOrb(Pickup):
    def __init__(self, game, x, y, image, value):
        super().__init__(game, image, x, y)
        self.value = value

    def pickup(self):
        self.game.player.xp += self.value
        self.kill()

    def update(self):
        super().update()