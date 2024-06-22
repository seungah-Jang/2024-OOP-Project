import pygame
from Parent import *

class Game(Screen):
    def draw(self):
        self.screen.fill(WHITE)
        draw_text('Start Game', font, BLACK, self.screen, 400, 300)
        pygame.display.update()