import pygame
import os
import sys
# Импортирование библиотек

FPS = 30  # Количество кадров в секунду
WIDTH = 1200  # Ширина окна
HEIGHT = 800  # Высота окна
ALL_WIDTH = 0  # Длинна всего окна
RUNNING = True  # Переменная для проверки работы программы
player = None  # Основной персонаж
JUMP = False
jumpCount = 12
STEP = 10  # Перемещние ща одно нажатие


def terminate():  # Функция для выхода из игры
    pygame.quit()  # Выход pygame
    sys.exit()  # Выход из программы


def load_image(name, color_key=None):  # Функция загрузки программы
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


def load_level(filename):
    global ALL_WIDTH
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    ALL_WIDTH = max_width * 50

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == 'D':
                Tile('dirty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '#':
                Tile('ground', x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx

    # позиционировать камеру на объекте target
    def update(self, target):
        if target.x + target.rect.w // 2 >= WIDTH // 2 and \
           target.x + target.rect.w // 2 + WIDTH // 2 <= ALL_WIDTH:
            self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        else:
            self.dx = 0



class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = tile_width * pos_x
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y - 5)


pygame.init()

pygame.key.set_repeat(200, 70)

pygame.display.set_caption('Treasure hunt')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

background = pygame.image.load("data/background.png").convert()

tile_images = {'dirty': load_image('dirty.png'),
               'ground': load_image('ground.png'),
               'empty': load_image('white.png', -1)}

tile_width = tile_height = 50

player_image = load_image('player.png', color_key=-1)

player, level_x, level_y = generate_level(load_level("FirstLevel.txt"))

camera = Camera()

clock = pygame.time.Clock()

while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > -10:
        player.rect.x -= STEP
        player.x -= STEP
    if keys[pygame.K_RIGHT] and \
       player.x + player.rect.w <= ALL_WIDTH:
        player.rect.x += STEP
        player.x += STEP
    if not JUMP:
        if keys[pygame.K_UP]:
            JUMP = True
    else:
        if jumpCount >= -12:
            player.rect.y -= jumpCount
            jumpCount -= 1
        else:
            jumpCount = 12
            JUMP = False

    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    screen.blit(background, [0, 0])

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

terminate()  # Выход из игры
