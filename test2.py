import pygame

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
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

# image
sprite_sheet_image = pygame.image.load("assets/MainCharacter/male_hero.png").convert_alpha()

def get_image(sheet, frame, width, height, scale, y_offset):
    image = pygame.Surface((width, height)).convert_alpha()

    # vertical of the image animation: 128=idle, 768=run, 1280=jump, 1408=fall, 3072=death
    image.blit(sheet, (0, 0), ((frame * width), y_offset, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(BLACK)

    return image

# animations: frames, vertical position
ANIMATIONS = {
    "idle": (10, 128),
    "run": (10, 768),
    "jump": (6, 1280),
    "fall": (4, 1408),
    "death": (23, 3072)
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_sheet):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.x = x
        self.y = y
        self.current_action = "idle"
        self.direction = "right"
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.anim_cooldown = 100  # milliseconds
        
        # Create animation lists for each action
        self.anim_lists = {}
        for action_name, (anim_step, y_offset) in ANIMATIONS.items():
            anim_list = []
            for x in range(anim_step):
                anim_list.append(get_image(sprite_sheet, x, 128, 128, 1.5, y_offset))
            self.anim_lists[action_name] = anim_list
        
        # Set initial sprite
        self.image = self.anim_lists[self.current_action][self.frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.anim_cooldown:
            self.frame += 1
            self.last_update = current_time
            # reset frame
            if self.frame >= len(self.anim_lists[self.current_action]):
                self.frame = 0
    
    def set_action(self, action, direction=None):
        if action != self.current_action:
            self.current_action = action
            self.frame = 0
        if direction:
            self.direction = direction
    
    def update(self):
        self.update_animation()
        
        # Get current frame image
        current_image = self.anim_lists[self.current_action][self.frame]
        
        # Flip the image if facing left
        if self.direction == "left":
            current_image = pygame.transform.flip(current_image, True, False)
            current_image.set_colorkey(BLACK)
        
        self.image = current_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

# Create player
player = Player(0, 0, sprite_sheet_image)

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(FPS)

    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Change animation and direction based on input
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.set_action("run", "left")
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.set_action("run", "right")
    else:
        player.set_action("idle")

    # Update player
    player.update()

    screen.fill(CUSTOM_1)
    player.draw(screen)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
