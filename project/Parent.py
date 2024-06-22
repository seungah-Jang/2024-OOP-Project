import pygame
import random
import math
# 초기화
pygame.init()

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

selected_character = None

#폰트
font = pygame.font.Font(None, 36)

class Stars:
    def __init__(self):
        self.WINSIZE = [800, 900]
        self.WINCENTER = [400, 450]
        self.NUMSTARS = 150

    def init_star(self,steps=-1):
        "creates new star values"
        dir = random.randrange(100000)
        steps_velocity = 1 if steps == -1 else steps * 0.09
        velmult = steps_velocity * (random.random() * 0.6 + 0.4)
        vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]

        if steps is None:
            return [vel, [self.WINCENTER[0] + (vel[0] * steps), self.WINCENTER[1] + (vel[1] * steps)]]
        return [vel, self.WINCENTER[:]]

    def initialize_stars(self):
        "creates a new starfield"
        random.seed()
        stars = [self.init_star(steps=random.randint(0, self.WINCENTER[0])) for _ in range(self.NUMSTARS)]
        self.move_stars(stars)
        return stars


    def draw_stars(self,surface, stars, color):
        "used to draw (and clear) the stars"
        for _, pos in stars:
            pos = (int(pos[0]), int(pos[1]))
            surface.set_at(pos, color)


    def move_stars(self,stars):
        "animate the star values"
        for vel, pos in stars:
            pos[0] = pos[0] + vel[0]
            pos[1] = pos[1] + vel[1]
            if not 0 <= pos[0] <= self.WINSIZE[0] or not 0 <= pos[1] <= self.WINSIZE[1]:
                vel[:], pos[:] = self.init_star()
            else:
                vel[0] = vel[0] * 1.05
                vel[1] = vel[1] * 1.05

class Screen:
    def __init__(self, screen):
        self.screen = screen
        print("ss")
    
    def draw(self):
        pass

    def handle_event(self, event):
        pass

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)