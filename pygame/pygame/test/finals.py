import pygame

pygame.init()

# Map 1
map1 = [
    "################################",
    "#..............................#",
    "#..#...........................#",
    "#......##...##......##.........#",
    "#...............##......##.....#",
    "#...........................##.#",
    "#.......................##.....#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "################################"
]

# Map 2
map2 = [
    "################################",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "################################"
]

# Map 3
map3 = [
    "################################",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "#..............................#",
    "################################"
]

maps = [None, map1, map2, map3]
current_level = 1
current_map = maps[current_level]
screen_width = len(map1[0]) * 32
screen_height = len(map1) * 32

# Colors
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)

# Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pixel Path")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Groups
player_group = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
doors = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.image = pygame.Surface((32 * scale, 32 * scale))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velX = 5
        self.velY = 0
        self.jumping = False
        self.gravity = 0.5

    def update(self):
        global current_level, is_running
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velX
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velX
        if not self.jumping:
            if keys[pygame.K_UP]:
                self.jumping = True
                self.velY = -10

        self.velY += self.gravity
        self.rect.y += self.velY

        # Simple ground collision
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velY = 0
            self.jumping = False

        # Level finish check
        if self.rect.right >= screen_width:
            current_level += 1
            if current_level > len(maps) - 1:
                is_running = False
            else:
                load_level(current_level, self)
                self.rect.x = 32
                self.rect.y = screen_height - 64

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def load_level(level, player=None):
    global current_map
    current_map = maps[level]
    obstacles.empty()
    doors.empty()
    player_group.empty()

    current_player = player
    for y, row in enumerate(current_map):
        for x, char in enumerate(row):
            pos_x = x * 32
            pos_y = y * 32
            if char == "#":
                obstacles.add(Obstacle(pos_x, pos_y, 32, 32))
            elif char == "P":
                current_player = Player(pos_x, pos_y, 1)
                player_group.add(current_player)
            elif char == "D":
                doors.add(Door(pos_x, pos_y, 32, 32))

    if current_player is None:
        current_player = Player(32, screen_height - 64, 1)
        player_group.add(current_player)

    return current_player

player_sprite = load_level(current_level)
# Main loop
is_running = True
while is_running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    player_group.update()

    screen.fill(BROWN)

    # Draw level text
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    screen.blit(level_text, (10, 10))

    player_group.draw(screen)
    obstacles.draw(screen)
    doors.draw(screen)

    pygame.display.flip()
pygame.quit()