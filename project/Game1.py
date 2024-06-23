import pygame
import random
import time
import os
from Parent import *

current_dir = os.path.dirname(__file__)

class Game1_Screen(Screen):
    def draw(self):
        self.screen.fill(WHITE)
        draw_text('Start Setting', font, BLACK, self.screen, 400, 300)
        pygame.display.update()


class Game1_Play:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Set up the display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Load background image
        Game1_back_dir = os.path.join(current_dir,'data','Game1_background.png')
        self.background = pygame.image.load(Game1_back_dir)
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Bomb image
        Game1_bomb_dir = os.path.join(current_dir,'data','Game1_bomb.png')
        self.bomb = pygame.image.load(Game1_bomb_dir)
        self.bomb_size = self.bomb.get_rect().size
        self.bomb_width = self.bomb_size[0]
        self.bomb_height = self.bomb_size[1]

        # Bomb2 image
        Game1_bomb2_dir = os.path.join(current_dir,'data','Game1_bomb2.png')
        self.bomb2 = pygame.image.load(Game1_bomb2_dir)
        self.bomb2 = pygame.transform.scale(self.bomb2, (int(self.bomb2.get_width() * 0.8), int(self.bomb2.get_height() * 0.8)))
        self.bomb2_size = self.bomb.get_rect().size
        self.bomb2_width = self.bomb2_size[0]
        self.bomb2_height = self.bomb2_size[1]

        # Font
        self.font = pygame.font.Font(None, 74)
        self.player_font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 36)

        # Word list
        self.words = ["Print", "import", "def", "return", "if", "elif",
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
        self.current_word = random.choice(self.words)
        self.player_score = 0
        self.computer_score = 0
        self.player_input_text = ""
        self.computer_input_text = ""
        self.game_over = False
        self.timer_start = time.time()
        self.TIMER_DURATION = 30  # seconds for the bomb timer
        self.computer_level = 3  # Computer level (1: easy, 2: medium, 3: hard)
        self.player_input_box = pygame.Rect(100, self.SCREEN_HEIGHT - 260, 140, 32)
        self.computer_input_box = pygame.Rect(self.SCREEN_WIDTH - 230, self.SCREEN_HEIGHT - 260, 140, 32)
        self.next_word_time = None  # To track the time when the word changes
        self.frames_per_char = 0.01  # Default value

    def computer_typing_simulation(self, frames_per_char=0.01):
        if self.next_word_time is None or time.time() - self.next_word_time > 1:  # Add delay between words
            self.next_word_time = time.time()
            chars_to_type = min(len(self.current_word) - len(self.computer_input_text), 1)  # Type one character at a time
            if frames_per_char <= 0:
                frames_per_char = 1  # Prevent division by zero

            if random.random() < 1 / frames_per_char:
                self.computer_input_text += self.current_word[len(self.computer_input_text):len(self.computer_input_text) + chars_to_type]
                if self.computer_input_text == self.current_word:
                    self.computer_score += 1
                    self.current_word = random.choice(self.words)
                    self.computer_input_text = ""
                    self.player_input_text = ""

    # Add difficulty adjustment function
    def set_difficulty(self, level):
        if level == 1:
            self.frames_per_char = 0.001  # Easy: 1 char per 50 frames
        elif level == 2:
            self.frames_per_char = 0.05  # Medium: 1 char per 20 frames
        elif level == 3:
            self.frames_per_char = 0.01  # Hard: 1 char per 10 frames
        else:
            self.frames_per_char = 0.005  # Default to medium if unknown level

    def run(self):
        # Initialize difficulty level
        self.set_difficulty(self.computer_level)

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_input_text == self.current_word:
                            self.player_score += 1
                            self.current_word = random.choice(self.words)
                            self.computer_input_text = ""
                            self.player_input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_input_text = self.player_input_text[:-1]
                    else:
                        self.player_input_text += event.unicode

            self.screen.fill(self.WHITE)

            # Update background and bomb positions
            self.screen.blit(self.background, (0, 0))
            if self.game_over:
                bomb_x_pos = self.SCREEN_WIDTH / 2 - self.bomb_width / 2
                bomb_y_pos = self.SCREEN_HEIGHT / 2 - self.bomb_height / 2
            else:
                if self.player_score > self.computer_score:
                    bomb_x_pos = self.SCREEN_WIDTH / 4 * 3
                    bomb_y_pos = self.SCREEN_HEIGHT - 360
                else:
                    bomb_x_pos = self.SCREEN_WIDTH / 7
                    bomb_y_pos = self.SCREEN_HEIGHT - 360

            # Simulate computer typing
            self.computer_typing_simulation()

            # Draw current word
            word_surface = self.font.render(self.current_word, True, self.WHITE)
            self.screen.blit(word_surface, (self.SCREEN_WIDTH // 2 - word_surface.get_width() // 2, 50))

            # Draw input boxes
            pygame.draw.rect(self.screen, self.WHITE, self.player_input_box)
            pygame.draw.rect(self.screen, self.WHITE, self.computer_input_box)
            pygame.draw.rect(self.screen, self.BLACK, self.player_input_box, 2)
            pygame.draw.rect(self.screen, self.BLACK, self.computer_input_box, 2)

            # Draw input texts
            player_input_surface = self.player_font.render(self.player_input_text, True, self.BLACK)
            self.screen.blit(player_input_surface, (self.player_input_box.x + 5, self.player_input_box.y + 7))

            # Draw computer input text
            computer_input_surface = self.player_font.render(self.computer_input_text, True, self.BLACK)
            self.screen.blit(computer_input_surface, (self.computer_input_box.x + 5, self.computer_input_box.y + 7))

            # Draw scores
            player_score_surface = self.small_font.render(f"{self.player_score}", True, self.BLACK)
            self.screen.blit(player_score_surface, (100, 50))
            computer_score_surface = self.small_font.render(f"{self.computer_score}", True, self.BLACK)
            self.screen.blit(computer_score_surface, (self.SCREEN_WIDTH - 100, 50))
            
            # Timer and bomb logic
            elapsed_time = time.time() - self.timer_start
            remaining_time = self.TIMER_DURATION - elapsed_time
            timer_surface = self.small_font.render(f"{int(remaining_time)}", True, self.RED)
            self.screen.blit(timer_surface, (bomb_x_pos, bomb_y_pos))

            # Bomb display logic
            if remaining_time > 5:
                self.screen.blit(self.bomb, (bomb_x_pos, bomb_y_pos))
            else:
                # Bomb blinking logic
                if int(remaining_time * 5) % 2 == 0:  # Blinks every half second
                    self.screen.blit(self.bomb, (bomb_x_pos, bomb_y_pos))
                else:
                    Game1_blink_dir = os.path.join(current_dir,'data','Game1_blink.jpeg')
                    blink = pygame.image.load(Game1_blink_dir)
                    self.screen.blit(blink, (bomb_x_pos, bomb_y_pos))

            if remaining_time <= 0:
                self.game_over = True
                running = False

            # Reset input boxes if 1 second has passed since the word changed
            if self.next_word_time and time.time() - self.next_word_time >= 0.5:
                self.next_word_time = None

            pygame.display.flip()

        # Game over screen
        self.screen.blit(self.bomb2, (bomb_x_pos - 60, bomb_y_pos - 70))
        pygame.display.flip()
        pygame.time.wait(2000)

        # Game over screen2
        self.screen.fill(self.WHITE)
        game_over_surface = self.font.render("Game Over", True, self.BLACK)
        
        self.screen.blit(game_over_surface, (self.SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, self.SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))
        

        pygame.display.flip()
        pygame.time.wait(1000)
        return "Game_main_screen"
        #pygame.quit()
if __name__ == "__main__":
    game_instance = Game1_Play()
    game_instance.run() 