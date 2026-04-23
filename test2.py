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
animations = {
    "idle": (10, 128),
    "run": (10, 768),
    "jump": (6, 1280),
    "fall": (4, 1408),
    "death": (23, 3072)
}

# Create animation lists for each action
anim_lists = {}
for action_name, (anim_step, y_offset) in animations.items():
    anim_list = []
    for x in range(anim_step):
        anim_list.append(get_image(sprite_sheet_image, x, 128, 128, 1.5, y_offset))
    anim_lists[action_name] = anim_list

current_action = "idle"
last_update = pygame.time.get_ticks()
anim_cooldown = 100  # millisecond
frame = 0  # start of the frame
direction = "right"

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(FPS)

    # Get keyboard input
    keys = pygame.key.get_pressed()
    
    # Change animation and direction based on input
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        current_action = "run"
        direction = "left"
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        current_action = "run"
        direction = "right"
    else:
        current_action = "idle"

    # Update animation frame
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= anim_cooldown:
        frame += 1
        last_update = current_time
        # Reset frame when animation completes
        if frame >= len(anim_lists[current_action]):
            frame = 0

    screen.fill(CUSTOM_1)
    
    # Get the current frame image
    current_image = anim_lists[current_action][frame]
    
    # Flip the image if facing left
    if direction == "left":
        current_image = pygame.transform.flip(current_image, True, False)
        current_image.set_colorkey(BLACK)
    
    screen.blit(current_image, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()
