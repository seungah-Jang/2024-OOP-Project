import pygame
import os
from Parent import *
from Game1 import *
from Game2 import *  
from Game3 import *
# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

NUMSTARS = 150
WINSIZE = [800,600]
WINCENTER = [320,240]

screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Code Typing Game")

font_path = os.path.join(os.path.dirname(__file__), '..', 'font', 'DungGeunMo.ttf')
font = pygame.font.Font(font_path, 50)


current_dir = os.path.dirname(__file__)
sound_dir = os.path.join(current_dir,'data','MainSound.wav')

#850 900
#800 600

class Game(Screen):
    def __init__(self,screen):
        super().__init__(screen)
        self.button_rects = {
            "Survive1" : pygame.Rect(250, 100, 300, 80),
            "Survive2" : pygame.Rect(250, 250, 300, 80),
            "Survive3" : pygame.Rect(250, 400, 300, 80)
        }
    def draw(self):
        for button_text, rect in self.button_rects.items():
            pygame.draw.rect(self.screen, GRAY, rect)
            draw_text(button_text.replace('_', ' ').title(), font, BLACK, self.screen, rect.centerx, rect.centery)
        
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for screen_name, rect in self.button_rects.items():
                if rect.collidepoint(event.pos):
                    return screen_name
        return None

class C_Play:
    def __init__(self):
        self.screen = screen
        self.current_screen = Game(self.screen)
        self.screens = {
            "main_screen" : Main_Screen(self.screen),
            "Game_main_screen" : Game(self.screen),
            "Survive1" : Game1_Screen(self.screen),
            "Survive2" : Game2_Screen(self.screen),
            "Survive3" : Game3_Screen(self.screen)
        }
    def run(self):
        done = False
        while not done:
            screen.fill(BLACK)

        
            self.current_screen.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                    done = True
                    break
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.current_screen = self.screens["Game_main_screen"]

                screen_name = self.current_screen.handle_event(e)
                if screen_name:
                    self.current_screen = self.screens[screen_name]

                if self.current_screen == self.screens["main_screen"]:
                    program_play = Main_Screen()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
                
                if self.current_screen == self.screens["Survive1"]:
                    program_play = Game1_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
                
                if self.current_screen == self.screens["Survive2"]:
                    program_play = Game2_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]

                if self.current_screen == self.screens["Survive3"] :
                    program_play = Game3_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
                
                #else:
                #    
            pygame.display.flip()

        return "main_screen"
        #pygame.quit()

if __name__ == '__main__':
    app = C_Play()
    app.run()