import pygame
import os
import sys
# Импортирование библиотек

LIVES = 3  # Количество жизней
FPS = 60  # Количество кадров в секунду
WIDTH = 1200  # Ширина окна
ALL_WIDTH = 0  # Длинна всего игрового поля
HEIGHT = 800  # Высота окна
RUNNING = True  # Переменная для проверки работы программы
player = None  # Основной персонаж
JUMP = False  # Переменная для прыжка
DAMAGE = False  # Переменная при получении урона
FALL = False  # Количество пикселей при падении
jumpCount = 12  # Высота прыжка
STEP = 10  # Перемещние ща одно нажатие
LEFT = True  # Можно ли идти влево
RIGHT = True  # Можно ли идти вправо
TIME = 0  # Время


def load_image(name, color_key=None):  # Функция загрузки программы
    fullname = os.path.join('data', name)  # Открытие файла

    try:
        image = pygame.image.load(fullname)  # Открыть фалй
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)  # Создать исключение

    image = image.convert()  # Конверировании изображения

    if color_key is not None:  # Если передан аргумент
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)  # Убрать фон у картинки
    return image  # Вернуть изображение


def terminate():  # Функция для выхода из игры
    pygame.quit()  # Выход pygame
    sys.exit()  # Выход из программы


def startGame():  # Функция для начала игры
    # Фоновое изображение
    start = pygame.image.load("data/start.png").convert()
    Start()  # Спрайт начала игры
    Exit()  # Спрайт для выхода
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()  # Выход если нажата кнопка
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in main_group:
                    if i.clicked(event.pos) == 1:
                        return  # Если нажата кнопка для игры, начать игру
                    elif i.clicked(event.pos) == 2:
                        terminate()  # Если нажата кнопка для выхожа, выйти
        screen.blit(start, [0, 0])  # Вывод изображения
        main_group.draw(screen)  # Вывод спрайтов
        pygame.display.flip()  # Обновление картинки
        clock.tick(FPS)  # Количество кадров в секунду


def gameOver():  # Функция для конца игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                terminate()  # Выход при нажатии любой кнопка
        screen.blit(overImage, [0, 0])  # Вывод фонового изображения
        pygame.display.flip()  # Обновления картинки


# Функция для проверки с какой стороны столкнулись спрайты
def rect_side(rect1, rect2):
    # 1 справа
    # 2 слева
    # 3 сверху
    # 4 снизу
    if rect1.y + rect1.h - 10 < rect2.y:
        return 3
    if rect1.x + rect1.w >= rect2.x and rect1.x < rect2.x:
        return 1
    elif rect2.x + rect2.w >= rect1.x and rect2.x < rect1.x:
        return 2
    else:
        return 4


def load_level(filename):  # Функция для получения списка из игры
    global ALL_WIDTH
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    ALL_WIDTH = (max_width - 1) * 50

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def camera_configure(camera, target_rect):  # Конфигурации камеры
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIDTH / 2, -t + HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width-WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height-HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


def generate_level(level):  # Функция для создания уровня
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'D':
                Tile('dirty', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
            elif level[y][x] == '#':
                Tile('ground', x, y)
            elif level[y][x] == 'E':
                Enemy(x, y)  # Создания спрайта
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)


class Camera:

    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class Player(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y - 5)

    def update(self):
        global LEFT
        global RIGHT
        global JUMP
        global FALL
        global LIVES
        global DAMAGE
        global TIME
        t = False
        for i in tiles_group:
            if self.rect.colliderect(i.rect):
                if rect_side(self.rect, i.rect) == 1:
                    RIGHT = False
                    break
                elif rect_side(self.rect, i.rect) == 2:
                    LEFT = False
                    break
                elif rect_side(self.rect, i.rect) == 3:
                    t = True
            else:
                LEFT = True
                RIGHT = True
        if not t and not JUMP and LEFT and RIGHT:
            FALL = True
        else:
            FALL = False

        if not DAMAGE:
            for i in enemys:
                if self.rect.colliderect(i.rect):
                    if rect_side(self.rect, i.rect) == 3 and not JUMP:
                        i.kill()
                    else:
                        LIVES -= 1
                        DAMAGE = True
                        TIME = pygame.time.get_ticks()
                        if LIVES == 0:
                            gameOver()


pygame.init()

pygame.key.set_repeat(200, 70)

pygame.display.set_caption('Treasure hunt')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

main_group = pygame.sprite.Group()


class Start(pygame.sprite.Sprite):
    image = load_image('startgame.png', -1)

    def __init__(self):
        super().__init__(main_group)
        self.image = Start.image
        self.rect = self.image.get_rect().move(500, 350)

    def clicked(self, cord):
        if cord[0] >= self.rect.x and \
           cord[0] <= self.rect.x + self.rect.w and \
           cord[1] >= self.rect.y and \
           cord[1] <= self.rect.y + self.rect.h:
            return 1


class Exit(pygame.sprite.Sprite):
    image = load_image('exit.png', -1)

    def __init__(self):
        super().__init__(main_group)
        self.image = Exit.image
        self.rect = self.image.get_rect().move(500, 450)

    def clicked(self, cord):
        if cord[0] >= self.rect.x and \
           cord[0] <= self.rect.x + self.rect.w and \
           cord[1] >= self.rect.y and \
           cord[1] <= self.rect.y + self.rect.h:
            return 2


startGame()

overImage = load_image('gameover.png')


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png", -1)

    def __init__(self, x, y):
        super().__init__(enemys, all_sprites)
        self.image = Enemy.image
        self.rect = self.image.get_rect().move(tile_width * x,
                                               tile_height * y - 5)
        self.v = -5

    def update(self):
        for i in tiles_group:
            if self.rect.colliderect(i.rect):
                if rect_side(self.rect, i.rect) == 1:
                    self.v = -self.v
                    self.image = pygame.transform.flip(self.image, 1, 0)
                elif rect_side(self.rect, i.rect) == 2:
                    self.v = -self.v
                    self.image = pygame.transform.flip(self.image, 1, 0)
        self.rect.x += self.v


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemys = pygame.sprite.Group()

background = pygame.image.load("data/background.png").convert()

lives = load_image('lives.png', -1)

tile_images = {'dirty': load_image('dirty.png'),
               'ground': load_image('ground.png'),
               'empty': load_image('white.png', -1)}

tile_width = tile_height = 50

player_image = load_image('player.png', color_key=-1)

load_image = load_image('lives.png', color_key=-1)

world = load_level("FirstLevel.txt")

player, level_x, level_y = generate_level(world)

total_level_width = (level_x + 1) * tile_width
# Высчитываем фактическую ширину уровня

total_level_height = (level_y + 1) * tile_height  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)

while RUNNING:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and player.rect.x < ALL_WIDTH and RIGHT:
        player.rect.x += STEP
        player.image = player_image
    if keys[pygame.K_LEFT] and player.rect.x > -10 and LEFT:
        player.rect.x -= STEP
        player.image = pygame.transform.flip(player_image, 1, 0)
    if not JUMP and not FALL:
        if keys[pygame.K_UP]:
            JUMP = True
    else:
        if jumpCount >= 0 and not FALL:
            player.rect.y -= jumpCount
            jumpCount -= 1
        else:
            jumpCount = 12
            JUMP = False
    if FALL:
        player.rect.y += 4

    screen.blit(background, [0, 0])

    for i in range(LIVES):
        screen.blit(lives, [i * 50, 0])

    camera.update(player)

    for e in all_sprites:
        screen.blit(e.image, camera.apply(e))
    all_sprites.update()

    if DAMAGE:
        if pygame.time.get_ticks() - TIME > 1200:
            DAMAGE = False

    pygame.display.flip()

    clock.tick(FPS)

terminate()  # Выход из игры
