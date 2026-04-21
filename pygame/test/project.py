import pygame
import characterSprite

pygame.init()

SCREEN_WIDTH = 950
SCREEN_HEIGTH = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Pixel Path")
clock = pygame.time.Clock()

# Size
C_WIDTH = 32
C_HEIGTH = 32

# Gravity
GRAVITY = 0.6
JUMP_HEIGTH = -12

# Colors
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)

# idle
idle_image = pygame.image.load('image/male_hero-idle.png').convert_alpha()
idle_sheet = characterSprite.SpriteSheet(idle_image)

# run
run_image = pygame.image.load('image/male_hero-run.png').convert_alpha()
run_sheet = characterSprite.SpriteSheet(run_image)

# jump || fall
jump_image = pygame.image.load('image/male_hero-jump.png').convert_alpha()
jump_sheet = characterSprite.SpriteSheet(jump_image)

fall_image = pygame.image.load('image/male_hero-fall.png').convert_alpha()
fall_sheet = characterSprite.SpriteSheet(fall_image)

# death
death_image = pygame.image.load('image/male_hero-death.png').convert_alpha()
death_sheet = characterSprite.SpriteSheet(death_image)

# animation
animation_list = []
animation_steps = [idle_sheet, run_sheet, jump_sheet, fall_sheet, death_sheet]
action = 0
last_update = pygame.time.get_ticks()
anim_cooldown = 300 # millisecond
frame = 0
step_count = 0



# for animation in animation_steps:
#     temp_image_list = []
#     for _ in range(animation):
#         temp_image_list.append(idle_sheet.get_idle(step_count, 128, 128, 1.5, BLACK))
#         step_count += 1
#     animation_list.append(temp_image_list)

# animation_run = idle_sheet.get_idle(step_count, 128, 128, 1.5, BLACK)

run = True

while run:
    clock.tick(60)
    screen.fill(BROWN)

    # update animation

    # show frame idle
    # screen.blit(animation_list[action][frame], (0, 600))
        
    # screen.blit(animation_run, (0, 100))
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
       
        # if event.type == pygame.KEYDOWN:
        #     if event.type == pygame.K_LEFT:ke


    pygame.display.update()
pygame.quit()