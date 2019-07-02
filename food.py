import pygame

from entity import Entity


class Food(Entity):
    def __init__(self, init_pos, size, healthy=True):
        color = (0, 255, 0) if healthy else (255, 0, 0)
        sprite_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(sprite_img, int(size / 2), int(size / 2), int(size / 2 - 1), color)
        pygame.gfxdraw.filled_circle(sprite_img, int(size / 2), int(size / 2), int(size / 2 - 1), color)
        super().__init__(init_pos, size, sprite_img)
        self.value = int(size * 3)
