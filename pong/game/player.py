import pygame

vector = pygame.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, posx=0, posy=0):
        groups = [game.sprites]
        super().__init__(groups)
        self.game = game
        self.posx = posx
        self.posy = posy
        self.image = pygame.Surface((10, 75))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)

    def set_pos(self, x, y):
        self.rect.center = (x, y)
        self.posx = x
        self.posy = y

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.posy -= 5
        elif keys[pygame.K_DOWN]:
            self.posy += 5
        self.set_pos(self.posx, self.posy)

    @property
    def pos(self):
        return self.posx, self.posy
