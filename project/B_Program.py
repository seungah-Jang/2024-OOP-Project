import pygame
from Parent import *
import sys
from datetime import datetime
#import db
import time
import string
from openai import OpenAI
import os
import Parent

client = OpenAI()
current_dir = os.path.dirname(__file__)
# 선택한 캐릭터 이미지 불러오기




# 데이터베이스 연결
#conn = db.create_connection()

# 1707x1067
def generate_code():
    res = client.completions.create (
        model="gpt-3.5-turbo-instruct",
        prompt=
        "Generate between 10 and 15 lines of Python code. Each line should not exceed 40 characters. The concept of the program should be related to space and aliens, so use space-related variable names. Generate code using different Python syntaxes. Provide different code each time. Do not include code numbers or comments. Provide only the code in your response.",
        temperature = 0,
        max_tokens =500
    )
    return res.choices[0].text

def load_selection():
    try:
        with open('selection.txt', 'r') as file:
            selection = file.read().strip()
            return os.path.join(current_dir, 'data', selection)
            #return pygame.image.load(os.path.join(current_dir, 'data', selection))
    except FileNotFoundError:
        return None

class Program(Screen):
    def draw(self):
        self.screen.fill(WHITE)
        draw_text('Start Program practice', font, BLACK, self.screen, 400, 300)
        pygame.display.update()
# TB_SESSION_RESULT
## (session_start_time,total_keystrokes,correct_cnt,elapsed_time,accuracy,wpm)
# TB_KEY
## (session_id,key_value,total_keyvalue,correct_keyvalue,incorrect_keyvalue)


class B_Play:
    def __init__(self):
        self.correct_cnt = 0
        self.correct_ll = []
        self.sound_trace = False

    def make_key_dic(self):
        # 대문자, 소문자, 숫자 가져오기
        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_characters = string.punctuation

        # 모든 문자들을 합치기
        all_characters = uppercase_letters + lowercase_letters + digits + special_characters

        # 딕셔너리를 생성하고 초기값을 0으로 설정
        key_values_dic = {char: 0 for char in all_characters}

        return key_values_dic
    
    def checkcolor(self,input_len,sentence_ll,current_char,color_text,correct_cnt):
        # text 의 color (같으면 검은색0, 틀리면 빨간색2, 미완이면 회색1)
        if input_len <= len(sentence_ll):
            if current_char == sentence_ll[input_len-1]: #같으면 검은색 (0)
                color_text[input_len-1] = 0
                self.correct_cnt += 1
                
            else:
                color_text[input_len-1] = 2
                self.correct_ll[input_len-1] = 0

    def run(self):
        # 변수 초기화
    
        #correct_cnt = 0
        current = datetime.now()
        session_start_time = current.strftime("%Y-%m-%d %H:%M:%S")
        sTime = time.time() 
        total_keystrokes = 0
        key_values_dic = self.make_key_dic()
        # 초기화
        pygame.init()

        # 화면 설정
        screen = pygame.display.set_mode((850, 900))
        pygame.display.set_caption("타자 연습 프로그램")


        # 색상 설정
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREY = (200, 200, 200)
        RED = (255,0,0)
        BLUE = (0, 0, 255)
        LIGHT_RED = (255, 200, 200)
        YELLOW = (255,255,0)

        # 폰트 설정
        font_size = 26
        # 폰트 설정
        #font = pygame.font.Font(None, 26)

        font_path = os.path.join(os.path.dirname(__file__), '..', 'font', 'DungGeunMo.ttf')
        font = pygame.font.Font(font_path, 26)

        # 배경 이미지 로드
        
        current_dir = os.path.dirname(__file__)

        back_dir = os.path.join(current_dir,'data','background.gif')
        background_image = pygame.image.load(back_dir)
        background_image = pygame.transform.scale(background_image, (850, 900))
        
        
        #font_path = os.path.join(os.path.dirname(__file__), "NANUMGOTHIC.TTF")
        #font = pygame.font.Font(font_path, 20)

        # 연습할 문장
        '''
        sentence = [
            "dic = {'STRAWBERRY':0,'BANANA':0,'LIME':0,'PLUM':0}",
            "N = int(input())",
            "for i in range(N):",
            "   fruit,num = input().split()",
            "   dic[fruit] += int(num)",
            "check=0",
            "for key,value in dic.items():",
            "   if value==5:",
            "       check=1",
            "       break",
            "if check==1:",
            "   print(\"YES\")",
            "else:",
            "   print(\"NO\")",


        ]'''
        '''
        sentence = """dic = {'STRAWBERRY':0,'BANANA':0,'LIME':0,'PLUM':0}
        N = int(input())
        for i in range(N):
            fruit,num = input().split()
            dic[fruit] += int(num)
        check=0
        for key,value in dic.items():
            if value==5:
                check=1
                break
        if check==1:
            print("YES")
        else:
            print("NO")"""
        '''
        sentence = generate_code()
        sentence_ll = list(sentence)
        #sentence_ll = [char for char in sentence if char != ' ']
        print(sentence_ll)
        typed_text = ""
        start_time = None
        wpm = 0
        current_char = ""
        color_text = [1]*len(sentence)
        self.correct_ll = [1]*len(sentence)
        blink = True
        blink_time = 0
        finished = False
        # 메인 루프
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        idx = len(typed_text)-1
                        #print(idx,typed_text[idx],color_text[idx])
                        color_text[idx] = 1
                        #print(color_text[idx])
                        typed_text = typed_text[:-1]
                        self.correct_cnt -= 1
                        self.correct_ll[idx] = 1
                        #print(self.correct_ll[idx-1])
                        #self.checkcolor(input_len,sentence_ll,current_char,color_text,correct_cnt)
                    elif event.key == pygame.K_RETURN:
                        if len(typed_text) < len(sentence_ll):
                            if sentence_ll[len(typed_text)]=='\n':
                                self.correct_cnt += 1
                                typed_text += '\n'

                    elif event.key == pygame.K_TAB:
                        typed_text += '\t'
                    elif event.key == pygame.K_SPACE:
                        if len(typed_text) < len(sentence_ll):
                            if sentence_ll[len(typed_text)]!=' ':
                                color_text[len(typed_text)] = 2
                                typed_text += ' '
                            else:
                                self.correct_cnt += 1
                                typed_text += ' '

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        pass
                    else: #한줄 끝났을 때, 엔터를 누르지 않으면 해당 글자가 거기서 멈추거고 커서가 넘어가지 않도록 처리해야함.
                        if sentence_ll[len(typed_text)] == '\n':
                            continue
                        # 공백인데 다른 키를 누르면 넘어가지 않도록 처리해야함.
                        #if sentence_ll[len(typed_text)] == ' ':
                        #    continue
                        else:
                            if start_time is None: # 처음 키 누를 때, 시작시간 저장
                                start_time = pygame.time.get_ticks()
                            typed_text += event.unicode #event 가 유저가 타이핑한 텍스트인데 이걸 unicode 로 바꿔서 text 에 저장!
                            current_char = event.unicode
                            #입력 텍스트 길이
                            input_len = len(typed_text)
                            #남은 텍스트
                            remaining_text = sentence_ll[input_len:]
                            #print(input_len,len(sentence))
                            
                            #     def checkcolor(self,input_len,sentence_ll,current_char,color_text,correct_cnt):
                            self.checkcolor(input_len,sentence_ll,current_char,color_text,self.correct_cnt)
                            # text 의 color (같으면 검은색0, 틀리면 빨간색2, 미완이면 회색1)
                            '''
                            if input_len <= len(sentence_ll):
                                if current_char == sentence_ll[input_len-1]: #같으면 검은색 (0)
                                    color_text[input_len-1] = 0
                                    correct_cnt += 1
                                else:
                                    color_text[input_len-1] = 2
                            '''

            tmp_total_keystrokes = len(typed_text)
            tmp_correct_cnt = self.correct_cnt
            tmp_elapsed_time = (time.time()-sTime)/60

            #real_accuracy = (tmp_correct_cnt/len(typed_text))* 100
            #print("real accuracy",tmp_correct_cnt,len(sentence_ll))
            
            if len(typed_text)==0:
                real_accuracy = 100
            else:
                #real_accuracy = (tmp_correct_cnt / max(tmp_total_keystrokes, 1)) * 100
                #real_accuracy = (tmp_correct_cnt/len(typed_text))* 100
                real_accuracy = (sum(self.correct_ll)/len(sentence_ll))*100
            #print("real accuracy",self.correct_ll)

            real_wpm = (tmp_total_keystrokes/5)/tmp_elapsed_time
            
            #print("accuracy",real_accuracy)
            # 하단 좌측에 출력할 텍스트 좌표
            left_bottom_x = 20
            left_bottom_y = screen.get_height() - 40  

            # 하단 우측에 출력할 텍스트 좌표
            right_bottom_x = screen.get_width() - 200  
            right_bottom_y = screen.get_height() - 40  
            
            screen.blit(background_image, (0, 0))
            #캐릭터설정
            selected_character = load_selection()
            
            ########## 배경음 ##########
            current_dir = os.path.dirname(__file__)
            bomb_dir = os.path.join(current_dir,'data','boom.wav')
            pygame.mixer.init()
            pygame.mixer.music.load(bomb_dir)  # 음성 파일 경로 설정
            pygame.mixer.music.set_volume(0.5)  # 음량 설정 (0.0 ~ 1.0)

            # 특정 조건을 만족하면 "cry"가 붙여진 이미지 사용
            
            if selected_character and real_accuracy <= 70:
                if real_accuracy <70 and not self.sound_trace:
                    pygame.mixer.music.play()
                    pygame.time.delay(1500)
                    self.sound_trace = True
                base_name, ext = os.path.splitext(selected_character)
                selected_character = f"{base_name}cry{ext}"
                screen.blit(danger_image,(600,30))
            
            danger_dir = os.path.join(current_dir,'data','danger.gif')
            danger_image = pygame.image.load(danger_dir)
            danger_image = pygame.transform.scale(danger_image, (100, 50))


            if selected_character:
                selected_character = pygame.image.load(selected_character)
                selected_character_scaled = pygame.transform.scale(selected_character, (150, 150))
                screen.blit(selected_character_scaled, (650, 50))
                

            '''
            if selected_character:
                if real_accuracy <= 60:
                    base_name, ext = os.path.splitext(selected_character)
                    selected_character = f"{base_name}cry{ext}"
                selected_character_scaled = pygame.transform.scale(selected_character, (150, 150))  # 이미지 크기 조정
                screen.blit(selected_character_scaled, (650, 50))  # 상단 우측에 이미지 표시
            '''
            # 화면 그리기
            #screen.fill(WHITE)sd
            # Real Accuracy 텍스트 생성
            accuracy_text = font.render("Real Accuracy: {:.2f}%".format(real_accuracy), True, BLACK)
            # Real Accuracy 텍스트 화면에 표시 (하단 좌측)
            screen.blit(accuracy_text, (left_bottom_x, left_bottom_y))

            # Real WPM 텍스트 생성
            wpm_text = font.render("Real WPM: {:.2f}".format(real_wpm), True, BLACK)
            # Real WPM 텍스트 화면에 표시 (하단 우측)
            screen.blit(wpm_text, (right_bottom_x, right_bottom_y))
            

            x_offset = 50
            y_offset = 50
            char_width = 12
            line_height = font_size + 10 

            
            #correct_surface = font.render(sentence, True, BLACK)
            #screen.blit(correct_surface, (50, 50))

            for i in range(len(sentence)):
                if sentence[i] == "\n":
                    x_offset = 50
                    y_offset += line_height
                    continue
                if sentence[i] == ' ' and color_text[i] == 2:
                    pygame.draw.rect(screen, LIGHT_RED, (x_offset, y_offset, char_width, font_size))
                
                color = YELLOW if color_text[i] == 0 else RED if color_text[i] == 2 else WHITE    
                # 글자 렌더링
                text_surface = font.render(sentence[i], True, color)
                screen.blit(text_surface, (x_offset, y_offset))
                x_offset += char_width
            
            #print(typed_text)

            #커서 깜빡임 제어
            if current_time - blink_time > 500:
                blink = not blink
                blink_time = current_time

            if blink:
                # 커서 위치 계산
                cursor_x = 50
                cursor_y = 50
                j = 0
                for char in typed_text:
                    if char == '\n':
                        if sentence_ll[j] == '\n':
                            cursor_x = 50
                            cursor_y += line_height
                            j += 1
                        else:
                            j += 1
                            continue
                    elif char == ' ':
                        
                        cursor_x += char_width
                        if cursor_x >= 850 - 50:
                            cursor_x = 50
                            cursor_y += line_height
                        j += 1
                        

                    
                    else: # 공백인데 다른 키를 누르면 커서 넘어가지 않도록 처리해야함./ 해당 줄의 마지막에 엔터인데 다른키를 누르면 움직이지 않도록 해야함.
                        if sentence_ll[j] == '\n':
                            j+=1
                            continue
                        else:
                            cursor_x += char_width
                            if cursor_x >= 850 - 50:
                                cursor_x = 50
                                cursor_y += line_height
                            j += 1
                            
                    

                pygame.draw.rect(screen, BLUE, (cursor_x, cursor_y, 2, font_size))
                if len(typed_text) == len(sentence):
                    total_keystrokes = len(typed_text)
                    finished = True
                    print("True")
                
                #large_font = pygame.font.Font(font_path, 72)
                large_font = pygame.font.Font(None, 72)  # 큰 폰트 설정

                if finished:
                    finish_surface = large_font.render("FINISH", True, RED)
                    screen.blit(finish_surface, ((800 - finish_surface.get_width()) // 2, 800 - finish_surface.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.delay(2000)  # 2초간 "finish" 문구를 보여줌
                    running = False  # 프로그램 종료
            # 화면 업데이트
            pygame.display.flip()
        '''
        elapsed_time = (time.time() - sTime)/60
        accuracy = (correct_cnt/total_keystrokes)*100
        wpm = (total_keystrokes/5)/elapsed_time
        print(session_start_time, total_keystrokes, correct_cnt,elapsed_time,accuracy,wpm)
        ## DB에 insert 할것.
        '''

        return "main_screen"
        # 종료
        #pygame.quit()
        #sys.exit()


if __name__ == "__main__":
    app = B_Play()
    app.run()