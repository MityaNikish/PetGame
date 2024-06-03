import pygame
import random
import os

# размер окна
WIDTH = 1280
HEIGHT = 720

# коэф-ты размера
ratio_width = WIDTH / 1280
ratio_height = HEIGHT / 720

# размер клетчетого поля
N_cell_WIDTH = 30
N_cell_HEIGHT = 20

# размер квадратной клетки
cell_size = round(min(HEIGHT, WIDTH) * 0.8 / N_cell_HEIGHT)

# крайняя левая верхняя позиция поля
pos_cel_x = (WIDTH - cell_size * N_cell_WIDTH) / 2
pos_cel_y = (HEIGHT - cell_size * N_cell_HEIGHT) / 2

# частота кадров
FPS = 30

# счетчик очереди
motion = 1

# счетчик пропусков
skip_counter = 0

# игровые очки
player1_score = 9
player2_score = 9

# код победившего
player_win = -1

delay = 0

# настройка вкл/выкл бота
bot = False

# настройка папки ассетов
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_folder = os.path.join(game_folder, 'snd')
fonts_folder = os.path.join(game_folder, 'fonts')

# настройка музыки
# sound = pygame.mixer.Sound(os.path.join(snd_folder, 'sound.wav'))
# click = pygame.mixer.Sound(os.path.join(snd_folder, 'click.wav'))

# настройка фона
background = pygame.image.load(os.path.join(img_folder, 'grass.png'))
background_new_game_size = pygame.transform.scale(background, (WIDTH, round(WIDTH / 16 * 9)))
background_new_game_rect = background_new_game_size.get_rect()

background = pygame.image.load(os.path.join(img_folder, 'popit.png'))
background_mine_menu_size = pygame.transform.scale(background, (WIDTH, round(WIDTH / 16 * 9)))
background_mine_menu_rect = background_mine_menu_size.get_rect()

# настройка изображения спрайтов для меню
body_box_mine_menu_img = pygame.image.load(os.path.join(img_folder, 'body_box_mine_menu.png'))
header_box_mine_menu_img = pygame.image.load(os.path.join(img_folder, 'header_box_mine_menu.png'))
yellow_button_img = pygame.image.load(os.path.join(img_folder, 'yellow_button.png'))
yellow_button_press_img = pygame.image.load(os.path.join(img_folder, 'yellow_button_press.png'))
red_button_img = pygame.image.load(os.path.join(img_folder, 'red_button.png'))
red_button_press_img = pygame.image.load(os.path.join(img_folder, 'red_button_press.png'))
blue_button_img = pygame.image.load(os.path.join(img_folder, 'blue_button.png'))
blue_button_press_img = pygame.image.load(os.path.join(img_folder, 'blue_button_press.png'))
green_button_img = pygame.image.load(os.path.join(img_folder, 'green_button.png'))
green_button_press_img = pygame.image.load(os.path.join(img_folder, 'green_button_press.png'))
red_short_button_img = pygame.image.load(os.path.join(img_folder, 'red_short_button.png'))
red_short_button_press_img = pygame.image.load(os.path.join(img_folder, 'red_short_button_press.png'))
red_cross_img = pygame.image.load(os.path.join(img_folder, 'red_cross.png'))
white_cross_img = pygame.image.load(os.path.join(img_folder, 'white_cross.png'))
red_circle_img = pygame.image.load(os.path.join(img_folder, 'red_circle.png'))
grey_box_img = pygame.image.load(os.path.join(img_folder, 'grey_box.png'))
green_checkmark_img = pygame.image.load(os.path.join(img_folder, 'green_checkmark.png'))
white_checkmark_img = pygame.image.load(os.path.join(img_folder, 'white_checkmark.png'))

# настройка изображения спрайтов для игры
cell_img = pygame.image.load(os.path.join(img_folder, 'grey.png'))
blue_team_img = pygame.image.load(os.path.join(img_folder, 'blue.png'))
blue_full_team_img = pygame.image.load(os.path.join(img_folder, 'blue_full.png'))
green_team_img = pygame.image.load(os.path.join(img_folder, 'green.png'))
green_full_team_img = pygame.image.load(os.path.join(img_folder, 'green_full.png'))

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
AQUA = (0, 255, 255)
LawnGreen = (124, 252, 0)
LawnGreenToo = (100, 255, 100)
LightGrey = (211, 211, 211)


def inherit(group_sprites1, group_sprites2, group_sprites3, img):
    cell_replacement = pygame.sprite.groupcollide(group_sprites1, group_sprites2, True, True)

    for amn in cell_replacement:
        figure_pos_x = amn.rect.x
        figure_pos_y = amn.rect.y
        break

    group_sprites3 = creature(figure_size_width, figure_size_height, figure_pos_x, figure_pos_y, img, group_sprites3)


def touch_groups(group_sprites1, group_sprites2):
    touch = False
    all_sprites_team.update(pygame.K_UP)
    if pygame.sprite.groupcollide(group_sprites1, group_sprites2, False, False):
        touch = True
    all_sprites_team.update(pygame.K_DOWN)
    all_sprites_team.update(pygame.K_DOWN)
    if pygame.sprite.groupcollide(group_sprites1, group_sprites2, False, False):
        touch = True
    all_sprites_team.update(pygame.K_UP)
    all_sprites_team.update(pygame.K_RIGHT)
    if pygame.sprite.groupcollide(group_sprites1, group_sprites2, False, False):
        touch = True
    all_sprites_team.update(pygame.K_LEFT)
    all_sprites_team.update(pygame.K_LEFT)
    if pygame.sprite.groupcollide(group_sprites1, group_sprites2, False, False):
        touch = True
    all_sprites_team.update(pygame.K_RIGHT)
    return touch


# настройка шрифта
font_name = os.path.join(fonts_folder, 'Kenney Future.ttf')


def draw_text(surf, text, size, color, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)


class Box_body(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(body_box_mine_menu_img, (width, hight))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Box_header(pygame.sprite.Sprite):
    def __init__(self, width, hight, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(header_box_mine_menu_img, (width, hight))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Button(pygame.sprite.Sprite):
    def __init__(self, img, width, height, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def press(self, img, width, height, x, y):
        self.image = pygame.transform.scale(img, (width, height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Cell(pygame.sprite.Sprite):
    def __init__(self, img, pos_cel_cal_x, pos_cel_cal_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (cell_size, cell_size))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = pos_cel_cal_x
        self.rect.y = pos_cel_cal_y

    def update(self, event):
        self.speedx = 0

        if event == pygame.K_LEFT:
            self.speedx = -cell_size
        if event == pygame.K_RIGHT:
            self.speedx = cell_size
        self.rect.x += self.speedx

        self.speedy = 0
        if event == pygame.K_UP:
            self.speedy = -cell_size
        if event == pygame.K_DOWN:
            self.speedy = cell_size
        self.rect.y += self.speedy


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        if x1 == x2:
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([1, y2 - y1])
            self.image.fill(GREEN)
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        if y1 == y2:
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([x2 - x1, 1])
            self.image.fill(GREEN)
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen_mine_menu = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

screen_new_game = pygame.display.set_mode((WIDTH, HEIGHT))
# sound.play()

# группы спрайтов
all_sprites_game_over = pygame.sprite.Group()
all_sprites_new_game = pygame.sprite.Group()
all_sprites_mine_menu = pygame.sprite.Group()
all_sprites_settings = pygame.sprite.Group()
all_sprites_border = pygame.sprite.Group()
all_sprites_team = pygame.sprite.Group()
all_sprites_blue_full_team = pygame.sprite.Group()
all_sprites_green_full_team = pygame.sprite.Group()
all_sprites_green_team = pygame.sprite.Group()

# Спрайты для ГРАНИЦ ИГОВОГО ПОЛЯ
all_sprites_border.add(Border(pos_cel_x - 5, pos_cel_y - 5, WIDTH - pos_cel_x + 5, pos_cel_y - 5))
all_sprites_border.add(Border(pos_cel_x - 5, HEIGHT - pos_cel_y + 5, WIDTH - pos_cel_x + 5, HEIGHT - pos_cel_y + 5))
all_sprites_border.add(Border(pos_cel_x - 5, pos_cel_y - 5, pos_cel_x - 5, HEIGHT - pos_cel_y + 5))
all_sprites_border.add(Border(WIDTH - pos_cel_x + 5, pos_cel_y - 5, WIDTH - pos_cel_x + 5, HEIGHT - pos_cel_y + 5))

# Спрайты для КОРОБКИ конца игры
all_sprites_game_over.add(Box_body(round(ratio_width * 380), round(ratio_height * 190), WIDTH / 2, HEIGHT / 2))

# Спрайты для КНОПОК конца игры
button_game_over_new_game = Button(yellow_button_img, round(ratio_width * 254), round(ratio_height * 66), 300,
                                   HEIGHT / 2)
all_sprites_game_over.add(button_game_over_new_game)
button_game_over_mine_menu = Button(yellow_button_img, round(ratio_width * 254), round(ratio_height * 66), WIDTH - 300,
                                    HEIGHT / 2)
all_sprites_game_over.add(button_game_over_mine_menu)

# Спрайты для КОРОБКИ главного меню
box_header_mine_menu = Box_header(round(ratio_width * 190), round(ratio_height * 45), WIDTH / 2, HEIGHT / 2 - 110)
all_sprites_mine_menu.add(box_header_mine_menu)
box_body_mine_menu = Box_body(round(ratio_width * 190), round(ratio_height * 190), WIDTH / 2, HEIGHT / 2)
all_sprites_mine_menu.add(box_body_mine_menu)

# Спрайты для КНОПОК главного меню
button_settings = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2, HEIGHT / 2)
all_sprites_mine_menu.add(button_settings)
button_new_game = Button(yellow_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2,
                         HEIGHT / 2 - 50)
all_sprites_mine_menu.add(button_new_game)

# Спрайты для КОРОБКИ настроек
box_header_settings = Box_header(round(ratio_width * 280), round(ratio_height * 45), WIDTH / 2, HEIGHT / 2 - 200)
all_sprites_settings.add(box_header_settings)
box_body_settings = Box_body(round(ratio_width * 280), round(ratio_height * 370), WIDTH / 2, HEIGHT / 2)
all_sprites_settings.add(box_body_settings)

# Спрайты для КНОПОК настроек
cross_settings = Button(red_cross_img, round(ratio_width * 18), round(ratio_height * 18), WIDTH / 2 + 120,
                        HEIGHT / 2 - 200)
all_sprites_settings.add(cross_settings)
green_button = Button(green_button_img, round(ratio_width * 170), round(ratio_height * 50), WIDTH / 2 + 40,
                      HEIGHT / 2 + 140)
all_sprites_settings.add(green_button)
all_sprites_settings.add(
    Button(white_checkmark_img, round(ratio_width * 21), round(ratio_height * 20), WIDTH / 2 - 20, HEIGHT / 2 + 140))
red_short_button = Button(red_short_button_img, round(ratio_width * 50), round(ratio_height * 50), WIDTH / 2 - 90,
                          HEIGHT / 2 + 140)
all_sprites_settings.add(red_short_button)
all_sprites_settings.add(
    Button(white_cross_img, round(ratio_width * 21), round(ratio_height * 20), WIDTH / 2 - 90, HEIGHT / 2 + 140))
grey_box1 = Button(grey_box_img, round(ratio_width * 38), round(ratio_height * 36), WIDTH / 2 - 50, HEIGHT / 2 - 150)
all_sprites_settings.add(grey_box1)
grey_box2 = Button(grey_box_img, round(ratio_width * 38), round(ratio_height * 36), WIDTH / 2 - 50, HEIGHT / 2 - 100)
all_sprites_settings.add(grey_box2)
green_checkmark = Button(green_checkmark_img, round(ratio_width * 21), round(ratio_height * 20), WIDTH / 2 - 50,
                         HEIGHT / 2 - 150)
all_sprites_settings.add(green_checkmark)

# Спрайты для КНОПОК новой игры
button_skip = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2, HEIGHT / 2 + 320)
all_sprites_new_game.add(button_skip)
button_surrender_player1 = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), 80, 80)
all_sprites_new_game.add(button_surrender_player1)
button_surrender_player2 = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH - 80, 80)
all_sprites_new_game.add(button_surrender_player2)
all_sprites_new_game.add(Button(blue_button_img, round(ratio_width * 127), round(ratio_height * 33), 80, 20))
all_sprites_new_game.add(Button(green_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH - 80, 20))


# Спрайты для КЛЕТОК(поля, шаблон и территории синей и зеленой команд) новой игры
def creature(N_WIDTH, N_HEIGHT, pos_x, pos_y, img, all_sprites):
    redpos_x = pos_x
    redpos_y = pos_y
    for i in range(N_WIDTH * N_HEIGHT):
        cell = Cell(img, redpos_x, redpos_y)
        all_sprites.add(cell)
        redpos_x += cell_size
        if redpos_x == cell_size * N_WIDTH + pos_x:
            redpos_x = pos_x
            redpos_y += cell_size
    return all_sprites


# генерация клетчетого поля
all_sprites_new_game = creature(N_cell_WIDTH, N_cell_HEIGHT, pos_cel_x, pos_cel_y, cell_img, all_sprites_new_game)

# генерация первого шаблона
figure_size_width = random.randint(1, 6)
figure_size_height = random.randint(1, 6)
all_sprites_team = creature(figure_size_width, figure_size_height, pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                            pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size, blue_team_img, all_sprites_team)

# генерация 2 x 2 фигрур по углам поля для разных команд (синяя, зеленая)
all_sprites_blue_full_team = creature(3, 3, pos_cel_x, pos_cel_y, blue_full_team_img, all_sprites_blue_full_team)
all_sprites_green_full_team = creature(3, 3, WIDTH - pos_cel_x - 3 * cell_size, HEIGHT - pos_cel_y - 3 * cell_size,
                                       green_full_team_img, all_sprites_green_full_team)
pygame.sprite.groupcollide(all_sprites_blue_full_team, all_sprites_new_game, False, True)
pygame.sprite.groupcollide(all_sprites_green_full_team, all_sprites_new_game, False, True)

# Цикл игры
game_over = False
mine_menu = True
settings = False
new_games = False
running = True
while running:

    # Держим цикл на правильной скорости
    clock.tick(FPS)

    if mine_menu:
        # Ввод процесса (события)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:

                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2 - 50)) <= 16:
                    button_new_game.press(yellow_button_press_img, round(ratio_width * 127), round(ratio_height * 33),
                                          WIDTH / 2, HEIGHT / 2 - 50)
                    pygame.display.update()
                else:
                    button_new_game.press(yellow_button_img, round(ratio_width * 127), round(ratio_height * 33),
                                          WIDTH / 2, HEIGHT / 2 - 50)

                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2)) <= 16:
                    button_settings.press(red_button_press_img, round(ratio_width * 127), round(ratio_height * 33),
                                          WIDTH / 2, HEIGHT / 2)
                    pygame.display.update()
                else:
                    button_settings.press(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2,
                                          HEIGHT / 2)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2 - 50)) <= 16:
                    mine_menu = False
                    new_games = True
                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2)) <= 16:
                    mine_menu = False
                    settings = True

        screen_mine_menu.fill(BLACK)
        screen_mine_menu.blit(background_mine_menu_size, background_mine_menu_rect)

        all_sprites_mine_menu.draw(screen_mine_menu)
        draw_text(screen_mine_menu, "Mine Menu", round(ratio_height * 20), WHITE, WIDTH / 2, HEIGHT / 2 - 110)
        draw_text(screen_mine_menu, "New Game", round(ratio_height * 18), WHITE, WIDTH / 2, HEIGHT / 2 - 50)
        draw_text(screen_mine_menu, "Setting", round(ratio_height * 18), WHITE, WIDTH / 2, HEIGHT / 2)

    if settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:

                if abs(event.pos[0] - (WIDTH / 2 - 90)) <= 25 and abs(event.pos[1] - (HEIGHT / 2 + 140)) <= 25:
                    red_short_button.press(red_short_button_press_img, round(ratio_width * 50),
                                           round(ratio_height * 50), WIDTH / 2 - 90, HEIGHT / 2 + 140)
                    pygame.display.update()
                else:
                    red_short_button.press(red_short_button_img, round(ratio_width * 50), round(ratio_height * 50),
                                           WIDTH / 2 - 90, HEIGHT / 2 + 140)

                if abs(event.pos[0] - (WIDTH / 2 + 40)) <= 85 and abs(event.pos[1] - (HEIGHT / 2 + 140)) <= 25:
                    green_button.press(green_button_press_img, round(ratio_width * 170), round(ratio_height * 50),
                                       WIDTH / 2 + 40, HEIGHT / 2 + 140)
                    pygame.display.update()
                else:
                    green_button.press(green_button_img, round(ratio_width * 170), round(ratio_height * 50),
                                       WIDTH / 2 + 40, HEIGHT / 2 + 140)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if abs(event.pos[0] - (WIDTH / 2 + 120)) <= 9 and abs(event.pos[1] - (HEIGHT / 2 - 200)) <= 9:
                    mine_menu = True
                    settings = False

                if abs(event.pos[0] - (WIDTH / 2 + 40)) <= 85 and abs(event.pos[1] - (HEIGHT / 2 + 140)) <= 25:
                    mine_menu = True
                    settings = False

                if abs(event.pos[0] - (WIDTH / 2 - 90)) <= 25 and abs(event.pos[1] - (HEIGHT / 2 + 140)) <= 25:
                    green_checkmark.press(green_checkmark_img, round(ratio_width * 21), round(ratio_height * 20),
                                          WIDTH / 2 - 50, HEIGHT / 2 - 150)
                    pygame.display.update()
                    bot = False

                if abs(event.pos[0] - (WIDTH / 2 - 50)) <= 19 and abs(event.pos[1] - (HEIGHT / 2 - 150)) <= 18:
                    green_checkmark.press(green_checkmark_img, round(ratio_width * 21), round(ratio_height * 20),
                                          WIDTH / 2 - 50, HEIGHT / 2 - 150)
                    pygame.display.update()
                    bot = False

                if abs(event.pos[0] - (WIDTH / 2 - 50)) <= 19 and abs(event.pos[1] - (HEIGHT / 2 - 100)) <= 18:
                    green_checkmark.press(green_checkmark_img, round(ratio_width * 21), round(ratio_height * 20),
                                          WIDTH / 2 - 50, HEIGHT / 2 - 100)
                    pygame.display.update()
                    bot = True

        all_sprites_settings.draw(screen_mine_menu)

        draw_text(screen_mine_menu, "Setting", round(ratio_height * 20), WHITE, WIDTH / 2, HEIGHT / 2 - 200)
        draw_text(screen_mine_menu, "VS:", round(ratio_height * 18), BLACK, WIDTH / 2 - 100, HEIGHT / 2 - 125)
        draw_text(screen_mine_menu, "1 VS 1", round(ratio_height * 18), BLACK, WIDTH / 2 + 50, HEIGHT / 2 - 150)
        draw_text(screen_mine_menu, "1 VS BOT", round(ratio_height * 18), BLACK, WIDTH / 2 + 50, HEIGHT / 2 - 100)
        draw_text(screen_mine_menu, "VS:", round(ratio_height * 18), BLACK, WIDTH / 2 - 100, HEIGHT / 2 - 125)

    if new_games:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if (event.type == pygame.KEYDOWN) and (
            not pygame.sprite.groupcollide(all_sprites_team, all_sprites_border, False, False)):

                if event.key == pygame.K_DOWN:
                    all_sprites_team.update(pygame.K_DOWN)
                    if pygame.sprite.groupcollide(all_sprites_team, all_sprites_border, False, False):
                        all_sprites_team.update(pygame.K_UP)

                if event.key == pygame.K_UP:
                    all_sprites_team.update(pygame.K_UP)
                    if pygame.sprite.groupcollide(all_sprites_team, all_sprites_border, False, False):
                        all_sprites_team.update(pygame.K_DOWN)

                if event.key == pygame.K_LEFT:
                    all_sprites_team.update(pygame.K_LEFT)
                    if pygame.sprite.groupcollide(all_sprites_team, all_sprites_border, False, False):
                        all_sprites_team.update(pygame.K_RIGHT)

                if event.key == pygame.K_RIGHT:
                    all_sprites_team.update(pygame.K_RIGHT)
                    if pygame.sprite.groupcollide(all_sprites_team, all_sprites_border, False, False):
                        all_sprites_team.update(pygame.K_LEFT)

                if event.key == pygame.K_SPACE:

                    if motion % 2 == 1:
                        team_img = blue_team_img
                    else:
                        team_img = green_team_img

                    figure_size_width, figure_size_height = figure_size_height, figure_size_width

                    for amn in all_sprites_team:
                        figure_pos_x = amn.rect.x
                        figure_pos_y = amn.rect.y
                        break

                    pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team, True, False)
                    pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team, True, False)
                    pygame.sprite.groupcollide(all_sprites_team, all_sprites_new_game, True, False)

                    if (HEIGHT - pos_cel_y - max(figure_size_width,
                                                 figure_size_height) * cell_size >= figure_pos_y) and (
                            WIDTH - pos_cel_x - max(figure_size_width, figure_size_height) * cell_size >= figure_pos_x):
                        all_sprites_team = creature(figure_size_width, figure_size_height, figure_pos_x, figure_pos_y,
                                                    team_img, all_sprites_team)
                    else:
                        figure_size_width, figure_size_height = figure_size_height, figure_size_width
                        all_sprites_team = creature(figure_size_width, figure_size_height, figure_pos_x, figure_pos_y,
                                                    team_img, all_sprites_team)

                if event.key == pygame.K_RETURN:

                    if motion % 2 == 1:

                        if touch_groups(all_sprites_team, all_sprites_blue_full_team):
                            if (not pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team, False,
                                                               False)) and (
                            not pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team, False,
                                                           False)):
                                motion += 1
                                skip_counter = 0
                                player1_score += figure_size_width * figure_size_height

                                inherit(all_sprites_team, all_sprites_new_game, all_sprites_blue_full_team,
                                        blue_full_team_img)

                                # бот
                                if bot:
                                    while True:
                                        delay += 1
                                        bot_pos_x = pos_cel_x + random.randint(1,
                                                                               N_cell_WIDTH - figure_size_width) * cell_size
                                        bot_pos_y = pos_cel_y + random.randint(1,
                                                                               N_cell_HEIGHT - figure_size_height) * cell_size
                                        all_sprites_team = pygame.sprite.Group()
                                        all_sprites_team = creature(figure_size_width, figure_size_height, bot_pos_x,
                                                                    bot_pos_y, green_team_img, all_sprites_team)
                                        if touch_groups(all_sprites_team, all_sprites_green_full_team):
                                            if (
                                            not pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team,
                                                                           False, False)) and (
                                            not pygame.sprite.groupcollide(all_sprites_team,
                                                                           all_sprites_green_full_team, False, False)):
                                                skip_counter = 0
                                                player2_score += figure_size_width * figure_size_height
                                                inherit(all_sprites_team, all_sprites_new_game,
                                                        all_sprites_green_full_team, green_full_team_img)
                                                break
                                        if delay == 100:

                                            figure_size_width, figure_size_height = figure_size_height, figure_size_width

                                            for amn in all_sprites_team:
                                                figure_pos_x = amn.rect.x
                                                figure_pos_y = amn.rect.y
                                                break

                                            pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team,
                                                                       True, False)
                                            pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team,
                                                                       True, False)
                                            pygame.sprite.groupcollide(all_sprites_team, all_sprites_new_game, True,
                                                                       False)

                                            if (HEIGHT - pos_cel_y - max(figure_size_width,
                                                                         figure_size_height) * cell_size >= figure_pos_y) and (
                                                    WIDTH - pos_cel_x - max(figure_size_width,
                                                                            figure_size_height) * cell_size >= figure_pos_x):
                                                all_sprites_team = creature(figure_size_width, figure_size_height,
                                                                            figure_pos_x, figure_pos_y, green_team_img,
                                                                            all_sprites_team)
                                            else:
                                                figure_size_width, figure_size_height = figure_size_height, figure_size_width
                                                all_sprites_team = creature(figure_size_width, figure_size_height,
                                                                            figure_pos_x, figure_pos_y, green_team_img,
                                                                            all_sprites_team)

                                        elif delay == 200:
                                            skip_counter += 1
                                            all_sprites_team = pygame.sprite.Group()
                                            break

                                    figure_size_width = random.randint(1, 6)
                                    figure_size_height = random.randint(1, 6)
                                    all_sprites_team = creature(figure_size_width, figure_size_height,
                                                                pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                                                pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size,
                                                                blue_team_img, all_sprites_team)
                                    delay = 0
                                    motion += 1

                                else:
                                    figure_size_width = random.randint(1, 6)
                                    figure_size_height = random.randint(1, 6)
                                    all_sprites_team = creature(figure_size_width, figure_size_height,
                                                                pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                                                pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size,
                                                                green_team_img, all_sprites_team)

                    else:

                        if touch_groups(all_sprites_team, all_sprites_green_full_team):
                            if (not pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team, False,
                                                               False)) and (
                            not pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team, False,
                                                           False)):
                                motion += 1
                                skip_counter = 0
                                player2_score += figure_size_width * figure_size_height

                                inherit(all_sprites_team, all_sprites_new_game, all_sprites_green_full_team,
                                        green_full_team_img)

                                figure_size_width = random.randint(1, 6)
                                figure_size_height = random.randint(1, 6)
                                all_sprites_team = creature(figure_size_width, figure_size_height,
                                                            pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                                            pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size,
                                                            blue_team_img, all_sprites_team)

            if event.type == pygame.MOUSEMOTION:

                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2 + 320)) <= 16:
                    button_skip.press(red_button_press_img, round(ratio_width * 127), round(ratio_height * 33),
                                      WIDTH / 2, HEIGHT / 2 + 320)
                    pygame.display.update()
                else:
                    button_skip.press(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2,
                                      HEIGHT / 2 + 320)

                if abs(event.pos[0] - 80) <= 63 and abs(event.pos[1] - 80) <= 16:
                    button_surrender_player1.press(red_button_press_img, round(ratio_width * 127),
                                                   round(ratio_height * 33), 80, 80)
                    pygame.display.update()
                else:
                    button_surrender_player1.press(red_button_img, round(ratio_width * 127), round(ratio_height * 33),
                                                   80, 80)

                if abs(event.pos[0] - (WIDTH - 80)) <= 63 and abs(event.pos[1] - 80) <= 16:
                    button_surrender_player2.press(red_button_press_img, round(ratio_width * 127),
                                                   round(ratio_height * 33), WIDTH - 80, 80)
                    pygame.display.update()
                else:
                    button_surrender_player2.press(red_button_img, round(ratio_width * 127), round(ratio_height * 33),
                                                   WIDTH - 80, 80)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if abs(event.pos[0] - WIDTH / 2) <= 63 and abs(event.pos[1] - (HEIGHT / 2 + 320)) <= 16:

                    if bot:
                        motion += 1

                    if motion % 2 == 1:
                        motion += 1
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_new_game, True, False)
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team, True, False)
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team, True, False)
                        figure_size_width = random.randint(1, 6)
                        figure_size_height = random.randint(1, 6)
                        all_sprites_team = creature(figure_size_width, figure_size_height,
                                                    pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                                    pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size, green_team_img,
                                                    all_sprites_team)
                    else:
                        motion += 1
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_new_game, True, False)
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_blue_full_team, True, False)
                        pygame.sprite.groupcollide(all_sprites_team, all_sprites_green_full_team, True, False)
                        figure_size_width = random.randint(1, 6)
                        figure_size_height = random.randint(1, 6)
                        all_sprites_team = creature(figure_size_width, figure_size_height,
                                                    pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                                    pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size, blue_team_img,
                                                    all_sprites_team)
                    skip_counter += 1

                if abs(event.pos[0] - 80) <= 63 and abs(event.pos[1] - 80) <= 16:
                    player_win = 2
                    game_over = True
                    new_games = False

                if abs(event.pos[0] - (WIDTH - 80)) <= 63 and abs(event.pos[1] - 80) <= 16:
                    player_win = 1
                    game_over = True
                    new_games = False

        if (player1_score + player2_score == N_cell_WIDTH * N_cell_HEIGHT) or (skip_counter == 6):

            if player1_score > player2_score:
                player_win = 1

            elif player1_score < player2_score:
                player_win = 2

            else:
                player_win = 0

            game_over = True
            new_games = False

        # Рендеринг
        screen_new_game.fill(BLACK)
        screen_new_game.blit(background_new_game_size, background_new_game_rect)

        all_sprites_green_full_team.draw(screen_new_game)
        all_sprites_blue_full_team.draw(screen_new_game)
        all_sprites_new_game.draw(screen_new_game)
        all_sprites_team.draw(screen_new_game)

        draw_text(screen_new_game, "Skip", round(ratio_height * 18), WHITE, WIDTH / 2, HEIGHT / 2 + 320)
        draw_text(screen_new_game, "Score Player1: " + str(player1_score), round(ratio_height * 18), WHITE, 150,
                  HEIGHT - 20)
        draw_text(screen_new_game, "Score Player2: " + str(player2_score), round(ratio_height * 18), WHITE, WIDTH - 150,
                  HEIGHT - 20)
        draw_text(screen_new_game, "Player1", round(ratio_height * 18), WHITE, 80, 20)
        draw_text(screen_new_game, "Surrender", round(ratio_height * 16), WHITE, 80, 80)
        draw_text(screen_new_game, "Player2", round(ratio_height * 18), WHITE, WIDTH - 80, 20)
        draw_text(screen_new_game, "Surrender", round(ratio_height * 16), WHITE, WIDTH - 80, 80)

    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:

                if abs(event.pos[0] - 300) <= 127 and abs(event.pos[1] - HEIGHT / 2) <= 33:
                    button_game_over_new_game.press(yellow_button_press_img, round(ratio_width * 254),
                                                    round(ratio_height * 66), 300, HEIGHT / 2)
                    pygame.display.update()
                else:
                    button_game_over_new_game.press(yellow_button_img, round(ratio_width * 254),
                                                    round(ratio_height * 66), 300, HEIGHT / 2)

                if abs(event.pos[0] - (WIDTH - 300)) <= 127 and abs(event.pos[1] - HEIGHT / 2) <= 33:
                    button_game_over_mine_menu.press(yellow_button_press_img, round(ratio_width * 254),
                                                     round(ratio_height * 66), WIDTH - 300, HEIGHT / 2)
                    pygame.display.update()
                else:
                    button_game_over_mine_menu.press(yellow_button_img, round(ratio_width * 254),
                                                     round(ratio_height * 66), WIDTH - 300, HEIGHT / 2)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if abs(event.pos[0] - 300) <= 127 and abs(event.pos[1] - HEIGHT / 2) <= 33:
                    game_over = False
                    new_games = True

                if abs(event.pos[0] - (WIDTH - 300)) <= 127 and abs(event.pos[1] - HEIGHT / 2) <= 33:
                    game_over = False
                    mine_menu = True

        if player_win != -1:
            if player_win == 0:
                text = "Nobody"
            elif player_win == 1:
                text = "Player1 WIN"
            elif player_win == 2:
                text = "Player2 WIN"

            # генерация клетчетого поля
            all_sprites_new_game = pygame.sprite.Group()
            all_sprites_new_game = creature(N_cell_WIDTH, N_cell_HEIGHT, pos_cel_x, pos_cel_y, cell_img,
                                            all_sprites_new_game)

            # Спрайты для КНОПОК новой игры
            button_skip = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH / 2,
                                 HEIGHT / 2 + 320)
            all_sprites_new_game.add(button_skip)
            button_surrender_player1 = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33), 80,
                                              80)
            all_sprites_new_game.add(button_surrender_player1)
            button_surrender_player2 = Button(red_button_img, round(ratio_width * 127), round(ratio_height * 33),
                                              WIDTH - 80, 80)
            all_sprites_new_game.add(button_surrender_player2)
            all_sprites_new_game.add(
                Button(blue_button_img, round(ratio_width * 127), round(ratio_height * 33), 80, 20))
            all_sprites_new_game.add(
                Button(green_button_img, round(ratio_width * 127), round(ratio_height * 33), WIDTH - 80, 20))

            # генерация первого шаблона
            all_sprites_team = pygame.sprite.Group()
            figure_size_width = random.randint(1, 6)
            figure_size_height = random.randint(1, 6)
            all_sprites_team = creature(figure_size_width, figure_size_height,
                                        pos_cel_x + round(N_cell_WIDTH / 2) * cell_size,
                                        pos_cel_y + round(N_cell_HEIGHT / 2) * cell_size, blue_team_img,
                                        all_sprites_team)

            # генерация 2 x 2 фигрур по углам поля для разных команд (синяя, зеленая)
            all_sprites_blue_full_team = pygame.sprite.Group()
            all_sprites_green_full_team = pygame.sprite.Group()
            all_sprites_blue_full_team = creature(3, 3, pos_cel_x, pos_cel_y, blue_full_team_img,
                                                  all_sprites_blue_full_team)
            all_sprites_green_full_team = creature(3, 3, WIDTH - pos_cel_x - 3 * cell_size,
                                                   HEIGHT - pos_cel_y - 3 * cell_size, green_full_team_img,
                                                   all_sprites_green_full_team)
            pygame.sprite.groupcollide(all_sprites_blue_full_team, all_sprites_new_game, False, True)
            pygame.sprite.groupcollide(all_sprites_green_full_team, all_sprites_new_game, False, True)

            # счетчик очереди
            motion = 1

            # счетчик пропусков
            skip_counter = 0

            # игровые очки
            player1_score = 9
            player2_score = 9

        all_sprites_game_over.draw(screen_new_game)

        draw_text(screen_new_game, text, round(ratio_height * 36), BLUE, WIDTH / 2 + 5, HEIGHT / 2 + 5)
        draw_text(screen_new_game, text, round(ratio_height * 36), AQUA, WIDTH / 2 + 3, HEIGHT / 2 + 3)
        draw_text(screen_new_game, text, round(ratio_height * 36), LightGrey, WIDTH / 2, HEIGHT / 2)

        draw_text(screen_new_game, "New Game", round(ratio_height * 20), WHITE, 300, HEIGHT / 2)
        draw_text(screen_new_game, "Mine Menu", round(ratio_height * 20), WHITE, WIDTH - 300, HEIGHT / 2)

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()