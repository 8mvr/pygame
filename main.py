import pygame, os
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

MAP_2 = [
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "...........S........",
    "....................",
    "....................",
    "....................",
    "#..................."
]

MAP_3 = [
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
    "...........S........",
    "....................",
    "....................",
    "....................",
    "#..................."
]

TILE_SIZE = 48
SCREEN_WIDTH = len(MAP_1[0]) * TILE_SIZE
SCREEN_HEIGHT = len(MAP_1) * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

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

# ==================== BLOCK ====================
# def get_block(size):
#     path = join("assets", "Terrain", "Terrain.png")
#     image = pygame.image.load(path).convert_alpha()
#     surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
#     rect = pygame.Rect(96, 64, size, size)
#     surface.blit(image, (0, 0), rect)

#     return surface

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
        # self.velY += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.velX, self.velY)

        self.fall_count += 1
        self.update_sprite()

    # top of the block
    def landed(self):
        self.fall_count = 0
        self.velY = 0
        self.jump_count = 0

    # bottom of the block
    def hit_head(self):
        self.count = 0
        self.velY *= -1

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

    # def update(self):
    #     self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
    #     self.mask = pygame.mask.from_surface(self.sprite) # mapping all pixels that exist in sprite

    # draw updated sprite on the screen
    def draw(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

# ========== OBSTACLE ==========
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(CUSTOM_3)
        self.rect = self.image.get_rect(topleft=(x, y))

# ========== SPIKE ==========
# class Spike(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#         super().__init__()
#         self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
#         self.image.fill(GRAY)
#         self.rect = self.image.get_rect(topleft=(x, y))
# class Spike(pygame.sprite.Sprite):
#     def __init__(self, x, y):
#             super().__init__()
#             self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
#             self.rect = self.image.get_rect(topleft=(x, y))
            
#             # spike arrow up
#             points = [
#                 (0, TILE_SIZE),
#                 (TILE_SIZE // 2, 0),
#                 (TILE_SIZE, TILE_SIZE)
#             ]
            
#             # Draw the triangle onto the internal image surface
#             pygame.draw.polygon(self.image, CUSTOM_2, points)
            
#             # Create a mask for pixel-perfect collision later
#             self.mask = pygame.mask.from_surface(self.image)

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        if flipped:
            # Points for Upside Down (Triangle pointing DOWN)
            points = [
                (0, 0),                       # Top Left
                (TILE_SIZE, 0),              # Top Right
                (TILE_SIZE // 2, TILE_SIZE)   # Bottom Middle
            ]
        else:
            # Points for Normal (Triangle pointing UP)
            points = [
                (0, TILE_SIZE),               # Bottom Left
                (TILE_SIZE // 2, 0),          # Top Middle
                (TILE_SIZE, TILE_SIZE)        # Bottom Right
            ]
        
        pygame.draw.polygon(self.image, CUSTOM_2, points)
        self.mask = pygame.mask.from_surface(self.image)

# ========== FINISH ==========
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

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

# ==================== OBJECTS ====================
# class Object(pygame.sprite.Sprite):
#     def __init__(self, x, y, width, height, name=None):
#         super().__init__()
#         self.rect = pygame.Rect(x, y, width, height) # rectangle
#         self.image = pygame.Surface((width, height), pygame.SRCALPHA) # image || support transparent images
#         self.width = width
#         self.height = height
#         self.name = name

#     # draw the block image
#     def draw(self, screen):
#         screen.blit(self.image, (self.rect.x, self.rect.y))

# class Block(Object):
#     def __init__(self, x, y, size):
#         super().__init__(x, y, size, size)
#         block = get_block(size) # get the image
#         self.image.blit(block, (0, 0))
#         self.mask = pygame.mask.from_surface(self.image)
# ==================== PLATFORMS ====================


# ==================== BACKGROUND ====================
# def get_background(name):
#     # joining
#     image = pygame.image.load(join("assets", "Background", name))
#     _, _, width, height = image.get_rect()
#     tiles = []

#     # loop tiles of the screen || add 1 for gap
#     for a in range(SCREEN_WIDTH // width + 1):
#         for b in range(SCREEN_HEIGHT // height + 1):
#             pos = (a * width, b * height)
#             tiles.append(pos)

#     return tiles, image

# ==================== DRAW ====================
def draw(screen, player):
    # background draw
    # for tile in background:
    #     screen.blit(bg_image, tile)
    screen.fill(CUSTOM_1)

    # for obj in objects:
    #     obj.draw(screen)

    #player draw
    player.draw(screen)
    obstacles.draw(screen)
    spikes.draw(screen)
    doors.draw(screen)

    pygame.display.update()

# ========== COLLISION ==========
# def vertical_collision(player, objects, dy):
#     collided_objects = []
#     for obj in objects:
#         if pygame.sprite.collide_mask(player, obj):
#             # player or top of block
#             if dy > 0:
#                 player.rect.bottom = obj.rect.top
#                 player.landed()
#             elif dy < 0:
#                 player.rect.top = obj.rect.bottom
#                 player.hit_head()

#             collided_objects.append(obj)
    
#     return collided_objects

# ==================== PLAYER MOVEMENT ====================
def movement(player):
    keys = pygame.key.get_pressed()

    player.velX = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.move_right(PLAYER_VEL)

    # vertical_collision(player, objects, player.velY)

# ==================== MAIN ====================
def main(screen):
    clock = pygame.time.Clock()

    # background
    # background, bg_image = get_background("Brown.png")

    # size of the block
    block_size = 48

    # player
    player = Player(100, 100, 64, 64)
    # floor block
    # floor = [Block(i * block_size, SCREEN_HEIGHT - block_size, block_size) for i in range(10)]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        player.move_loop(FPS)
        movement(player)
        draw(screen, player)

    pygame.quit()

if __name__ == '__main__':
    main(screen)
