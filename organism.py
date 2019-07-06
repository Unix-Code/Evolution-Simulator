import pygame

from entity import Entity
from genome import Genome
from vector import Vector


class Organism(Entity):
    MAX_HEALTH = 500

    def __init__(self, init_pos, init_vel, size, color, genome=None):
        self.genome = Genome(**dict(outer_vision_rad=int(size / 2) + 100,
                                    inner_vision_rad=int(size / 2) + 30,
                                    food_pref=1, poison_pref=-0.25,
                                    max_speed=8))
        super().__init__(init_pos, size, self.get_sprite_img(size, color), init_vel)
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
            return pygame.sprite.collide_circle(left, right)

        orig_rad = self.radius
        self.radius = self.genome.get("inner_vision_rad")
        food_inside_inner_rad = pygame.sprite.spritecollide(self, food, False, my_collide_circle)
        self.radius = self.genome.get("outer_vision_rad")
        food_inside_outer_rad = pygame.sprite.spritecollide(self, food, False, my_collide_circle)
        food_seen = [food for food in food_inside_outer_rad if food not in food_inside_inner_rad]
        self.radius = orig_rad
        if food_seen:
            food_vectors = [Vector(*f.rect.center).mult(-1 if self.genome.get("food_pref") < 0 else 1) for f in food_seen if not f.poisonous]
            poison_vectors = [Vector(*f.rect.center).mult(-1 if self.genome.get("poison_pref") < 0 else 1) for f in food_seen if f.poisonous]

            if food_vectors:
                food_force = Vector.steer_forces(food_vectors,
                                                 Vector(*self.rect.center),
                                                 self.velocity, self.max_force,
                                                 self.genome.get("max_speed"))
                self.apply_force(food_force.mult(abs(self.genome.get("food_pref"))))
            if poison_vectors:
                poison_force = Vector.steer_forces(poison_vectors,
                                                   Vector(*self.rect.center),
                                                   self.velocity, self.max_force,
                                                   self.genome.get("max_speed"))
                self.apply_force(poison_force.mult(abs(self.genome.get("poison_pref"))))

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
        return max(min(red, 255), 0), max(min(green, 255), 0), blue

    def change_color(self, color):
        self.image = self.get_sprite_img(self.size(), color)

    @classmethod
    def get_sprite_img(cls, size, color):
        sprite_img = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(sprite_img, int(size / 2), int(size / 2), int(size / 2), color)
        pygame.gfxdraw.filled_circle(sprite_img, int(size / 2), int(size / 2), int(size / 2), color)
        return sprite_img
