import pygame
import spritesheet

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Colors
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BROWN = (101, 67, 33)
BLACK = (0, 0, 0)

FPS = 60
PLAYER_VEL = 5

def get_background():
    pass
moving_left = False
moving_rigth = False
isJump = False

class character(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.screen.blit(anim_list[action][frame], (0, 500))

    # def char_draw(self):
        

# sheets
idle_sprite = pygame.image.load('image/male_hero-idle.png').convert_alpha()
idle_sheet = spritesheet.SpriteSheet(idle_sprite)

run_sprite = pygame.image.load('image/male_hero-run.png').convert_alpha()
run_sheet = spritesheet.SpriteSheet(run_sprite)

jump_sprite = pygame.image.load('image/male_hero-jump.png').convert_alpha()
jump_sheet = spritesheet.SpriteSheet(jump_sprite)

# death_sprite = pygame.image.load('image/male_hero-death.png').convert_alpha()
# death_sheet = spritesheet.SpriteSheet(death_sprite)



# Animation image count
idle_steps = 10
run_steps = 10
jump_steps = 10

idle_list = []
for x in range(idle_steps):
    idle_list.append(idle_sheet.get_idle(x, 128, 128, 1.5, BLACK))

run_list = []
for x in range(run_steps):
    run_list.append(run_sheet.get_run(x, 128, 128, 1.5, BLACK))

jump_list = []
for x in range(jump_steps):
    jump_list.append(jump_sheet.get_jump(x, 128, 128, 1.5, BLACK))
    

# fall_list = []
# for x in range(fall_steps):
#     fall_list.append(fall_sheet.get_fall(x, 128, 128, 1.5, BLACK))

anim_list = [idle_list, run_list, jump_list]
action = 0
last_update = pygame.time.get_ticks()
anim_cooldown = 100
frame = 0

def main(screen):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()



if __name__ == '__main__':
    main(screen)
        # update animation
        # current_time = pygame.time.get_ticks()
        # if current_time - last_update >= anim_cooldown:
        #     frame += 1
        #     last_update = current_time
        #     if frame >= len(anim_list[action]):
        #         frame = 0

        # # show frame image
        # # screen.blit(anim_list[action][frame], (0, 500))
        
        
        
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_LEFT:
        #             moving_left = True
                    

        #         if event.key == pygame.K_RIGHT:
        #             moving_right = True

        #         if event.key == pygame.K_SPACE:
        #             isJump = True


        #         if event.key == pygame.K_ESCAPE:
        #             run = False

        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT:
        #             moving_left = False
        #         if event.key == pygame.K_RIGHT:
        #             moving_right = False
        #         if event.key == pygame.K_SPACE:
        #             isJump = False

        # pygame.display.update()
