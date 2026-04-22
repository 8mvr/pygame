import os
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

# ==================== MAPS ====================
MAP_1 = [
    "....................",
    "....................",
    "..D.................",
    "..##................",
    "....................",
    "....................",
    "....................",
    "...........V........",
    "....................",
    "...........S........",
    "....................",
    "....................",
    "....................",
    "##########.........."
]

TILE_SIZE = 48
SCREEN_WIDTH = len(MAP_1[0]) * TILE_SIZE
SCREEN_HEIGHT = len(MAP_1) * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pathfinder")

# Colors
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)

# Custom color
CUSTOM_1 = ("#663300")
CUSTOM_2 = ("#C6C6C6")
CUSTOM_3 = ("#00550A")

FPS = 60
PLAYER_VEL = 5

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# load all image from the assets
def load_sprite_sheet(dir1, dir2, width, height, direction = False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            #size of the character
            sprites.append(pygame.transform.scale(surface, (192, 192)))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

obstacles = pygame.sprite.Group()
spikes = pygame.sprite.Group()
doors = pygame.sprite.Group()

# ==================== PLAYER ====================
class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    # access the character and the size of sprite
    SPRITES = load_sprite_sheet("MainCharacter", "MaleHero", 128, 128, True)
    anim_delay = 5 # speed of the animation

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.velX = 0
        self.velY = 0
        self.mask = None
        self.direction = "left"
        self.anim_count = 0
        self.fall_count = 0

     # moving
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    # image flipping
    def move_left(self, vel):
        self.velX = -vel
        if self.direction != "left":
            self.direction = "left"
            self.anim_count = 0
    
    # default image facing
    def move_right(self, vel):
        self.velX = vel
        if self.direction != "right":
            self.direction = "right"
            self.anim_count = 0

    def move_loop(self, fps):
        # gravity
        self.velY += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.velX, self.velY)

        # left border
        if self.rect.left < -64:
            self.rect.left = -64
        # right border
        if self.rect.right > SCREEN_WIDTH - 64:
            self.rect.right = SCREEN_WIDTH - 64

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - 60

        self.fall_count += 1
        self.update_sprite()

    # update sprite every frame
    def update_sprite(self):
        # no movement
        sprite_sheet = "idle"
        if self.velX != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
                                    # every 5 frames show different sprites
        sprite_index = (self.anim_count // self.anim_delay) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.anim_count += 1
        self.update()

    # draw updated sprite on the screen
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

# ==================== OBSTACLE ====================
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(CUSTOM_3)
        self.rect = self.image.get_rect(topleft=(x, y))

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        if flipped:
            # triangle pointing down
            points = [
                (0, 0),                     # top left
                (TILE_SIZE, 0),             # top right
                (TILE_SIZE // 2, TILE_SIZE) # bottom mid
            ]
        else:
            # triangle pointing up
            points = [
                (0, TILE_SIZE),        # bottom left
                (TILE_SIZE // 2, 0),   # top mid
                (TILE_SIZE, TILE_SIZE) # bottom right
            ]
        
        pygame.draw.polygon(self.image, CUSTOM_2, points)
        self.mask = pygame.mask.from_surface(self.image)

class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

# ==================== MAP OBSTACLES ====================
for y, row in enumerate(MAP_1):
    for x, char in enumerate(row):
        pos_x = x * TILE_SIZE
        pos_y = y * TILE_SIZE
        
        # blocks
        if char == "#":
            obstacles.add(Obstacle(pos_x, pos_y))
        # arrow up spike
        elif char == "S":
            spikes.add(Spike(pos_x, pos_y, flipped=False))
        # arrow down spike
        elif char == "V":
            spikes.add(Spike(pos_x, pos_y, flipped=True))
        # door
        elif char == "D":
            doors.add(Door(pos_x, pos_y))

# ==================== BACKGROUND ====================
def get_background(name):
    # joining
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    # loop tiles of the screen || add 1 for gap
    for a in range(SCREEN_WIDTH // width + 1):
        for b in range(SCREEN_HEIGHT // height + 1):
            pos = (a * width, b * height)
            tiles.append(pos)

    return tiles, image

# ==================== DRAW ====================
def draw(screen, player, background, bg_image): # background, bg_image
    # background draw
    for tile in background:
        screen.blit(bg_image, tile)
    # screen.fill(CUSTOM_1)

    #player draw
    player.draw(screen)
    obstacles.draw(screen)
    spikes.draw(screen)
    doors.draw(screen)

    pygame.display.update()

# ==================== PLAYER MOVEMENT ====================
def movement(player):
    keys = pygame.key.get_pressed()

    player.velX = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

# ==================== MAIN ====================
def main(screen):
    clock = pygame.time.Clock()

    # background
    background, bg_image = get_background("Brown.png")

    # player
    player = Player(200, 100, 64, 64)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.move_loop(FPS)
        movement(player)
        draw(screen, player, background, bg_image) # background, bg_image
        
    pygame.quit()

if __name__ == '__main__':
    main(screen)
