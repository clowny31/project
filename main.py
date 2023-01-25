import pygame.sprite
import os
import pygame.sprite
import os
import sys

pygame.init()
screen_size = width, height = 340, 340
screen = pygame.display.set_mode(screen_size)
FPS = 70


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(hero_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 15000, 15000)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = mario1_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        if event.key == pygame.K_UP:
            self.image = mario2_image
        if event.key == pygame.K_DOWN:
            self.image = mario1_image
        if event.key == pygame.K_LEFT:
            self.image = mario4_image
        if event.key == pygame.K_RIGHT:
            self.image = mario3_image
        camera.dx -= tile_width * (x - self.pos[0])
        camera.dy -= tile_height * (y - self.pos[1])
        self.pos = (x, y)
        for sprite in sprite_group:
            camera.apply(sprite)
        for sprite in end_group:
            camera.apply(sprite)


    def position(self):
        return self.pos


class Ending(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(end_group)
        self.image = end_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)

    def position(self):
        return self.pos


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x = obj.abs_pos[0] + self.dx
        obj.rect.y = obj.abs_pos[1] + self.dy

    def update(self, target):
        self.dx = 0
        self.dy = 0


tile_images = {
    'wall': load_image('box1.png'),
    'empty': load_image('grass.png'),
    'stena': load_image('stena.png'),
    'floor': load_image('pol.png'),
    'sand': load_image('pesok.png'),
    'wall_of_sand': load_image('kam_pesok.png')
}
mario1_image = load_image('mario1.png')
mario2_image = load_image('mario2.png')
mario3_image = load_image('mario3.png')
mario4_image = load_image('mario4.png')
end_image = load_image('star.png')

tile_width = tile_height = 50


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
end_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit

def end_screen():
    intro_text = ["Спасибо за игру",
                  "Нажмите Space, чтобы начать"]

    fon = pygame.transform.scale(load_image('fon2.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["Удачной игры",
                  "Веселитесь"]

    fon = pygame.transform.scale(load_image('fon.png'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                level[y][x] = "."
                end = Ending(x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                level[y][x] = "."
            elif level[y][x] == '%':
                Tile('stena', x, y)
            elif level[y][x] == ',':
                Tile('floor', x, y)
            elif level[y][x] == '&':
                Tile('floor', x, y)
                new_player = Player(x, y)
                level[y][x] = ","
            elif level[y][x] == '1':
                Tile('floor', x, y)
                level[y][x] = ","
                end = Ending(x, y)
            elif level[y][x] == '$':
                Tile('sand', x, y)
                new_player = Player(x, y)
                level[y][x] = "-"
            elif level[y][x] == '-':
                Tile('sand', x, y)
            elif level[y][x] == '<':
                Tile('wall_of_sand', x, y)
            elif level[y][x] == '+':
                Tile('sand', x, y)
                level[y][x] = "-"
                end = Ending(x, y)
    return end, new_player, x, y


def kill_Sprite_Group(sprite_group):
    for i in sprite_group:
        i.kill()


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0 and level_map1[y - 1][x] == "." or level_map1[y - 1][x] == "," or level_map1[y - 1][x] == "-":
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and level_map1[y + 1][x] == "." or level_map1[y + 1][x] == "," or level_map1[y + 1][x] == "-":
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and level_map1[y][x - 1] == "." or level_map1[y][x - 1] == "," or level_map1[y][x - 1] == "-":
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and level_map1[y][x + 1] == "." or level_map1[y][x + 1] == "," or level_map1[y][x + 1] == "-":
            hero.move(x + 1, y)
    return x, y


start_screen()
count = 0
level_map1 = load_level('m1.map')
ending, hero, max_x, max_y = generate_level(level_map1)
x_star, y_star = ending.position()
camera = Camera()
camera.update(hero)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
                x_hero, y_hero = hero.position()
                if x_hero == x_star and y_star == y_hero:
                    if count == 0:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m2.map')
                        image = load_image("dark.png")
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 1:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m3.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 2:
                        running = False
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
                Player.image = mario1_image
                x_hero, y_hero = hero.position()
                if x_hero == x_star and y_star == y_hero:
                    if count == 0:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m2.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 1:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m3.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 2:
                        running = False
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
                x_hero, y_hero = hero.position()
                if x_hero == x_star and y_star == y_hero:
                    if count == 0:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m2.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 1:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m3.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 2:
                        running = False
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")
                x_hero, y_hero = hero.position()
                if x_hero == x_star and y_star == y_hero:
                    if count == 0:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m2.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 1:
                        kill_Sprite_Group(hero_group)
                        kill_Sprite_Group(sprite_group)
                        kill_Sprite_Group(end_group)
                        start_screen()
                        level_map1 = []
                        level_map1 = load_level('m3.map')
                        camera.update(hero)
                        ending, hero, max_x, max_y = generate_level(level_map1)
                        x_star, y_star = ending.position()
                        count += 1
                        pygame.display.flip()
                    elif count == 2:
                        running = False
    screen.fill(pygame.Color("black"))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    end_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
end_screen()
pygame.quit()
