import pygame

from pong.settings import WIDTH, HEIGHT
from pong.game.player import Player
from pong.game.ball import Ball
from pong.client.pong_client import Client

# functions
def draw_text(surface, text, color, x, y, size, font_name='Comic Sans MS'):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# HUD
def show_waiting_window(window):
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill((162, 166, 166))
    draw_text(surface, "Waiting opponent!", (66, 123, 245), 180, 225, 48)
    window.blit(surface, (0,0))


class PongGame:
    def __init__(self):
        self.size = WIDTH, HEIGHT
        self.running = False
        self.surface = None
        self.clock = pygame.time.Clock()

    def init(self):
        pygame.init()
        pygame.font.init()
        self.client = Client()
        self.client.connect_server()
        self.running = True
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")
        self.sprites = pygame.sprite.Group()

        if self.client.is_host:
            self.player1 = Player(self, 10, HEIGHT//2)
            self.player2 = Player(self, WIDTH-10, HEIGHT//2)
        else:
            self.player1 = Player(self, WIDTH-10, HEIGHT//2)
            self.player2 = Player(self, 10, HEIGHT//2)

        self.ball = Ball(self)
        self.score = [0, 0]
        
        
    def cleanup(self):
        pygame.font.quit()
        pygame.quit()

    def render(self):
        self.sprites.draw(self.surface)
        draw_text(self.surface, f'{self.score[0]} x {self.score[1]}',
         (255,255,255), WIDTH//2-5, 0, 32)

    def loop(self):
        self.client.update(self)
        self.player1.move()

    def event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def execute(self):
        self.init()
        while(self.running):
            for event in pygame.event.get():
                self.event(event)
            self.surface.fill((0,0,0))
            pygame.display.set_caption(f"Pong - FPS: {round(self.clock.get_fps(), 1)}")
            if self.client.is_playable:
                self.loop()
                self.render()
            else:
                show_waiting_window(self.surface)
            pygame.display.flip()
            self.clock.tick(60)
        self.cleanup()
