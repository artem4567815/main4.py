import pygame
from pygame.transform import scale
from pygame import *


class Platform(sprite.Sprite):
    def __init__(self, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = Surface((width, height))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, width, height)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 50, 50)
        self.image = scale(pygame.image.load("shit.png"), (50, 50))
        self.xvel = 0
        self.yvel = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.yvel = -50
            self.jumping = True
        else:
            print("cant jump")

    def update(self, left, right):
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5

        if not (left or right):
            self.xvel = 0

        self.yvel += 3
        self.rect.x += self.xvel
        self.rect.y += self.yvel

        for p in platforms:
            if p.rect.colliderect(self.rect):
                if self.jumping:
                    print("yes")
                had_vertical_collision = False
                if self.yvel < 0:
                    if p.rect.bottom >= self.rect.top >= p.rect.top:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0
                        had_vertical_collision = True

                if self.yvel > 0:
                    if p.rect.top <= self.rect.bottom <= p.rect.bottom:
                        self.rect.bottom = p.rect.top
                        self.yvel = 0
                        self.jumping = False
                        had_vertical_collision = True


                if not had_vertical_collision:
                    if p.rect.right >= self.rect.left >= p.rect.left:
                        self.rect.left = p.rect.right
                        self.xvel = 0

                    if p.rect.left <= self.rect.right <= p.rect.right:
                        self.rect.right = p.rect.left
                        self.xvel = 0

        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.yvel = 0
            self.jumping = False

        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


left = False
right = False

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("GAME")
ship = Spaceship(400, 300)
sky = pygame.image.load("img.png")
clock = pygame.time.Clock()
platforms = []
entities = pygame.sprite.Group()

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"
level = [
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "-     -     -     -     "
    "                        "]

x = y = 0
for row in level:
    for col in row:
        if col == "-":
            pf = Platform(x, y, 32 * 5, 32)
            platforms.append(pf)
            entities.add(pf)

        # if "-----" in row:
        #     pf = Platform(x, y)
        #     platforms.append(pf)
        #     entities.add(pf)

        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

while True:
    screen.blit(sky, (0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            ship.jump()

    ship.update(left, right)
    ship.draw(screen)
    entities.draw(screen)
    pygame.display.update()
    clock.tick(60)
