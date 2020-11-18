import pygame
from pygame.locals import *

from src.settings import WIDTH, HEIGHT

class PongGame:
    def __init__(self):
        self.size = WIDTH, HEIGHT
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def init(self):
        pygame.init()
        self.running = True
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")

    def cleanup(self):
        pygame.quit()

    def render(self):
        pass

    def loop(self):
        pygame.display.set_caption(f"Pong - FPS: {round(self.clock.get_fps(), 1)}")

    def event(self, event):
        if event.type == QUIT:
            self.running = False

    def execute(self):
        self.init()
        while(self.running):
            for event in pygame.event.get():
                self.event(event)
            self.surface.fill((0,0,0))
            self.loop()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        self.cleanup()
