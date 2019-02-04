import pygame
import os
import sys

FPS = 60
WIDTH = 1200
HEIGHT = 900
RUNNING = True
player = None


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()

    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.add(player_group)


class Dirty(pygame.sprite.Sprite):
    pass


class Ground(pygame.sprite.Sprite):
    pass


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
dirty = pygame.sprite.Group()
ground = pygame.sprite.Group()
player_group = pygame.sprite.Group()
background = pygame.image.load("data/background.png").convert()
player_image = load_image('player.png', color_key=-1)
Player(200, 200)
clock = pygame.time.Clock()

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
terminate()
