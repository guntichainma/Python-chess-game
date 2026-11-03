import pygame
import sys

pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8

SQUARE_SIZE = WIDTH // COLS

# Colors
LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess Game")


def draw_board():
    """Draw the 8x8 chess board."""

    for row in range(ROWS):
        for col in range(COLS):

            if (row + col) % 2 == 0:
                color = LIGHT_SQUARE
            else:
                color = DARK_SQUARE

            pygame.draw.rect(
                screen,
                color,
                (
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ),
            )


def main():
    clock = pygame.time.Clock()
    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        draw_board()

        pygame.display.flip()

        # Limit game to 60 FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()