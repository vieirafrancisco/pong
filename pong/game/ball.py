import pygame

from pong.settings import WIDTH, HEIGHT


class Ball(pygame.sprite.Sprite):
    def __init__(self, game):
        groups = [game.sprites]
        super().__init__(groups)
        self.game = game
        self.posx = WIDTH//2
        self.posy = HEIGHT//2
        self.x_dir = -1
        self.y_dir = 2
        self.image = pygame.Surface((10,10))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.posx, self.posy)

    def update(self):
        """
        rep: 
           0: no collision
           1: collisition with player
           2: outbounds
        """
        resp = 0
        self.posx += self.x_dir
        self.posy += self.y_dir
        if self.posy < 0 or self.posy > HEIGHT+10:
            self.y_dir *= -1
        if self.has_collided:
            resp = 1
            self.x_dir *= -1
            self.posx += 10 * self.x_dir
        if self.is_outbounds:
            resp = 2
            self.posx = WIDTH//2
            self.posy = HEIGHT//2
        self.rect.center = (self.posx, self.posy)

        return resp

    @property
    def pos(self):
        return self.posx, self.posy

    @property
    def has_collided(self):
        return len(pygame.sprite.spritecollide(self, self.game.sprites, False)) > 1

    @property
    def is_outbounds(self):
        return self.posx < 0 or self.posx > WIDTH
    
    def set_pos(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.rect.center = (self.posx, self.posy)
