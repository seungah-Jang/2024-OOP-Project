import pygame
import random
import time
import os

class TypingGame:
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
        os.chdir('/Users/hyeonjuyeon/Downloads/python/3')
        self.background = pygame.image.load('background3.png')
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Cut image
        self.cut = pygame.image.load('cut.png')
        self.cut = pygame.transform.scale(self.cut, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Font
        self.font = pygame.font.Font(None, 74)
        self.player_font = pygame.font.Font(None, 30)
        self.small_font = pygame.font.Font(None, 80)

        # Code parts list
        self.code_front = ["print(", "for i in range(", "if x > ", "while "]
        self.code_back = ["'hello world')", "10): print(i)", "5: print('x is greater than 5')", "True: print('loop')"]

        # Shuffle the back parts of the code but keep the indices consistent
        self.shuffled_indices, self.shuffled_code_back = self.create_shuffled_code_lists()

        # Game variables
        self.player_score = 0
        self.current_step = 0
        self.player_input_text1 = ""
        self.player_input_text2 = ""
        self.game_over = False
        self.timer_start = time.time()
        self.TIMER_DURATION = 60  # seconds for the bomb timer
        self.input_box1 = pygame.Rect(230, self.SCREEN_HEIGHT - 100, 300, 32)
        self.input_box2 = pygame.Rect(230, self.SCREEN_HEIGHT - 50, 300, 32)
        self.active_box = self.input_box1  # Start with input_box1 as active

    def create_shuffled_code_lists(self):
        shuffled_indices = list(range(len(self.code_back)))
        random.shuffle(shuffled_indices)
        shuffled_code_back = [self.code_back[i] for i in shuffled_indices]
        return shuffled_indices, shuffled_code_back

    def check_code(self, front, back):
        expected_code = self.code_front[self.current_step].strip() + self.code_back[self.current_step].strip()
        user_code = front.strip() + back.strip()
        return expected_code == user_code

    def display_cut_image(self):
        self.screen.blit(self.cut, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box1.collidepoint(event.pos):
                    self.active_box = self.input_box1
                elif self.input_box2.collidepoint(event.pos):
                    self.active_box = self.input_box2
                else:
                    self.active_box = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.active_box == self.input_box1:
                        self.active_box = self.input_box2
                    elif self.active_box == self.input_box2:
                        if self.check_code(self.player_input_text1, self.player_input_text2):
                            self.display_cut_image()
                            self.player_score += 1
                            self.current_step += 1
                            if self.current_step == 4:
                                self.player_input_text1 = ""
                                self.player_input_text2 = ""
                                self.current_step = 0
                                self.shuffled_indices, self.shuffled_code_back = self.create_shuffled_code_lists()
                            else:
                                self.player_input_text1 = ""
                                self.player_input_text2 = ""
                                self.active_box = self.input_box1
                        else:
                            self.game_over = True
                            return False
                elif event.key == pygame.K_BACKSPACE:
                    if self.active_box == self.input_box1:
                        self.player_input_text1 = self.player_input_text1[:-1]
                    elif self.active_box == self.input_box2:
                        self.player_input_text2 = self.player_input_text2[:-1]
                else:
                    if self.active_box == self.input_box1:
                        self.player_input_text1 += event.unicode
                    elif self.active_box == self.input_box2:
                        self.player_input_text2 += event.unicode
        return True

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        # Draw code parts
        for i, front in enumerate(self.code_front):
            back_index = self.shuffled_indices[i]
            back = self.code_back[back_index]
            front_surface = self.player_font.render(f"{i + 1}. {front}", True, self.BLACK)
            back_surface = self.player_font.render(f"{i + 1}. {back}", True, self.BLACK)
            self.screen.blit(front_surface, (50, 50 + i * 50))
            self.screen.blit(back_surface, (500, 50 + i * 50))

        # Draw input texts
        player_input_surface1 = self.player_font.render(self.player_input_text1, True, self.BLACK)
        self.screen.blit(player_input_surface1, (self.input_box1.x + 5, self.input_box1.y + 7))

        player_input_surface2 = self.player_font.render(self.player_input_text2, True, self.BLACK)
        self.screen.blit(player_input_surface2, (self.input_box2.x + 5, self.input_box2.y + 7))

        # Draw input boxes
        pygame.draw.rect(self.screen, self.BLACK, self.input_box1, 2)
        pygame.draw.rect(self.screen, self.BLACK, self.input_box2, 2)

        # Draw scores
        player_score_surface = self.small_font.render(f"{self.player_score}", True, self.BLACK)
        self.screen.blit(player_score_surface, (415, 365))

        # Timer and cut logic
        elapsed_time = time.time() - self.timer_start
        remaining_time = self.TIMER_DURATION - elapsed_time
        timer_surface = self.small_font.render(f"00:{int(remaining_time)}", True, self.RED)
        self.screen.blit(timer_surface, (330, 270))  # Adjust timer position

        if remaining_time <= 0:
            self.game_over = True

        pygame.display.flip()

    def run(self):
        # Main game loop
        running = True
        while running:
            if not self.handle_events():
                break
            self.draw()
            if self.game_over:
                break

        # Game over screen
        self.screen.fill(self.WHITE)
        game_over_surface = self.font.render("Game Over", True, self.RED)
        self.screen.blit(game_over_surface, (self.SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, self.SCREEN_HEIGHT // 2 - game_over_surface.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

        pygame.quit()

# Create an instance of class `TypingGame` and call the `run` method
if __name__ == "__main__":
    game_instance = TypingGame()
    game_instance.run()