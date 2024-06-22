from Parent import *
import pygame
import sys
import os
import time
from B_Program import *
from C_Game import *  
from D_Setting import *
from F_Exit import *
from Parent import *

black = 20, 20, 40
white = 255, 240, 200

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

NUMSTARS = 150
WINSIZE = [850,900]
WINCENTER = [320,240]

screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption("Code Typing Game")

font_path = os.path.join(os.path.dirname(__file__), '..', 'font', 'DungGeunMo.ttf')
font = pygame.font.Font(font_path, 21)

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

current_dir = os.path.dirname(__file__)

sound_dir = os.path.join(current_dir,'data','MainSound.wav')

pygame.mixer.init()
pygame.mixer.music.load(sound_dir)  # 음성 파일 경로 설정
pygame.mixer.music.set_volume(0.5)  # 음량 설정 (0.0 ~ 1.0)




# 텍스트를 한 줄씩 그리는 함수
def line_draw_text(screen, text, position, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# 색상을 번갈아가면서 텍스트를 표시하는 함수
def draw_colored_text(screen, text, position, finished=False):
    x, y = position
    for i, char in enumerate(text):
        if finished:
            color = WHITE
        else:
            color = YELLOW if i % 2 == 0 else CYAN
        char_surface = font.render(char, True, color)
        screen.blit(char_surface, (x, y))
        x += char_surface.get_width()



###### draw star ########
def init_star(steps=-1):
    "creates new star values"
    dir = random.randrange(100000)
    steps_velocity = 1 if steps == -1 else steps * 0.09
    velmult = steps_velocity * (random.random() * 0.6 + 0.4)
    vel = [math.sin(dir) * velmult, math.cos(dir) * velmult]

    if steps is None:
        return [vel, [WINCENTER[0] + (vel[0] * steps), WINCENTER[1] + (vel[1] * steps)]]
    return [vel, WINCENTER[:]]


def initialize_stars():
    "creates a new starfield"
    random.seed()
    stars = [init_star(steps=random.randint(0, WINCENTER[0])) for _ in range(NUMSTARS)]
    move_stars(stars)
    return stars


def draw_stars(surface, stars, color):
    "used to draw (and clear) the stars"
    for _, pos in stars:
        pos = (int(pos[0]), int(pos[1]))
        surface.set_at(pos, color)


def move_stars(stars):
    "animate the star values"
    for vel, pos in stars:
        pos[0] = pos[0] + vel[0]
        pos[1] = pos[1] + vel[1]
        if not 0 <= pos[0] <= WINSIZE[0] or not 0 <= pos[1] <= WINSIZE[1]:
            vel[:], pos[:] = init_star()
        else:
            vel[0] = vel[0] * 1.05
            vel[1] = vel[1] * 1.05

class Main_Screen(Screen):
    def __init__(self,screen):
        super().__init__(screen)
        self.button_rects = {
            "Setting" : pygame.Rect(30, 810, 100, 50),
            "Practice" : pygame.Rect(200, 810, 100, 50),
            "Survive" : pygame.Rect(600, 810, 100, 50)
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




class A_Play:
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
        # 음성 재생
        pygame.mixer.music.play(-1)
        "This is the starfield code"
        # create our starfield
        stars = initialize_stars()

        # initialize and prepare screen
        pygame.init()
        
        screen.fill(BLACK)

        clock = pygame.time.Clock()

        text_index = 0
        letter_index = 0
        show_time = 0.05  # 각 글자의 딜레이 (초)
        last_update_time = time.time()

        # main game loop
        done = False
        while not done:
            screen.fill(BLACK)

            current_time = time.time()
            if current_time - last_update_time > show_time:
                last_update_time = current_time
                if text_index < len(story):
                    if letter_index < len(story[text_index]):
                        letter_index += 1
                    else:
                        text_index += 1
                        letter_index = 0

            y = 50
            for i in range(text_index):
                line_draw_text(screen, story[i], (50, y))
                y += 40

            if text_index < len(story):
                current_text = story[text_index][:letter_index]
                draw_colored_text(screen, current_text, (50, y))
            else:
                for i in range(len(story)):
                    draw_colored_text(screen, story[i], (50, 50 + 40 * i), finished=True)

            draw_stars(screen, stars, BLACK)
            move_stars(stars)
            draw_stars(screen, stars, WHITE)

            self.current_screen.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT or (e.type == pygame.KEYUP and e.key == pygame.K_ESCAPE):
                    done = True
                    break
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    WINCENTER[:] = list(e.pos)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        self.current_screen = self.screens["main_screen"]

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
                #else:
                #    
            #pygame.display.flip()
            clock.tick(50)
        pygame.quit()
    
if __name__ == "__main__":
    app = A_Play()
    app.run()
