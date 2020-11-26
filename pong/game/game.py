import sys

import pygame

from pong.settings import WIDTH, HEIGHT
from pong.game.player import Player
from pong.game.ball import Ball
from pong.game.menu import Menu
from pong.client.pong_client import Client


class PongGame:
    def __init__(self):
        self.size = WIDTH, HEIGHT
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def new(self):
        pygame.init()
        pygame.font.init()
        self.running = True
        self.surface = pygame.display.set_mode(self.size)
        self.sprites = pygame.sprite.Group()
        self.menu_widgets = pygame.sprite.Group()
        pygame.display.set_caption("Pong")
        self.ball = Ball(self)
        self.player1 = Player(self)
        self.player2 = Player(self)
        self.score = [0, 0]
        self.menu = Menu(self)
        self.playing = False

    def init_client(self):
        self.client = Client(self, connect=True)
        self.client.set_players_positions()
    
    def cleanup(self):
        pygame.font.quit()
        pygame.quit()
        sys.exit(2)

    def render(self):
        self.sprites.draw(self.surface)
        PongGame.draw_text(self.surface, f'{self.score[0]} x {self.score[1]}',
         (255,255,255), WIDTH//2-5, 0, 32)

    def loop(self):
        self.client.update()
        self.player1.move()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def execute(self):
        self.init_client()
        while(self.running):
            for event in pygame.event.get():
                self.event(event)
            self.surface.fill((0,0,0))
            pygame.display.set_caption(f"Pong - FPS: {round(self.clock.get_fps(), 1)}")
            if self.client.is_playable:
                self.loop()
                self.render()
            else:
                self.show_waiting_window()
            pygame.display.flip()
            self.clock.tick(60)
        self.cleanup()

    def menu_screen(self):
        while not self.playing:
            for event in pygame.event.get():
                self.menu.handle_event(event)
            self.menu_widgets.draw(self.surface)
            pygame.display.flip()

    def show_waiting_window(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((162, 166, 166))
        PongGame.draw_text(surface, "Waiting opponent!", (66, 123, 245), 180, 225, 48)
        self.surface.blit(surface, (0,0))

    @staticmethod
    def draw_text(surface, text, color, x, y, size, align='topleft', font_name='Comic Sans MS'):
        font = pygame.font.SysFont(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == 'center':
            text_rect.center = (x, y)
        elif align == 'topleft':
            text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)
