import pygame


class EventHandler:
    def handle_events(self, sim):
        for event in pygame.event.get():
            self.handle_event(event, sim)

    def handle_event(self, event, sim):
        if event.type == pygame.QUIT:
            sim.stop()
