import pygame, os


def _color_(hex_color):
    hex_color = hex_color[1:]

    if (len(hex_color) != 3):
        hex_color = "000"

    full_hex_color = "#"

    for ch in hex_color:
        full_hex_color += ch + ch

    return pygame.Color(full_hex_color)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image

def load_level(filename):
    filename = os.path.join('data', 'levels', filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


pygame.init()
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(_color_("#fff"))
FPS = 50
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 200)



tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = pygame.transform.scale(load_image('blue1.png'), (40, 40));

tile_width = tile_height = 50

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 5, tile_height * pos_y + 5)

    def move_right(self):
        if self.rect.x + tile_width <= WIDTH:
            self.rect.x += tile_width

    def move_left(self):
        if self.rect.x - tile_width >= 0:
            self.rect.x -= tile_width

    def move_down(self):
        if self.rect.y + tile_width <= HEIGHT:
            self.rect.y += tile_width

    def move_up(self):
        if self.rect.y - tile_width >= 0:
            self.rect.y -= tile_width


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)         
    return new_player, x, y



def terminate():
    pygame.quit()
    exit(0)

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def draw(player):
    screen.fill(_color_("#fff"))


#start_screen()

player, level_x, level_y = generate_level(load_level('1.txt'))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #player.move_right()
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == 276: # <- left
                player.move_left()
                print("left")
            if event.key == 274: # V  down
                player.move_down()
                print("down")
            if event.key == 275: # -> right
                player.move_right()
                print("right")
            if event.key == 273: # A  up
                player.move_up()
                print("up")

    tiles_group.draw(screen)
    player_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
