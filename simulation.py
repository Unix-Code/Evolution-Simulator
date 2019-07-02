import random
from random import randint

import pygame
from pygame.sprite import Group as SpriteGroup

from bounds import ScreenBounds
from food import Food
from organism import Organism
from vector import Vector

random.seed("EVOLUTION SIMULATOR")


class Simulation:
    def __init__(self):
        pygame.init()
        self.bg_color = (127, 127, 127)
        self.screen_bounds = ScreenBounds(1600, 900)
        self.screen = pygame.display.set_mode(self.screen_bounds.bounds())
        pygame.display.set_caption('Evolution Simulator')
        self.screen.fill(self.bg_color)
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.frame_rate = 60
        self.running = False
        self.organisms = SpriteGroup()
        self.food = SpriteGroup()
        self.init_organisms()
        self.init_food()

    def init_organisms(self):
        screen_width, screen_height = self.screen_bounds.bounds()
        for x in range(0, 20):
            rand_pos = Vector(randint(100, screen_width - 100), randint(100, screen_height - 100))
            rand_vel = Vector(randint(2, Vector.MAX_SPEED), randint(2, Vector.MAX_SPEED))
            rand_organism = Organism(rand_pos, rand_vel, 30, (randint(0, 255), randint(0, 255), randint(0, 255)))
            self.organisms.add(rand_organism)

    def init_food(self):
        for x in range(0, 75):
            self.spawn_food()

    def spawn_food(self):
        screen_width, screen_height = self.screen_bounds.bounds()
        rand_pos = Vector(int(random.uniform(100, screen_width - 100)), int(random.uniform(100, screen_height - 100)))
        rand_food = Food(rand_pos, randint(20, 30))
        self.food.add(rand_food)

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def draw(self):
        self.screen.fill(self.bg_color)
        self.food.draw(self.screen)
        for x in self.organisms:
            surf = pygame.Surface((x.outer_vision_rad * 2 + 1, x.outer_vision_rad * 2 + 1), pygame.SRCALPHA)
            pygame.gfxdraw.aacircle(surf, x.outer_vision_rad, x.outer_vision_rad, x.outer_vision_rad, (255, 0, 0))
            pygame.gfxdraw.aacircle(surf, x.outer_vision_rad, x.outer_vision_rad, x.inner_vision_rad, (0, 0, 255))
            pygame.draw.rect(surf, (255, 0, 0), pygame.Rect(x.outer_vision_rad - x.rect.width / 2, x.outer_vision_rad - x.rect.height / 2, x.rect.width, x.rect.height), 1)
            self.screen.blit(surf, (x.rect.centerx - x.outer_vision_rad, x.rect.centery - x.outer_vision_rad))
        self.organisms.draw(self.screen)
        pygame.display.flip()

    def update(self):
        if len(self.food) < 75:
            self.spawn_food()
        self.organisms.update(self.screen_bounds, self.organisms.sprites(), self.food.sprites())
