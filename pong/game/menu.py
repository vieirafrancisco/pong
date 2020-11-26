import pygame

from pong.settings import WIDTH, HEIGHT

def test_callback():
    print('yeyy')


class Menu(pygame.sprite.Sprite):
    def __init__(self, game):
        groups = [game.menu_widgets]
        super().__init__(groups)
        self.game = game
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((0,0,0))
        self.game.draw_text(self.image, 'Pong', (255,255,255), WIDTH//2-65, 125, 50, align='topleft')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.quit_button = Button(game, WIDTH-30, HEIGHT-50, 40, 30, 'Sair', self.game.cleanup)
        self.enter_match_button = Button(game, WIDTH//2, HEIGHT-150, 200, 30, 'Partida Online', self.play_online_callback)
        self.enter_already_created_match_button = Button(game, WIDTH//2, HEIGHT-110, 250, 30, 'Entrar em partida existente', test_callback)
        self.create_match = Button(game, WIDTH//2, HEIGHT-70, 250, 30, 'Criar Partida', self.create_match_callback)
        self.buttons = [self.quit_button, self.enter_match_button, self.enter_already_created_match_button, self.create_match]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.cleanup()
        for button in self.buttons:
            button.handle_event(event)

    def play_online_callback(self):
        self.game.playing = True

    def create_match_callback(self):
        return self.game.client


class Button(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, text, callback):
        groups = [game.menu_widgets]
        super().__init__(groups)
        self.game = game
        self.x = x
        self.y = y
        self.text = text
        self.callback = callback
        self.image = pygame.Surface((w, h))
        self.image.fill((0,0,0))
        self.game.draw_text(self.image, text, (255,255,255), w//2, h//2, 18, align='center')
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        pygame.draw.rect(self.image, (255,255,255), (0,0,w,h), width=2)
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()
            self.button_down = False
