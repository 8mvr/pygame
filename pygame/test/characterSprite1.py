import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_idle(self, frame, width, heigth, scale, color):
        idle = pygame.Surface((width, heigth)).convert_alpha()
        idle.blit(self.sheet, (0, 0), ((frame * width), 0, width, heigth))
        idle = pygame.transform.scale(idle, (width * scale, heigth * scale))
        idle.set_colorkey(color)

        return idle
    
    def get_run(self, frame, width, heigth, scale, color):
        run = pygame.Surface((width, heigth)).convert_alpha()
        run.blit(self.sheet, (0, 0), ((frame * width), 0, width, heigth))
        run = pygame.transform.scale(run, (width * scale, heigth * scale))
        run.set_colorkey(color)

        return run
    
    def get_jump(self, frame, width, heigth, scale, color):
        jump = pygame.Surface((width, heigth)).convert_alpha()
        jump.blit(self.sheet, (0, 0), ((frame * width), 0, width, heigth))
        jump = pygame.transform.scale(jump, (width * scale, heigth * scale))
        jump.set_colorkey(color)

        return jump
    
    def get_fall(self, frame, width, heigth, scale, color):
        fall = pygame.Surface((width, heigth)).convert_alpha()
        fall.blit(self.sheet, (0, 0), ((frame * width), 0, width, heigth))
        fall = pygame.transform.scale(fall, (width * scale, heigth * scale))
        fall.set_colorkey(color)

        return fall
    
    def get_death(self, frame, width, heigth, scale, color):
        death = pygame.Surface((width, heigth)).convert_alpha()
        death.blit(self.sheet, (0, 0), ((frame * width), 0, width, heigth))
        death = pygame.transform.scale(death, (width * scale, heigth * scale))
        death.set_colorkey(color)

        return death