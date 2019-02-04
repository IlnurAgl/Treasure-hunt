import pygame
import os
import sys
# Импортирование библиотек

LIVES = 3
FPS = 30  # Количество кадров в секунду
WIDTH = 1200  # Ширина окна
HEIGHT = 800  # Высота окна
ALL_WIDTH = 0  # Длинна всего окна
RUNNING = True  # Переменная для проверки работы программы
player = None  # Основной персонаж
JUMP = False  # Переменная для прыжка
FALL = 5  # Количество пикселей при падении
jumpCount = 12  # Высота прыжка
ISFALL = False  # Переменная запрещающая прыгать
STEP = 10  # Перемещние ща одно нажатие
HARM = False
Time = 0


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


def rect_side(rect1, rect2):
    if rect1.y + 50 < rect2.y:
        return 1
    else:
        return 0    


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
            elif level[y][x] == 'E':
                Enemy(x, y)
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

    def update(self):
        global LIVES
        global HARM
        global Time
        for i in enemys:
            if self.rect.colliderect(i.rect):
                if rect_side(self.rect, i.rect):
                    i.kill()
                else:
                    if not HARM:
                        LIVES -= 1
                        HARM = True
                        Time = pygame.time.get_ticks()


pygame.init()

pygame.key.set_repeat(200, 70)

pygame.display.set_caption('Treasure hunt')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemys = pygame.sprite.Group()


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png", -1)

    def __init__(self, x, y):
        super().__init__(enemys, all_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y - 5)
        self.x = tile_width * x
        self.v = -5

    def update(self):
        a = ((self.rect.y + self.rect.h - 15) // (HEIGHT // level_y))
        b = (self.x + self.v - 10) // (WIDTH // level_x)
        if world[a][b] == '.' or \
           world[a][b] == 'E' or \
           world[a][b] == '@':
            self.x += self.v
            self.rect.x += self.v
        else:
            self.v = -self.v


background = pygame.image.load("data/background.png").convert()

tile_images = {'dirty': load_image('dirty.png'),
               'ground': load_image('ground.png'),
               'empty': load_image('white.png', -1)}

tile_width = tile_height = 50

player_image = load_image('player.png', color_key=-1)

world = load_level("FirstLevel.txt")

player, level_x, level_y = generate_level(world)

camera = Camera()

clock = pygame.time.Clock()

while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    keys = pygame.key.get_pressed()
    a = (player.rect.y + player.rect.h - 15) // (HEIGHT // level_y)
    b = (player.x - 15) // (WIDTH // level_x)
    if keys[pygame.K_LEFT] and player.x > -10 and \
       (world[a][b] == '.' or world[a][b] == 'E' or world[a][b] == '@'):
        player.rect.x -= STEP
        player.x -= STEP
    b = (player.x + 20) // (WIDTH // level_x)
    if keys[pygame.K_RIGHT] \
       and player.x + player.rect.w <= ALL_WIDTH \
       and (world[a][b] == '.' or world[a][b] == 'E' or world[a][b] == '@'):
        player.rect.x += STEP
        player.x += STEP
    if not JUMP:
        try:
            a = (player.rect.y - FALL + player.rect.h - 15)
            a = a // (HEIGHT // level_y) + 1
            if world[a][(player.x + 10) // (WIDTH // level_x)] == '.' or \
               world[a][(player.x + 10) // (WIDTH // level_x)] == 'E' or \
               world[a][(player.x + 10) // (WIDTH // level_x)] == '@':
                player.rect.y += FALL
                ISFALL = True
            else:
                ISFALL = False
        except:
            player.rect.y += FALL
        if not ISFALL and keys[pygame.K_UP]:
            JUMP = True
    else:
        if jumpCount >= -0:
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
    all_sprites.update()
    if not HARM:
        player.update()
    else:
        if pygame.time.get_ticks() - Time > 1800:
            HARM = False

    pygame.display.flip()

    clock.tick(FPS)

terminate()  # Выход из игры
