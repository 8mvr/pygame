import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 432
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("My pygame")

scroll = 0

bg_images = []
BG_WIDTH = 800
BG_HEIGHT = 432

for i in range(1, 6):
    bg_image = pygame.image.load(f"pix-{i}.png").convert_alpha()
    bg_images.append(bg_image)


ground_image = pygame.image.load("ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()


def draw_bg():
    for y in range(5):
        speed = 1
        for img in bg_images:
            (0, (y * height) - scroll * speed)
            screen.blit(img, (0, (y * BG_HEIGHT) - scroll * speed))
            speed += 0.2

def draw_ground():
    for x in range(15):
        screen.blit(ground_image, (x * ground_width, SCREEN_HEIGHT - ground_height - scroll * 2.5))


run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_ground()

   
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and scroll > 0: 
        scroll -= 5
    if key[pygame.K_DOWN] and scroll < 3000: 
        scroll += 5

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()