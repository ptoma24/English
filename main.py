import pygame
from random import randrange
import os
import sys
from random import sample
import sqlite3

# import gtts
# from pydub import AudioSegment

pygame.init()
pygame.display.set_caption('Учим английский алфавит')
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HIGHT = 600, 600
screen = pygame.display.set_mode(WINDOW_SIZE)
FPS = 15
MAPS_DIR = "maps"
TILE_SIZE = 30
list_x = []
list_y = []


# def load_music(word):
#     t1 = gtts.gTTS(word)
#     t1.save(word + ".mp3")
#     mp3_file_name = word + ".mp3"
# ogg_file_name = "data/" + word + ".ogg"  # oGG file name
# AudioSegment.from_mp3(mp3_file_name).export(ogg_file_name, format='ogg')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.i = 0

    def update(self):
        r = TILE_SIZE // 2
        x0 = 300
        y0 = 300
        if self.i == 0:
            pygame.draw.circle(screen, "#32CD32", (x0 + 2 * r, y0), r)
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 - r, y0 - r * (3 ** 0.5)), r)
        elif self.i == 1:
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#32CD32", (x0 - r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 - 2 * r, y0), r)
        elif self.i == 2:
            pygame.draw.circle(screen, "#32CD32", (x0 - r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#32CD32", (x0 - 2 * r, y0), r)
            pygame.draw.circle(screen, "#006400", (x0 - r, y0 + r * (3 ** 0.5)), r)
        elif self.i == 3:
            pygame.draw.circle(screen, "#32CD32", (x0 - 2 * r, y0), r)
            pygame.draw.circle(screen, "#32CD32", (x0 - r, y0 + r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 + r, y0 + r * (3 ** 0.5)), r)
        elif self.i == 4:
            pygame.draw.circle(screen, "#32CD32", (x0 - r, y0 + r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 + r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 + 2 * r, y0), r)
        elif self.i == 5:
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 + r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#32CD32", (x0 + 2 * r, y0), r)
            pygame.draw.circle(screen, "#006400", (x0 + r, y0 - r * (3 ** 0.5)), r)
        elif self.i == 6:
            pygame.draw.circle(screen, "#32CD32", (x0 + 2 * r, y0), r)
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 - r, y0 - r * (3 ** 0.5)), r)
        elif self.i == 7:
            pygame.draw.circle(screen, "#32CD32", (x0 + r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#32CD32", (x0 - r, y0 - r * (3 ** 0.5)), r)
            pygame.draw.circle(screen, "#006400", (x0 - 3 * r, y0 - r * (3 ** 0.5)), r)
            return True
        self.i += 1


def end_level(word, k, type_game):
    r = TILE_SIZE // 2
    x0 = 300
    y0 = 300
    ani = AnimatedSprite()
    running = True
    clock = pygame.time.Clock()
    t = False
    t2 = False
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main()
        if not t:
            t = ani.update()
        else:
            if not t2:
                # load_music(word)
                file = "data/" + word + ".ogg"
                s = pygame.mixer.Sound(file)
                s.play()
                # playsound(file)
                t2 = True
            con = sqlite3.connect("english.sqlite")
            cur = con.cursor()
            # print("type game")
            # print(type_game)
            # print(type_game, word.lower())
            result = cur.execute("""SELECT sum FROM games where type in(SELECT id FROM type_games 
            WHERE type = ?) and word in(SELECT id FROM words WHERE word = ?)""", (type_game, word.lower())).fetchall()
            (ans,) = result[0]
            if k <= ans:
                font = pygame.font.Font(None, 20)
                pygame.draw.rect(screen, (0, 0, 0), (20, 20, 440, 40))
                line = "Ваш результат " + str(k) + " Ваш рекорд " + str(ans)
                text = font.render(line, True, [255, 255, 255])
                textpos = 20, 20
                screen.blit(text, textpos)
            else:
                cur.execute("""UPDATE games SET sum = ? where type in(SELECT id FROM type_games 
                                            WHERE type = ?) and word in(SELECT id FROM words WHERE word = ?)""",
                            (k, type_game, word))
                font = pygame.font.Font(None, 20)
                pygame.draw.rect(screen, (0, 0, 0), (20, 20, 440, 40))
                line = "Ваш новый рекорд " + str(k)
                text = font.render(line, True, [255, 255, 255])
                textpos = 20, 20
                screen.blit(text, textpos)
            con.commit()
            con.close()

            center1 = (x0 + r, y0 - r * (3 ** 0.5))
            pygame.draw.circle(screen, "#32CD32", center1, r)
            text = font.render(word[2], True, [255, 255, 255])
            textpos = center1[0] - 5, center1[1] - 5
            screen.blit(text, textpos)

            center2 = (x0 - r, y0 - r * (3 ** 0.5))
            pygame.draw.circle(screen, "#32CD32", center2, r)
            text = font.render(word[1], True, [255, 255, 255])
            textpos = center2[0] - 5, center2[1] - 5
            screen.blit(text, textpos)

            center3 = (x0 - 3 * r, y0 - r * (3 ** 0.5))
            pygame.draw.circle(screen, "#006400", center3, r)
            text = font.render(word[0], True, [255, 255, 255])
            textpos = center3[0] - 5, center3[1] - 5
            screen.blit(text, textpos)

        pygame.display.flip()
        clock.tick(2)


def end_level_wrong(word, wrong):
    fon = pygame.transform.scale(load_image('english.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    line = "Неверно, " + "'" + wrong + "'" + ". Правильно " + word
    string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 10
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                main()
            # if event.type == pygame.KEYDOWN or \
            #         event.type == pygame.MOUSEBUTTONDOWN:
            #     return
        pygame.display.flip()


class Labyrinth:

    def __init__(self, filename, free_tiles, finish_tile, trashcan, task):
        self.map = []
        with open(f"{MAPS_DIR}/{filename}") as input_file:
            for line in input_file:
                self.map.append(list(map(int, line.split())))
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.tile_size = TILE_SIZE
        self.free_tiles = free_tiles
        self.finish_tiles = finish_tile
        self.trashcan = int(trashcan)
        self.task = task
        self.k = 10

    def render(self, screen):
        colors = {0: (0, 0, 0), 1: (120, 120, 120), 2: (50, 50, 50), 3: (255, 0, 0)}
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size,
                                   self.tile_size, self.tile_size)
                screen.fill(colors[self.get_tile_id((x, y))], rect)
        font = pygame.font.Font(None, 30)
        text_coord = 4
        string_rendered = font.render(self.task, 1, pygame.Color(255, 255, 255))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    def get_tile_id(self, position):
        return self.map[position[1]][position[0]]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles

    def is_trashcan(self, position):
        return self.get_tile_id(position) == self.trashcan, self.k


class Hero(pygame.sprite.Sprite):

    def __init__(self, position, len, word, type_game):
        super().__init__(sprite_hero)
        self.type_game = type_game
        self.word = word
        self.word_now = ""
        self.len = len
        self.x = []
        self.y = []
        for i in range(len):
            self.x.append(position[0] - i)
            self.y.append(position[1])
        self.rect = pygame.Rect(self.x[0] * TILE_SIZE, self.y[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.i = 0
        self.character = [""] * len
        self.k = 10

    def set_character(self, character):
        if self.i > len(self.character) - 1:
            self.k -= 1
            Сharacter(character, labyrinth)
        else:
            self.word_now += character
            self.character[self.i] = character
            self.i += 1
        # load_music(word)
        file = "data/" + character + ".ogg"
        s = pygame.mixer.Sound(file)
        s.play()
        # playsound(file)

    def get_position(self):
        return self.x[0], self.y[0]

    def set_position(self, position):
        for i in range(self.len - 1, -1, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        self.x[0], self.y[0] = position
        self.rect = pygame.Rect(self.x[0] * TILE_SIZE, self.y[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if self.x[0] == 0 and self.y[0] == 1:
            # print(self.word_now)
            if self.word == self.word_now:
                # print(self.k)
                # load_music(word)
                file = "data/" + self.word + ".ogg"
                s = pygame.mixer.Sound(file)
                s.play()
                end_level(self.word, self.k, self.type_game)

            else:
                end_level_wrong(self.word, self.word_now)
                # print("Неверно")

    def render(self, screen):
        for i in range(self.len):
            center1 = self.x[i] * TILE_SIZE + TILE_SIZE // 2, self.y[i] * TILE_SIZE + TILE_SIZE // 2
            if i == 0:
                pygame.draw.circle(screen, "#006400", center1, TILE_SIZE // 2)
            else:
                pygame.draw.circle(screen, "#32CD32", center1, TILE_SIZE // 2)
            font = pygame.font.Font(None, 20)
            text = font.render(self.character[i], True, [255, 255, 255])
            textpos = center1[0] - 5, center1[1] - 5
            screen.blit(text, textpos)

    def del_character(self, k):
        self.k = k
        if self.word_now != "":
            self.word_now = self.word_now[:-1]
            self.i -= 1
            character = self.character[len(self.word_now)]
            self.character[len(self.word_now)] = ""
            Сharacter(character, labyrinth)


class Сharacter(pygame.sprite.Sprite):
    def __init__(self, character, labyrinth):
        super().__init__(letter)
        self.character = character
        self.labyrinth = labyrinth
        while True:
            self.x = randrange(15)
            self.y = randrange(15)
            if self.labyrinth.is_free((self.x, self.y)) and not (self.x in list_x) and not (self.y in list_y):
                list_x.append(self.x)
                list_y.append(self.y)
                break
        self.rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def update(self, screen, sprite_hero, hero):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (0, 0, 255), center, TILE_SIZE // 2)
        font = pygame.font.Font(None, 20)
        text = font.render(self.character, True, [255, 255, 255])
        textpos = center[0] - 5, center[1] - 5
        screen.blit(text, textpos)
        let = pygame.sprite.spritecollide(hero, letter, True)
        for s in let:
            text = s.character
            hero.set_character(text)


class Game:
    def __init__(self, labyrinth, hero, letter):
        self.labyrinth = labyrinth
        self.hero = hero
        self.letter = letter
        self.k = 10

    def render(self, screen):
        self.labyrinth.render(screen)
        self.letter.update(screen, sprite_hero, self.hero)
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
            if self.labyrinth.is_free((next_x, next_y)):
                self.hero.set_position((next_x, next_y))
            a = self.labyrinth.is_trashcan((next_x, next_y))
            if a[0]:
                self.k -= 1
                # self.k = a[1]
                self.hero.del_character(self.k)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
            if self.labyrinth.is_free((next_x, next_y)):
                self.hero.set_position((next_x, next_y))
            a = self.labyrinth.is_trashcan((next_x, next_y))
            if a[0]:
                self.k -= 1
                self.hero.del_character(self.k)
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
            if self.labyrinth.is_free((next_x, next_y)):
                self.hero.set_position((next_x, next_y))
            a = self.labyrinth.is_trashcan((next_x, next_y))
            if a[0]:
                self.k -= 1
                self.hero.del_character(self.k)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
            if self.labyrinth.is_free((next_x, next_y)):
                self.hero.set_position((next_x, next_y))
            a = self.labyrinth.is_trashcan((next_x, next_y))
            if a[0]:
                self.k = a[1]
                self.hero.del_character(self.k)


def terminate():
    pygame.quit()
    sys.exit()


def choice():
    intro_text = [
        "Нажми a или e"]
    fon = pygame.transform.scale(load_image('choice.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 40)
    text_coord = 250
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return "a"
                if event.key == pygame.K_e:
                    return "e"
        pygame.display.flip()


def type(level):
    if level == "a":
        intro_text = [
            "Нажми цифру:", "1 - учить слова с буквой a",
            "2 - учить заглавные буквы", "3 - учить строчные буквы"]
        fon = pygame.transform.scale(load_image('a.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    else:
        intro_text = [
            "Нажми цифру:", "1 - учить слова с буквой e",
            "2 - учить заглавные буквы", "3 - учить строчные буквы"]
        fon = pygame.transform.scale(load_image('e.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 40)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 70
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3
        pygame.display.flip()


def end():
    fon = pygame.transform.scale(load_image('english.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont("arial", 30)
    text_coord = 150
    line = "Приходи ещё играть"
    string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 150
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    return "a"
                if event.key == pygame.K_e:
                    return "e"
        pygame.display.flip()


def main():
    level = choice()
    types = type(level)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    words = []
    if level == "a":
        # print(words)
        words = sample(list_a, 2)
        # print(words)
        if types == 1:
            task = "Собери по-английски слово " + dict_a[words[0]]
            type_game = "english"
        elif types == 2:
            task = "Собери большими буквами слово " + words[0]
            type_game = "upper"
            for i in range(len(words)):
                words[i] = words[i].upper()
        else:
            task = "Собери маленьким буквами слово " + words[0].upper()
            type_game = "lower"
        labyrinth = Labyrinth("simple_map_a.txt", [0, 2], 2, 3, task)
        word = words[0]
    if level == "e":
        # print(words)
        words = sample(list_e, 2)
        # print(words)
        if types == 1:
            task = "Собери по-английски слово " + dict_e[words[0]]
            type_game = "english"
        elif types == 2:
            task = "Собери большими буквами слово " + words[0]
            type_game = "upper"
            for i in range(len(words)):
                words[i] = words[i].upper()
        else:
            type_game = "lower"
            task = "Собери маленьким буквами слово " + words[0].upper()
        labyrinth = Labyrinth("simple_map_e.txt", [0, 2], 2, 3, task)
        word = words[0]
    x = 3
    y = 1
    list_x.append(x)
    list_y.append(y)
    hero = Hero((x, y), 3, word, type_game)
    for j in words:
        for i in j:
            character = i
            Сharacter(character, labyrinth)
    game = Game(labyrinth, hero, letter)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.update_hero()
        screen.fill((0, 0, 0))
        game.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    end()
    pygame.quit()


def start_screen():
    intro_text = ["Давай играть!", "Нажми любую клавишу"]
    fon = pygame.transform.scale(load_image('abc.png'), (WINDOW_WIDTH, WINDOW_HIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('arial', 40)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 120
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    task = ""
    sprite_hero = pygame.sprite.Group()
    letter = pygame.sprite.Group()
    dict_a = {"cat": "кот", "hat": "шляпа", "ant": "муравей", "map": "карта"}
    dict_e = {"ten": "10", "net": "сеть", "pet": "питомец", "pen": "ручка"}
    list_a = ["cat", "hat", "ant", "map"]
    list_e = ["ten", "net", "pet", "pen"]
    labyrinth = Labyrinth("simple_map_a.txt", [0, 2], 2, 3, task)
    start_screen()
    main()