import pygame
import random
import time
import os
from Parent import *

current_dir = os.path.dirname(__file__)


class Game2_Screen(Screen):
    def draw(self):
        self.screen.fill(WHITE)
        draw_text('Start Setting', font, BLACK, self.screen, 400, 300)
        pygame.display.update()

class Game2_Play:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 600, 600
        self.ROWS, self.COLS = 6, 6
        self.CIRCLE_RADIUS = 40
        self.GRID_OFFSET = 100  # Offset for the grid to prevent overlap with text

        # Colors
        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Font
        self.FONT = pygame.font.Font(None, 36)

        # Words list
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

        # Create screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Bomb Defusal Game")

        # Load background image
        Game2_back_dir = os.path.join(current_dir,'data','Game2_background2.png')
        self.background = pygame.image.load(Game2_back_dir)
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

        # Load player image
        Game2_player_dir = os.path.join(current_dir,'data','Game2_player.png')
        self.player_image = pygame.image.load(Game2_player_dir)  # Replace 'player.png' with your image file
        self.player_image = pygame.transform.scale(self.player_image, (self.CIRCLE_RADIUS * 2, self.CIRCLE_RADIUS * 2))

        # Load bomb image
        Game2_bomb_dir = os.path.join(current_dir,'data','Game2_bomb.png')
        self.bomb_image = pygame.image.load(Game2_bomb_dir)  # Replace 'bomb.png' with your image file
        self.bomb_image = pygame.transform.scale(self.bomb_image, (self.CIRCLE_RADIUS * 2.1, self.CIRCLE_RADIUS * 2.1))

        # Player starting position
        self.player_pos = [self.ROWS - 1, self.COLS - 1]

        # Bomb position
        self.bomb_pos = self.generate_bomb_position()

        # Defused bomb counter
        self.defused_bomb_count = 0

        # Timer
        self.start_time = time.time()
        self.time_limit = 60  # 60 seconds time limit

    def generate_bomb_position(self):
        while True:
            pos = [random.randint(0, self.ROWS - 1), random.randint(0, self.COLS - 1)]
            if pos != self.player_pos:
                return pos

    # Function to draw grid
    def draw_grid(self):
        pass

    # Function to draw player
    def draw_player(self):
        self.screen.blit(self.player_image, (self.player_pos[1] * self.WIDTH // self.COLS + self.WIDTH // (self.COLS * 2) - self.CIRCLE_RADIUS, 
                                    self.player_pos[0] * (self.HEIGHT - self.GRID_OFFSET) // self.ROWS + (self.HEIGHT - self.GRID_OFFSET) // (self.ROWS * 2.1) + self.GRID_OFFSET - self.CIRCLE_RADIUS))

    # Function to draw bomb
    def draw_bomb(self):
        self.screen.blit(self.bomb_image, (self.bomb_pos[1] * self.WIDTH // self.COLS + self.WIDTH // (self.COLS * 2) - self.CIRCLE_RADIUS, 
                                    self.bomb_pos[0] * (self.HEIGHT - self.GRID_OFFSET) // self.ROWS + (self.HEIGHT - self.GRID_OFFSET) // (self.ROWS * 2.1) + self.GRID_OFFSET - self.CIRCLE_RADIUS))

    def main(self):
        run = True
        word = random.choice(self.words)
        typed_word = ""
        move_allowed = False

        while run:
            self.screen.blit(self.background, (0, 0))
            self.draw_grid()
            self.draw_player()
            self.draw_bomb()
            
            # Display word
            word_surface = self.FONT.render(word, True, self.WHITE)
            self.screen.blit(word_surface, (self.WIDTH // 2 - word_surface.get_width() // 2, 10))
            
            # Display typed word
            typed_surface = self.FONT.render(typed_word, True, self.WHITE)
            self.screen.blit(typed_surface, (self.WIDTH // 2 - typed_surface.get_width() // 2, 50))

            # Display timer
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.time_limit - elapsed_time)
            timer_surface = self.FONT.render(f"Time: {int(remaining_time)}", True, self.WHITE)
            self.screen.blit(timer_surface, (10, 10))

            # Display defused bomb count
            bomb_count_surface = self.FONT.render(f"BOMB: {self.defused_bomb_count}", True, self.WHITE)
            self.screen.blit(bomb_count_surface, (self.WIDTH - 150, 10))
            
            # Check for time out
            if remaining_time == 0:
                run = False
                print("Time's up! You failed to defuse the bomb.")
                break
            
            # Check for player reaching bomb
            if self.player_pos == self.bomb_pos:
                self.defused_bomb_count += 1
                self.bomb_pos = self.generate_bomb_position()
                move_allowed = False  # Stop player movement until next word is typed correctly

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if move_allowed:
                        new_pos = self.player_pos[:]
                        if event.key == pygame.K_UP and self.player_pos[0] > 0:
                            new_pos[0] -= 1
                        elif event.key == pygame.K_DOWN and self.player_pos[0] < self.ROWS - 1:
                            new_pos[0] += 1
                        elif event.key == pygame.K_LEFT and self.player_pos[1] > 0:
                            new_pos[1] -= 1
                        elif event.key == pygame.K_RIGHT and self.player_pos[1] < self.COLS - 1:
                            new_pos[1] += 1
                        
                        if new_pos != self.player_pos:
                            self.player_pos = new_pos
                            move_allowed = False  # Require typing word again after each move

                    else:
                        if event.key == pygame.K_BACKSPACE:
                            typed_word = typed_word[:-1]
                        elif event.key == pygame.K_RETURN:
                            if typed_word.lower() == word.lower():
                                move_allowed = True
                                word = random.choice(self.words)
                                typed_word = ""
                        else:
                            typed_word += event.unicode
            
            pygame.display.flip()
        
        # Game over screen
        self.screen.fill(self.WHITE)
        game_over_surface = self.FONT.render("Game Over", True, self.BLACK)
        self.screen.blit(game_over_surface, (self.WIDTH // 2 - game_over_surface.get_width() // 2, self.HEIGHT // 2 - game_over_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        

    def run(self):
        self.main()
        return "Game_main_screen"

# Create an instance of class `BombDefusalGame` and call the `run` method
if __name__ == "__main__":
    game_instance = Game2_Play()
    game_instance.run()