import pygame

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = SCREEN_WIDTH * 0.8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pixel Path")
# pygame.display.set_icon(pygame.image.load("icon.png"))
clock = pygame.time.Clock()

class player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('image/heart.png')
        self.image = pygame.transform.scale(img, (32 * scale, 32 * scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(player.image, player.rect)
        
player = player(100, 100, 3)

    # def update(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_LEFT]:
    #             self.x -= self.vel
    #     if keys[pygame.K_RIGHT]:
    #             self.x += self.vel

# Colors
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)

TILE_SIZE = 32


# Groups


running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    

    screen.fill(BROWN) 
      
pygame.quit()