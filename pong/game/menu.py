import pygame
from functools import partial
from pong.settings import WIDTH, HEIGHT

def test_callback():
    print('yeyy')

def draw_text(surface, text, color, x, y, size, align='topleft', font_name='Comic Sans MS'):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == 'center':
        text_rect.center = (x, y)
    elif align == 'topleft':
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


class Menu:
    def __init__(self, game):
        self.game = game
        self.windows = [MainMenuWindow(self), MatchListWindow(self)]
        self.curr_window = 0

    def draw(self, surface):
        self.windows[self.curr_window].group.draw(surface)

    def toggle_window(self):
        self.curr_window = (self.curr_window + 1) % len(self.windows)
        self.windows[self.curr_window].show()

    def cleanup(self):
        self.game.cleanup()

    def play_queue(self):
        self.game.playing = True
        self.game.client.player.connect_match(None)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.cleanup
        self.windows[self.curr_window].handle_event(event)

    def show(self):
        pass


class MainMenuWindow(pygame.sprite.Sprite):
    def __init__(self, menu):
        self.group = pygame.sprite.Group()
        super().__init__([self.group])
        self.menu = menu
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((0,0,0))
        draw_text(self.image, 'Pong:', (255,255,255), WIDTH//2-50, 50, 50, align='topleft')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.quit_button = Button(self.group, WIDTH-30, HEIGHT-50, 40, 30, 'Sair', self.menu.cleanup)
        self.enter_match_button = Button(self.group, WIDTH//2, HEIGHT-150, 200, 30, 'Partida Online', self.menu.play_queue)
        self.enter_already_created_match_button = Button(self.group, WIDTH//2, HEIGHT-110, 250, 30, 'Entrar em partida existente', self.menu.toggle_window)
        self.create_match = Button(self.group, WIDTH//2, HEIGHT-70, 250, 30, 'Criar Partida', self.create_match_callback)
        self.buttons = [self.quit_button, self.enter_match_button, self.enter_already_created_match_button, self.create_match]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.menu.cleanup()
        for button in self.buttons:
            button.handle_event(event)

    def create_match_callback(self):
        self.menu.game.client.player.create_match()
        self.menu.game.playing = True

    def show(self):
        pass


class MatchListWindow(pygame.sprite.Sprite):
    def __init__(self, menu):
        self.group = pygame.sprite.Group()
        super().__init__([self.group])
        self.menu = menu
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((0,0,0))
        draw_text(self.image, 'Lista de Partidas:', (255,255,255), WIDTH//2-100, 50, 30, align='topleft')
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.menu_button = Button(self.group, WIDTH-50, HEIGHT-50, 70, 30, 'Menu', self.menu.toggle_window)
        self.buttons = [self.menu_button]
        self.base_buttons = self.buttons
        self.match_list = []
        
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.menu.cleanup()
        for button in self.buttons:
            button.handle_event(event)

        self.update_match_list()

    def update_match_list(self):
        match_list = self.menu.game.client.get_matchs()["match_list"]

        if match_list != self.match_list:
            self.match_list = match_list
            self.render_match_list()

    def show(self):
        pass

    def render_match_list(self):
        def connect_match(match_id):
            self.menu.game.playing = True
            self.menu.game.client.player.connect_match(match_id)

        button_matchs = []
        for i, match in enumerate(self.match_list):
            button_matchs.append(Button(self.group, WIDTH//2, HEIGHT-350+35*i, 200, 30, 
                                        match["match_name"], partial(connect_match, match_id=match["match_id"])))

        self.buttons = self.base_buttons + button_matchs

class Button(pygame.sprite.Sprite):
    def __init__(self, group, x, y, w, h, text, callback):
        super().__init__([group])
        self.x = x
        self.y = y
        self.text = text
        self.callback = callback
        self.image = pygame.Surface((w, h))
        self.image.fill((0,0,0))
        draw_text(self.image, text, (255,255,255), w//2, h//2, 18, align='center')
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
