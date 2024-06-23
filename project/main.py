from Parent import *
import pygame
import sys
import os
import time
from B_Program import *
from C_Game import *  
from D_Setting import *
from Parent import *

class Text_process:
    # 텍스트를 한 줄씩 그리는 함수
    def line_draw_text(self,screen, text, position, color=WHITE):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)

    # 색상을 번갈아가면서 텍스트를 표시하는 함수
    def draw_colored_text(self,screen, text, position, finished=False):
        x, y = position
        for i, char in enumerate(text):
            if finished:
                color = WHITE
            else:
                color = YELLOW if i % 2 == 0 else CYAN
            char_surface = font.render(char, True, color)
            screen.blit(char_surface, (x, y))
            x += char_surface.get_width()

# color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

#window size
NUMSTARS = 150
WINSIZE = [850,900]
WINCENTER = [320,240]

screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Code Typing Game")

# font
font_path = os.path.join(os.path.dirname(__file__), '..', 'font', 'DungGeunMo.ttf')
font = pygame.font.Font(font_path, 21)

current_dir = os.path.dirname(__file__)

# instance
stars_istance = Stars()
texts_instance = Text_process()


###### story ###########
story = [
    "코딩별에 사는 외계인은 파이썬을 무지 좋아해서 지구로 내려왔습니다.",
    "문제는 성격이 너무 급해 타이핑이 느린 지구인을 굉장히 답답해합니다!",
    "",
    "당신은 코딩별로 납치되었습니다 ...",
    "눈 떠 보니 외계인이 지구에서 폭탄을 들고 왔네요 !",
    "놀랍게도 코딩별에 오니 외계인이랑 대화를 하고 있습니다.",
    "",
    "",
    "외계인 왈..",
    "",
    "외 : 이게 뭐야?",
    "지구인 : 건들지마 ...!! 터지면 죽어 !!!",
    "외 : 그럼 우리가 만든 프로그램 미션 완수하면 살려줄게.",
    "타이핑이 왜 이렇게 답답해? 우리별에선 너처럼 독수리타자는 없다구!",
    "",
    "컴퓨터 한 대와 폭탄을 넣고 가둬버렸습니다.",
    "친절하게도 연습 시간은 주네요 !!",
    "",
    "연습시간이 완료되면 3가지 미션을 완수해보세요!!"
]

########## 배경음 ##########
sound_dir = os.path.join(current_dir,'data','MainSound.wav')
pygame.mixer.init()
pygame.mixer.music.load(sound_dir)
pygame.mixer.music.set_volume(0.5)  # 음량 설정 (0.0 ~ 1.0)




# screen 이름을 반환 / UI (버튼, text) / 버튼 마우스 클릭 동작
class Main_Screen(Screen):
    def __init__(self,screen):
        super().__init__(screen)
        self.button_rects = {
            "Setting" : pygame.Rect(30, 810, 100, 50),
            "Practice" : pygame.Rect(200, 810, 100, 50),
            "Survive" : pygame.Rect(600, 810, 100, 50)
        }
    # 버튼 text,버튼 배경 그리기
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




class A_Play:
    # screen 설정
    def __init__(self):
        self.screen = screen
        self.current_screen = Main_Screen(self.screen)
        self.screens = {
            "main_screen" : Main_Screen(self.screen),
            "Setting" : Setting(self.screen),
            "Practice" : Program(self.screen),
            "Survive" : Game(self.screen)
        }
    
    def run(self):

        # initialize and prepare screen
        pygame.init()
        screen.fill(BLACK)
        clock = pygame.time.Clock()

        # 음성 재생
        pygame.mixer.music.play(-1)

        # create starfield
        stars = stars_istance.initialize_stars()

        # text
        text_index = 0
        letter_index = 0
        show_time = 0.05  # 각 글자의 딜레이 (초)
        last_update_time = time.time()

        done = False
        while not done:
            screen.fill(BLACK)
            current_time = time.time()
            if current_time - last_update_time > show_time:
                last_update_time = current_time
                if text_index < len(story):
                    if letter_index < len(story[text_index]):
                        letter_index += 1 #다음 글자
                    else:
                        text_index += 1 # 다음 줄로
                        letter_index = 0
            # 완료된 한줄 텍스트 WHITE로
            y = 50
            for i in range(text_index):
                texts_instance.line_draw_text(screen, story[i], (50, y))
                y += 40
            # 현재 표시 중인 텍스트
            if text_index < len(story):
                current_text = story[text_index][:letter_index]
                texts_instance.draw_colored_text(screen, current_text, (50, y))
            # 모든 줄 완료되면 모두 흰색으로
            else:
                for i in range(len(story)):
                    texts_instance.draw_colored_text(screen, story[i], (50, 50 + 40 * i), finished=True)
            
            ###stars####
            stars_istance.draw_stars(screen, stars, BLACK)
            stars_istance.move_stars(stars)
            stars_istance.draw_stars(screen, stars, WHITE)
            
            self.current_screen.draw()

            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                    done = True
                    break
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    stars_istance.WINCENTER[:] = list(e.pos)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.current_screen = self.screens["main_screen"]

                # 스크린 클릭 시 화면 전환
                screen_name = self.current_screen.handle_event(e)
                if screen_name:
                    self.current_screen = self.screens[screen_name]

                if self.current_screen == self.screens["Practice"]:
                    program_play = B_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
                
                if self.current_screen == self.screens["Setting"]:
                    program_play = D_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]

                if self.current_screen == self.screens["Survive"] :
                    program_play = C_Play()
                    screen_name = program_play.run()
                    self.current_screen = self.screens[screen_name]
            clock.tick(50)
        pygame.quit()
    
if __name__ == "__main__":
    app = A_Play()
    app.run()
