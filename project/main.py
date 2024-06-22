import pygame
import sys
from B_Program import *
from C_Game import * 
from D_Setting import *
from F_Exit import *
from Parent import *
#import db
import time
import random
import math

# 데이터베이스 연결
#conn = db.create_connection()

# 초기화
pygame.init()

# 화면 설정
screen = pygame.display.set_mode((800, 900))
pygame.display.set_caption("타자 연습 프로그램")
# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
black = 20, 20, 40
white = 255, 240, 200
#폰트
font = pygame.font.Font(None, 36)



class MainPage(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.button_rects = {
            "1. Grammer Practice": pygame.Rect(300, 200, 200, 50),
            "2. Program Practice": pygame.Rect(300, 300, 200, 50),
            "3. Game": pygame.Rect(300, 400, 200, 50),
            "4. Analysis": pygame.Rect(300, 500, 200, 50),
            "5. Setting": pygame.Rect(300, 600, 200, 50),
            "6. Exit": pygame.Rect(300, 700, 200, 50),
        }

    def draw(self):
        #self.screen.fill(black)
        #draw_text('Coding Typing Program', font, BLACK, self.screen, 400, 100)
        
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

class TypingProgram:
    # 첫화면 진입 시 메인 화면
    def __init__(self):
        
        self.screen = screen
        self.current_screen = MainPage(self.screen)
        self.screens = {
            "main_screen" : MainPage(self.screen),
            "1. Grammer Practice" : Grammer(self.screen),
            "2. Program Practice" : Program(self.screen),
            "3. Game" : Game(self.screen),
            "4. Analysis" : Analysis(self.screen),
            "5. Setting" : Setting(self.screen),
        }



    

    def run(self):
        screen.fill(black)
        clock = pygame.time.Clock()
        class_Stars = Stars()
        stars = class_Stars.initialize_stars()
        while True:
            for event in pygame.event.get():
                class_Stars.draw_stars(screen,stars,black)
                class_Stars.move_stars(stars)
                class_Stars.draw_stars(screen,stars,white)
                pygame.display.update()
                # 창을 닫거나, esc 눌렀을 때 닫힘
                if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    class_Stars.WINCENTER[:] = list(event.pos)
                
                # backspace 누르면 다시 메인화면으로!

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.current_screen = self.screens["main_screen"]
                    
                # 클릭한 스크린 이름 반환
                screen_name = self.current_screen.handle_event(event)
                #해당 스크린 클릭했을 때, 화면 전환
                if screen_name:
                    self.current_screen = self.screens[screen_name]
            
                if self.current_screen == self.screens["2. Program Practice"]:
                    
                    program_play = B_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
                
                else:
                    self.current_screen.draw()
                
                #pygame.display.update()

if __name__ == "__main__":
    app = TypingProgram()
    app.run()