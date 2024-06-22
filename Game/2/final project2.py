import pygame
import random
import time
import os

class BombDefusalGame:
    def run(self):
        # Initialize pygame
        pygame.init()

        # Screen dimensions
        WIDTH, HEIGHT = 600, 600
        ROWS, COLS = 6, 6
        CIRCLE_RADIUS = 40
        GRID_OFFSET = 100  # Offset for the grid to prevent overlap with text

        # Colors
        BLUE = (0, 0, 255)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)

        # Font
        FONT = pygame.font.Font(None, 36)

        # Words list
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

        # Create screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bomb Defusal Game")

        # Load background image
        os.chdir('/Users/hyeonjuyeon/Desktop/2024-OOP-Project/2024-OOP-project/Game/2')
        background = pygame.image.load('background2.png')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))

        # Load player image
        player_image = pygame.image.load('player.png')  # Replace 'player.png' with your image file
        player_image = pygame.transform.scale(player_image, (CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2))

        # Load bomb image
        bomb_image = pygame.image.load('bomb.png')  # Replace 'bomb.png' with your image file
        bomb_image = pygame.transform.scale(bomb_image, (CIRCLE_RADIUS * 2.1, CIRCLE_RADIUS * 2.1))

        # Player starting position
        player_pos = [ROWS - 1, COLS - 1]

        # Bomb position
        def generate_bomb_position():
            while True:
                pos = [random.randint(0, ROWS - 1), random.randint(0, COLS - 1)]
                if pos != player_pos:
                    return pos

        bomb_pos = generate_bomb_position()

        # Defused bomb counter
        defused_bomb_count = 0

        # Timer
        start_time = time.time()
        time_limit = 60  # 60 seconds time limit

        # Function to draw grid
        def draw_grid():
            pass

        # Function to draw player
        def draw_player():
            screen.blit(player_image, (player_pos[1] * WIDTH // COLS + WIDTH // (COLS * 2) - CIRCLE_RADIUS, 
                                    player_pos[0] * (HEIGHT - GRID_OFFSET) // ROWS + (HEIGHT - GRID_OFFSET) // (ROWS * 2.1) + GRID_OFFSET - CIRCLE_RADIUS))

        # Function to draw bomb
        def draw_bomb():
            screen.blit(bomb_image, (bomb_pos[1] * WIDTH // COLS + WIDTH // (COLS * 2) - CIRCLE_RADIUS, 
                                    bomb_pos[0] * (HEIGHT - GRID_OFFSET) // ROWS + (HEIGHT - GRID_OFFSET) // (ROWS * 2.1) + GRID_OFFSET - CIRCLE_RADIUS))

        # Main game loop
        def main():
            nonlocal player_pos, bomb_pos, defused_bomb_count
            run = True
            word = random.choice(words)
            typed_word = ""
            move_allowed = False

            while run:
                screen.blit(background, (0, 0))
                draw_grid()
                draw_player()
                draw_bomb()
                
                # Display word
                word_surface = FONT.render(word, True, WHITE)
                screen.blit(word_surface, (WIDTH // 2 - word_surface.get_width() // 2, 10))
                
                # Display typed word
                typed_surface = FONT.render(typed_word, True, WHITE)
                screen.blit(typed_surface, (WIDTH // 2 - typed_surface.get_width() // 2, 50))

                # Display timer
                elapsed_time = time.time() - start_time
                remaining_time = max(0, time_limit - elapsed_time)
                timer_surface = FONT.render(f"Time: {int(remaining_time)}", True, WHITE)
                screen.blit(timer_surface, (10, 10))

                # Display defused bomb count
                bomb_count_surface = FONT.render(f"BOMB: {defused_bomb_count}", True, WHITE)
                screen.blit(bomb_count_surface, (WIDTH - 150, 10))
                
                # Check for time out
                if remaining_time == 0:
                    run = False
                    print("Time's up! You failed to defuse the bomb.")
                    break
                
                # Check for player reaching bomb
                if player_pos == bomb_pos:
                    defused_bomb_count += 1
                    bomb_pos = generate_bomb_position()
                    move_allowed = False  # Stop player movement until next word is typed correctly

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == pygame.KEYDOWN:
                        if move_allowed:
                            new_pos = player_pos[:]
                            if event.key == pygame.K_UP and player_pos[0] > 0:
                                new_pos[0] -= 1
                            elif event.key == pygame.K_DOWN and player_pos[0] < ROWS - 1:
                                new_pos[0] += 1
                            elif event.key == pygame.K_LEFT and player_pos[1] > 0:
                                new_pos[1] -= 1
                            elif event.key == pygame.K_RIGHT and player_pos[1] < COLS - 1:
                                new_pos[1] += 1
                            
                            if new_pos != player_pos:
                                player_pos = new_pos
                                move_allowed = False  # Require typing word again after each move

                        else:
                            if event.key == pygame.K_BACKSPACE:
                                typed_word = typed_word[:-1]
                            elif event.key == pygame.K_RETURN:
                                if typed_word.lower() == word.lower():
                                    move_allowed = True
                                    word = random.choice(words)
                                    typed_word = ""
                            else:
                                typed_word += event.unicode
                
                pygame.display.flip()
            
            # Game over screen
            screen.fill(WHITE)
            game_over_surface = FONT.render("Game Over", True, BLACK)
            screen.blit(game_over_surface, (WIDTH // 2 - game_over_surface.get_width() // 2, HEIGHT // 2 - game_over_surface.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            
        main()

# Create an instance of class `BombDefusalGame` and call the `run` method
if __name__ == "__main__":
    game_instance = BombDefusalGame()
    game_instance.run()