
import pygame
import random
import time
import os

class c:
    def run(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        # Set up the display
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Load background image
        os.chdir('/Users/hyeonjuyeon/Downloads/python/3')
        background = pygame.image.load('background3.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Cut image
        cut = pygame.image.load('cut.png')
        cut = pygame.transform.scale(cut, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Font
        font = pygame.font.Font(None, 74)
        player_font = pygame.font.Font(None, 30)
        small_font = pygame.font.Font(None, 80)

        # Code parts list
        code_front = ["print(", "for i in range(", "if x > ", "while "]
        code_back = ["'hello world')", "10): print(i)", "5: print('x is greater than 5')", "True: print('loop')"]

        # Shuffle the back parts of the code but keep the indices consistent
        def create_shuffled_code_lists():
            shuffled_indices = list(range(len(code_back)))
            random.shuffle(shuffled_indices)
            shuffled_code_back = [code_back[i] for i in shuffled_indices]
            return shuffled_indices, shuffled_code_back

        shuffled_indices, shuffled_code_back = create_shuffled_code_lists()

        # Game variables
        player_score = 0
        current_step = 0
        player_input_text1 = ""
        player_input_text2 = ""
        game_over = False
        timer_start = time.time()
        TIMER_DURATION = 60  # seconds for the bomb timer
        input_box1 = pygame.Rect(230, SCREEN_HEIGHT - 100, 300, 32)
        input_box2 = pygame.Rect(230, SCREEN_HEIGHT - 50, 300, 32)
        active_box = input_box1  # Start with input_box1 as active

        def check_code(front, back):
            global current_step
            expected_code = code_front[current_step].strip() + code_back[current_step].strip()
            user_code = front.strip() + back.strip()
            return expected_code == user_code

        def display_cut():
            screen.blit(cut, (0, 0))
            pygame.display.flip()
            pygame.time.wait(1000)

        # Main game loop
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active_box = input_box1
                    elif input_box2.collidepoint(event.pos):
                        active_box = input_box2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if check_code(player_input_text1, player_input_text2):
                            player_score += 1
                            current_step += 1
                            if current_step >= len(code_front):
                                current_step = 0
                                shuffled_indices, shuffled_code_back = create_shuffled_code_lists()
                            player_input_text1 = ""
                            player_input_text2 = ""
                            display_cut()
                        else:
                            game_over = True
                    elif event.key == pygame.K_BACKSPACE:
                        if active_box == input_box1:
                            player_input_text1 = player_input_text1[:-1]
                        elif active_box == input_box2:
                            player_input_text2 = player_input_text2[:-1]
                    else:
                        if active_box == input_box1:
                            player_input_text1 += event.unicode
                        elif active_box == input_box2:
                            player_input_text2 += event.unicode

            if game_over:
                break

            screen.blit(background, (0, 0))

            # Draw code parts
            for i, front in enumerate(code_front):
                back_index = shuffled_indices[i]
                back = code_back[back_index]
                front_surface = player_font.render(f"{i + 1}. {front}", True, BLACK)
                back_surface = player_font.render(f"{i + 1}. {back}", True, BLACK)
                screen.blit(front_surface, (50, 50 + i * 50))
                screen.blit(back_surface, (500, 50 + i * 50))

            # Draw input texts
            player_input_surface1 = player_font.render(player_input_text1, True, BLACK)
            screen.blit(player_input_surface1, (input_box1.x + 5, input_box1.y + 7))

            player_input_surface2 = player_font.render(player_input_text2, True, BLACK)
            screen.blit(player_input_surface2, (input_box2.x + 5, input_box2.y + 7))

            # Draw input boxes
            pygame.draw.rect(screen, BLACK, input_box1, 2)
            pygame.draw.rect(screen, BLACK, input_box2, 2)

            # Draw scores
            player_score_surface = small_font.render(f"{player_score}", True, BLACK)
            screen.blit(player_score_surface, (415, 365))

            # Timer and cut logic
            elapsed_time = time.time() - timer_start
            remaining_time = TIMER_DURATION - elapsed_time
            timer_surface = small_font.render(f"00:{int(remaining_time)}", True, RED)
            screen.blit(timer_surface, (330, 270))  # 타이머 위치 조정

            if remaining_time <= 0:
                game_over = True
                break

            pygame.display.flip()

        # Game over screen
        if game_over:
            screen.fill(WHITE)
            game_over_surface = font.render("Game Over", True, RED)
            screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)

        pygame.quit()

# Create an instance of class `c` and call the `run` method
if __name__ == "__main__":
    game_instance = c()
    game_instance.run()
