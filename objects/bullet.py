import pygame
from pygame.transform import scale

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = scale(pygame.image.load("unnamed.png"), (20, 20))
        self.rect = pygame.Rect(x, y, 20, 20)
        self.yvel = 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y -= self.yvel

        if self.rect.y < -100:
            self.kill()