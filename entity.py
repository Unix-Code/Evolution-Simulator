import pygame.gfxdraw

from bounds import ScreenBounds
from vector import Vector


class Entity(pygame.sprite.Sprite):
    def __init__(self, init_pos, size, image, init_vel=Vector.null()):
        super().__init__()
        # self.genes = genes
        self.image = image
        self.radius = int(size / 2)
        self.rect = pygame.Rect(init_pos.x - self.radius, init_pos.y - self.radius, size, size)
        self.position = init_pos
        self.velocity = init_vel
        self.acceleration = Vector.null()
        self.max_force = 0.1
        self.age = 0

    def update(self, screen_bounds, **kwargs):
        self.age += 1
        self._handle_boundaries(screen_bounds)
        self._calc_movement()
        self.rect.center = (round(self.position.x), round(self.position.y))
        self.acceleration = Vector.null()

    def apply_force(self, force):
        self.acceleration = self.acceleration.add(force)

    def _calc_movement(self):
        self.velocity = self.velocity.add(self.acceleration).limit()
        self.acceleration = Vector.null()
        self.position = self.position.add(self.velocity)

    def _handle_boundaries(self, screen_bounds):
        collided_bounds = screen_bounds.bounds_collided(self)
        if ScreenBounds.RIGHT in collided_bounds or ScreenBounds.LEFT in collided_bounds:
            self.velocity = self.velocity.invert_x()
        if ScreenBounds.TOP in collided_bounds or ScreenBounds.BOTTOM in collided_bounds:
            self.velocity = self.velocity.invert_y()

    def size(self):
        return self.rect.size[0]
