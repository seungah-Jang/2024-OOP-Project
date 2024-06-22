import pygame
from Parent import *
import os
class Setting(Screen):
    def draw(self):
        self.screen.fill(WHITE)
        draw_text('Start Setting', font, BLACK, self.screen, 400, 300)
        pygame.display.update()


import pygame
import sys
import os
import Parent

def save_selection(selection):
    with open('selection.txt', 'w') as file:
        file.write(selection)

pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('캐릭터 선택')



current_dir = os.path.dirname(__file__)

ch1_dir = os.path.join(current_dir, 'data', 'character1.png')
ch2_dir = os.path.join(current_dir, 'data', 'character2.png')

# 화면 크기 설정
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('캐릭터 선택')

# 캐릭터 이미지 로드 및 크기 조정
character1 = pygame.image.load(ch1_dir)
character2 = pygame.image.load(ch2_dir)
character1 = pygame.transform.scale(character1, (100, 100))  # 이미지 크기 조정
character2 = pygame.transform.scale(character2, (100, 100))  # 이미지 크기 조정

# 위치 설정
character1_rect = character1.get_rect(center=(200, 300))
character2_rect = character2.get_rect(center=(600, 300))

class D_Play:
    def run(self):
        selected_character = None
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if character1_rect.collidepoint(event.pos):
                        Parent.selected_character = 'character1.png'
                        selected_character = 'character1.png'
                        save_selection('character1.png')
                    elif character2_rect.collidepoint(event.pos):
                        Parent.selected_character = 'character2.png'
                        selected_character = 'character2.png'
                        save_selection('character2.png')
            #print(selected_character)
            screen.fill((255, 255, 255))
            
            # 캐릭터 이미지를 화면에 그리기
            screen.blit(character1, character1_rect)
            screen.blit(character2, character2_rect)

            # 선택된 캐릭터에 빨간색 테두리 그리기
            if selected_character == 'character1.png':
                pygame.draw.rect(screen, (255, 0, 0), character1_rect, 3)  # 빨간색 테두리
            elif selected_character == 'character2.png':
                pygame.draw.rect(screen, (255, 0, 0), character2_rect, 3)  # 빨간색 테두리

            pygame.display.flip()
        return "main_screen"


if __name__ == '__main__':
    app = D_Play()
    app.run()
