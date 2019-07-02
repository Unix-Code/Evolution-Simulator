import pygame

from entity import Entity
from utils import max_by
from vector import Vector


class Organism(Entity):
    MAX_HEALTH = 500

    def __init__(self, init_pos, init_vel, size, color):
        outer_rad = int(size / 2) + 100
        inner_rad = int(size / 2) + 30
        super().__init__(init_pos, size, self.get_sprite_img(size, color), init_vel)
        self.outer_vision_rad = outer_rad
        self.inner_vision_rad = inner_rad
        self.health = self.MAX_HEALTH

    def update(self, screen_bounds, organisms, food):
        super().update(screen_bounds)
        self.health = max(0, self.health - 1)
        self._handle_food_eaten(food)
        self._look_for_food(food)
        if self.health <= 0:
            self.kill()

    def _look_for_food(self, food):
        def my_collide_circle(left, right):
            # print(left)
            # print(right)
            # print(left.radius)
            # print("\n")
            return pygame.sprite.collide_circle(left, right)

        orig_rad = self.radius
        self.radius = self.inner_vision_rad
        food_inside_inner_rad = pygame.sprite.spritecollide(self, food, False, my_collide_circle)
        self.radius = self.outer_vision_rad
        food_inside_outer_rad = pygame.sprite.spritecollide(self, food, False, my_collide_circle)
        food_seen = [food for food in food_inside_outer_rad if food not in food_inside_inner_rad]
        selected_food = max_by(food_seen, lambda f: f.size())
        self.radius = orig_rad
        if selected_food is not None:
            self.apply_force(Vector.steer_force(Vector(*selected_food.rect.center),
                                                Vector(*self.rect.center),
                                                self.velocity, self.max_force))

    def _handle_food_eaten(self, food):
        food_eaten = pygame.sprite.spritecollide(self, food, False, pygame.sprite.collide_circle)
        health_diff = 0
        for food_entity in food_eaten:
            health_diff += food_entity.value
            food_entity.kill()

        self.health = min(self.MAX_HEALTH, self.health + health_diff)
        new_color = self._calc_health_color()
        self.change_color(new_color)

    def _calc_health_color(self):
        blue = 0
        red = int(255 * ((self.MAX_HEALTH - self.health) / self.MAX_HEALTH))
        green = int(255 * (self.health / self.MAX_HEALTH))
        return red, green, blue

    def change_color(self, color):
        self.image = self.get_sprite_img(self.size(), color)

    @classmethod
    def get_sprite_img(cls, size, color):
        sprite_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(sprite_img, int(size / 2), int(size / 2), int(size / 2), color)
        pygame.gfxdraw.filled_circle(sprite_img, int(size / 2), int(size / 2), int(size / 2), color)
        return sprite_img
