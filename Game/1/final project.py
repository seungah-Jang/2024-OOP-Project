import pygame
import random
import time
import os

class a:
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
        os.chdir('/Users/hyeonjuyeon/Downloads/python/1')
        background = pygame.image.load('background.png')
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Bomb image
        bomb = pygame.image.load('bomb.png')
        bomb_size = bomb.get_rect().size
        bomb_width = bomb_size[0]
        bomb_height = bomb_size[1]

        # Bomb2 image
        bomb2 = pygame.image.load('bomb2.png')
        bomb2 = pygame.transform.scale(bomb2, (int(bomb2.get_width() * 0.8), int(bomb2.get_height() * 0.8)))
        bomb2_size = bomb.get_rect().size
        bomb2_width = bomb2_size[0]
        bomb2_height = bomb2_size[1]

        # Font
        font = pygame.font.Font(None, 74)
        player_font = pygame.font.Font(None, 30)
        small_font = pygame.font.Font(None, 36)

        # Word list
        words = ["Print", "import", "def", "return", "if", "elif",
                "else", "for", "while", "break", "continue", 
                "pass", "class", "try", "except", "finally", 
                "raise", "with", "as", "lambda", "yield",
                "global", "nonlocal", "assert", "del", "from", 
                "is", "in", "not", "and", "or", 
                "True", "False", "None", "input", "open", 
                "read", "write", "close", "range", "len", 
                "list", "tuple", "dict", "set", "str", 
                "int", "float", "bool", "type", "dir", 
                "help", "id", "sum", "min", "max", 
                "abs", "round", "pow", "sorted", "reversed", 
                "zip", "enumerate", "all", "any", "map", "filter", 
                "reduce", "lambda", "iter", "next", "slice", 
                "super", "self", "classmethod", "staticmethod", "property", 
                "__init__", "__str__", "__repr__", "__len__", "__getitem__", 
                "__setitem__", "__delitem__", "__iter__", "__next__", "__contains__", 
                "__call__", "__enter__", "__exit__", "try:", "except:", 
                "finally:", "with open", "as f:", "import os"]

        # Game variables
        current_word = random.choice(words)
        player_score = 0
        computer_score = 0
        player_input_text = ""
        computer_input_text = ""
        game_over = False
        timer_start = time.time()
        TIMER_DURATION = 30  # seconds for the bomb timer
        computer_level = 3  # Computer level (1: easy, 2: medium, 3: hard)
        player_input_box = pygame.Rect(100, SCREEN_HEIGHT - 260, 140, 32)
        computer_input_box = pygame.Rect(SCREEN_WIDTH - 230, SCREEN_HEIGHT - 260, 140, 32)
        next_word_time = None  # To track the time when the word changes

        def computer_typing_simulation(frames_per_char=0.05):
            nonlocal computer_input_text, computer_score, current_word, player_input_text, next_word_time
            
            if next_word_time is None or time.time() - next_word_time > 1:  # Add delay between words
                next_word_time = time.time()
                chars_to_type = min(len(current_word) - len(computer_input_text), 1)  # Type one character at a time
                if frames_per_char <= 0:
                    frames_per_char = 1  # Prevent division by zero

                if random.random() < 1 / frames_per_char:
                    computer_input_text += current_word[len(computer_input_text):len(computer_input_text) + chars_to_type]
                    if computer_input_text == current_word:
                        computer_score += 1
                        current_word = random.choice(words)
                        computer_input_text = ""
                        player_input_text = ""

        # Add difficulty adjustment function
        def set_difficulty(level):
            global frames_per_char
            if level == 1:
                frames_per_char = 0.1  # Easy: 1 char per 50 frames
            elif level == 2:
                frames_per_char = 0.05  # Medium: 1 char per 20 frames
            elif level == 3:
                frames_per_char = 0.01  # Hard: 1 char per 10 frames
            else:
                frames_per_char = 0.005  # Default to medium if unknown level

        # Initialize difficulty level
        set_difficulty(computer_level)

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_input_text == current_word:
                            player_score += 1
                            current_word = random.choice(words)
                            computer_input_text = ""
                            player_input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        player_input_text = player_input_text[:-1]
                    else:
                        player_input_text += event.unicode

            screen.fill(WHITE)

            # Update background and bomb positions
            screen.blit(background, (0, 0))
            if game_over:
                bomb_x_pos = SCREEN_WIDTH / 2 - bomb_width / 2
                bomb_y_pos = SCREEN_HEIGHT / 2 - bomb_height / 2
            else:
                bomb_x_pos = SCREEN_WIDTH / 4 * 3
                bomb_y_pos = SCREEN_HEIGHT - 360
                if player_score > computer_score:
                    bomb_x_pos = SCREEN_WIDTH / 4 * 3
                    bomb_y_pos = SCREEN_HEIGHT - 360
                else:
                    bomb_x_pos = SCREEN_WIDTH / 7
                    bomb_y_pos = SCREEN_HEIGHT - 360
            screen.blit(bomb, (bomb_x_pos, bomb_y_pos))

            # Simulate computer typing
            computer_typing_simulation()

            # Draw current word
            word_surface = font.render(current_word, True, WHITE)
            screen.blit(word_surface, (SCREEN_WIDTH // 2 - word_surface.get_width() // 2, 50))

            # Draw input boxes
            pygame.draw.rect(screen, WHITE, player_input_box)
            pygame.draw.rect(screen, WHITE, computer_input_box)
            pygame.draw.rect(screen, BLACK, player_input_box, 2)
            pygame.draw.rect(screen, BLACK, computer_input_box, 2)

            # Draw input texts
            player_input_surface = player_font.render(player_input_text, True, BLACK)
            screen.blit(player_input_surface, (player_input_box.x + 5, player_input_box.y + 7))

            # Draw computer input text
            computer_input_surface = player_font.render(computer_input_text, True, BLACK)
            screen.blit(computer_input_surface, (computer_input_box.x + 5, computer_input_box.y + 7))

            # Draw scores
            player_score_surface = small_font.render(f"{player_score}", True, BLACK)
            screen.blit(player_score_surface, (100, 50))
            computer_score_surface = small_font.render(f"{computer_score}", True, BLACK)
            screen.blit(computer_score_surface, (SCREEN_WIDTH - 100, 50))

            # Timer and bomb logic
            elapsed_time = time.time() - timer_start
            remaining_time = TIMER_DURATION - elapsed_time
            timer_surface = small_font.render(f"{int(remaining_time)}", True, RED)
            screen.blit(timer_surface, (bomb_x_pos, bomb_y_pos))

            # Bomb display logic
            if remaining_time > 5:
                screen.blit(bomb, (bomb_x_pos, bomb_y_pos))
            else:
                # Bomb blinking logic
                blink = pygame.image.load('blink.jpeg')
                if int(remaining_time * 5) % 2 == 0:  # Blinks every half second
                    screen.blit(blink, (bomb_x_pos, bomb_y_pos))

            if remaining_time <= 0:
                game_over = True
                running = False

            # Reset input boxes if 1 second has passed since the word changed
            if next_word_time and time.time() - next_word_time >= 0.5:
                next_word_time = None

            pygame.display.flip()

        # Game over screen
        screen.blit(bomb2, (bomb_x_pos - 60, bomb_y_pos - 70))
        pygame.display.flip()
        pygame.time.wait(2000)

        #Game over screen2
        screen.fill(WHITE)
        game_over_surface = font.render("Game Over", True, BLACK)
        screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)

        pygame.quit()

# Create an instance of class `c` and call the `run` method
if __name__ == "__main__":
    game_instance = a()
    game_instance.run()
