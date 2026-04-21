import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_idle(self, frame, width, height, scale, color):
        idle = pygame.Surface((width, height)).convert_alpha()
        idle.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        idle = pygame.transform.scale(idle, (width * scale, height * scale))
        idle.set_colorkey(color)

        return idle
    
    def get_run(self, frame, width, height, scale, color):
        run = pygame.Surface((width, height)).convert_alpha()
        run.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        run = pygame.transform.scale(run, (width * scale, height * scale))
        run.set_colorkey(color)

        return run

    def get_jump(self, frame, width, height, scale, color):
        jump = pygame.Surface((width, height)).convert_alpha()
        jump.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        jump = pygame.transform.scale(jump, (width * scale, height * scale))
        jump.set_colorkey(color)

        return jump

    def get_fall(self, frame, width, height, scale, color):
        fall = pygame.Surface((width, height)).convert_alpha()
        fall.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        fall = pygame.transform.scale(fall, (width * scale, height * scale))
        fall.set_colorkey(color)

        return fall

    def get_death(self, frame, width, height, scale, color):
        death = pygame.Surface((width, height)).convert_alpha()
        death.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        death = pygame.transform.scale(death, (width * scale, height * scale))
        death.set_colorkey(color)

        return death