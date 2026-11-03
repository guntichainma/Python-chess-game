import pygame
import sys

pygame.init()

# =========================================================
# SETTINGS
# =========================================================

BOARD_SIZE = 800
PANEL_WIDTH = 300

WIDTH = BOARD_SIZE + PANEL_WIDTH
HEIGHT = BOARD_SIZE

ROWS = 8
COLS = 8

SQUARE_SIZE = BOARD_SIZE // 8

# =========================================================
# COLORS
# =========================================================

LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)

BACKGROUND = (38, 36, 33)
PANEL = (49, 46, 43)

TEXT_COLOR = (235, 235, 235)

SELECTED_COLOR = (246, 246, 105)
LAST_MOVE_COLOR = (205, 210, 106)

# =========================================================
# WINDOW
# =========================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

clock = pygame.time.Clock()

# =========================================================
# FONTS
# =========================================================

piece_font = pygame.font.SysFont("Arial Unicode MS", 72)
coordinate_font = pygame.font.SysFont("Arial", 16, bold=True)
title_font = pygame.font.SysFont("Arial", 30, bold=True)
normal_font = pygame.font.SysFont("Arial", 20)

# =========================================================
# PIECES
# =========================================================

pieces = {
    "black_king": "♚",
    "black_queen": "♛",
    "black_rook": "♜",
    "black_bishop": "♝",
    "black_knight": "♞",
    "black_pawn": "♟",

    "white_king": "♔",
    "white_queen": "♕",
    "white_rook": "♖",
    "white_bishop": "♗",
    "white_knight": "♘",
    "white_pawn": "♙",
}

# =========================================================
# STARTING BOARD
# =========================================================

board = [
    [
        "black_rook",
        "black_knight",
        "black_bishop",
        "black_queen",
        "black_king",
        "black_bishop",
        "black_knight",
        "black_rook",
    ],

    ["black_pawn"] * 8,

    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,

    ["white_pawn"] * 8,

    [
        "white_rook",
        "white_knight",
        "white_bishop",
        "white_queen",
        "white_king",
        "white_bishop",
        "white_knight",
        "white_rook",
    ],
]

selected_square = None
current_turn = "white"

# =========================================================
# DRAW BOARD
# =========================================================


def draw_board():

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

    draw_coordinates()


# =========================================================
# COORDINATES
# =========================================================


def draw_coordinates():

    files = "abcdefgh"

    for col in range(8):

        text = coordinate_font.render(
            files[col],
            True,
            DARK_SQUARE if col % 2 == 0 else LIGHT_SQUARE,
        )

        screen.blit(
            text,
            (
                col * SQUARE_SIZE + SQUARE_SIZE - 17,
                BOARD_SIZE - 20,
            ),
        )

    for row in range(8):

        number = str(8 - row)

        text = coordinate_font.render(
            number,
            True,
            DARK_SQUARE if row % 2 == 0 else LIGHT_SQUARE,
        )

        screen.blit(
            text,
            (
                5,
                row * SQUARE_SIZE + 4,
            ),
        )


# =========================================================
# DRAW PIECES
# =========================================================


def draw_pieces():

    for row in range(8):
        for col in range(8):

            piece = board[row][col]

            if piece is not None:

                symbol = pieces[piece]

                text = piece_font.render(
                    symbol,
                    True,
                    (20, 20, 20),
                )

                rect = text.get_rect(
                    center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )

                screen.blit(text, rect)


# =========================================================
# SELECTED SQUARE
# =========================================================


def draw_selected_square():

    if selected_square is None:
        return

    row, col = selected_square

    highlight = pygame.Surface(
        (SQUARE_SIZE, SQUARE_SIZE),
        pygame.SRCALPHA,
    )

    highlight.fill((255, 255, 0, 90))

    screen.blit(
        highlight,
        (
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
        ),
    )


# =========================================================
# SIDE PANEL
# =========================================================


def draw_panel():

    pygame.draw.rect(
        screen,
        PANEL,
        (
            BOARD_SIZE,
            0,
            PANEL_WIDTH,
            HEIGHT,
        ),
    )

    title = title_font.render(
        "PYTHON CHESS",
        True,
        TEXT_COLOR,
    )

    screen.blit(
        title,
        (
            BOARD_SIZE + 30,
            40,
        ),
    )

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (BOARD_SIZE + 30, 90),
        (WIDTH - 30, 90),
        2,
    )

    turn_text = normal_font.render(
        f"Turn: {current_turn.capitalize()}",
        True,
        TEXT_COLOR,
    )

    screen.blit(
        turn_text,
        (
            BOARD_SIZE + 30,
            120,
        ),
    )

    instruction = normal_font.render(
        "Click a piece to select",
        True,
        (180, 180, 180),
    )

    screen.blit(
        instruction,
        (
            BOARD_SIZE + 30,
            170,
        ),
    )


# =========================================================
# MOUSE
# =========================================================


def handle_click(position):

    global selected_square

    x, y = position

    # Ignore side panel
    if x >= BOARD_SIZE:
        return

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    piece = board[row][col]

    if piece is not None:

        piece_color = piece.split("_")[0]

        if piece_color == current_turn:
            selected_square = (row, col)


# =========================================================
# MAIN LOOP
# =========================================================


def main():

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    handle_click(event.pos)

        screen.fill(BACKGROUND)

        draw_board()

        draw_selected_square()

        draw_pieces()

        draw_panel()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()