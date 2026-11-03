import pygame
import chess
import sys

pygame.init()

# =========================================================
# SETTINGS
# =========================================================

BOARD_SIZE = 800
PANEL_WIDTH = 300

WIDTH = BOARD_SIZE + PANEL_WIDTH
HEIGHT = BOARD_SIZE

SQUARE_SIZE = BOARD_SIZE // 8

# =========================================================
# COLORS
# =========================================================

LIGHT = (238, 238, 210)
DARK = (118, 150, 86)

PANEL = (49, 46, 43)
TEXT = (235, 235, 235)
SECONDARY_TEXT = (180, 180, 180)

SELECTED = (246, 246, 105, 130)
LAST_MOVE = (205, 210, 106, 130)

LEGAL_MOVE = (30, 30, 30, 100)

# =========================================================
# WINDOW
# =========================================================

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Arial", 30, bold=True)
normal_font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16, bold=True)

# =========================================================
# CHESS
# =========================================================

board = chess.Board()

selected_square = None
legal_moves = []
last_move = None

# =========================================================
# PIECE DRAWING
# =========================================================

# We'll use letters temporarily so V3 works on every Mac.
# PNG graphics will replace these next.

PIECE_LETTERS = {
    chess.PAWN: "P",
    chess.KNIGHT: "N",
    chess.BISHOP: "B",
    chess.ROOK: "R",
    chess.QUEEN: "Q",
    chess.KING: "K",
}

piece_font = pygame.font.SysFont("Arial", 46, bold=True)


# =========================================================
# CONVERSION
# =========================================================

def screen_to_chess(row, col):
    """Convert screen row/column into a python-chess square."""

    rank = 7 - row
    file = col

    return chess.square(file, rank)


def chess_to_screen(square):
    """Convert a python-chess square into screen row/column."""

    file = chess.square_file(square)
    rank = chess.square_rank(square)

    row = 7 - rank
    col = file

    return row, col


# =========================================================
# BOARD
# =========================================================

def draw_board():

    for row in range(8):
        for col in range(8):

            color = LIGHT if (row + col) % 2 == 0 else DARK

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

        color = DARK if col % 2 == 0 else LIGHT

        text = small_font.render(
            files[col],
            True,
            color,
        )

        screen.blit(
            text,
            (
                col * SQUARE_SIZE + 82,
                BOARD_SIZE - 20,
            ),
        )

    for row in range(8):

        color = DARK if row % 2 == 0 else LIGHT

        text = small_font.render(
            str(8 - row),
            True,
            color,
        )

        screen.blit(
            text,
            (
                5,
                row * SQUARE_SIZE + 5,
            ),
        )


# =========================================================
# HIGHLIGHT
# =========================================================

def highlight_square(square, color):

    row, col = chess_to_screen(square)

    surface = pygame.Surface(
        (SQUARE_SIZE, SQUARE_SIZE),
        pygame.SRCALPHA,
    )

    surface.fill(color)

    screen.blit(
        surface,
        (
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
        ),
    )


def draw_highlights():

    if last_move is not None:
        highlight_square(last_move.from_square, LAST_MOVE)
        highlight_square(last_move.to_square, LAST_MOVE)

    if selected_square is not None:
        highlight_square(selected_square, SELECTED)


# =========================================================
# LEGAL MOVE DOTS
# =========================================================

def draw_legal_moves():

    for move in legal_moves:

        row, col = chess_to_screen(move.to_square)

        center = (
            col * SQUARE_SIZE + SQUARE_SIZE // 2,
            row * SQUARE_SIZE + SQUARE_SIZE // 2,
        )

        target_piece = board.piece_at(move.to_square)

        if target_piece is None:

            pygame.draw.circle(
                screen,
                (50, 50, 50),
                center,
                12,
            )

        else:

            pygame.draw.circle(
                screen,
                (50, 50, 50),
                center,
                SQUARE_SIZE // 2 - 7,
                6,
            )


# =========================================================
# PIECES
# =========================================================

def draw_pieces():

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece is None:
            continue

        row, col = chess_to_screen(square)

        letter = PIECE_LETTERS[piece.piece_type]

        # White pieces = light circles
        # Black pieces = dark circles

        center = (
            col * SQUARE_SIZE + SQUARE_SIZE // 2,
            row * SQUARE_SIZE + SQUARE_SIZE // 2,
        )

        if piece.color == chess.WHITE:

            pygame.draw.circle(
                screen,
                (245, 245, 245),
                center,
                34,
            )

            pygame.draw.circle(
                screen,
                (40, 40, 40),
                center,
                34,
                3,
            )

            text_color = (30, 30, 30)

        else:

            pygame.draw.circle(
                screen,
                (45, 45, 45),
                center,
                34,
            )

            pygame.draw.circle(
                screen,
                (230, 230, 230),
                center,
                34,
                2,
            )

            text_color = (240, 240, 240)

        text = piece_font.render(
            letter,
            True,
            text_color,
        )

        rect = text.get_rect(center=center)

        screen.blit(text, rect)


# =========================================================
# PANEL
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
        TEXT,
    )

    screen.blit(
        title,
        (BOARD_SIZE + 30, 40),
    )

    pygame.draw.line(
        screen,
        (80, 80, 80),
        (BOARD_SIZE + 30, 95),
        (WIDTH - 30, 95),
        2,
    )

    turn = "White" if board.turn == chess.WHITE else "Black"

    turn_text = normal_font.render(
        f"Turn: {turn}",
        True,
        TEXT,
    )

    screen.blit(
        turn_text,
        (BOARD_SIZE + 30, 125),
    )

    # Game status

    if board.is_checkmate():

        winner = "Black" if board.turn == chess.WHITE else "White"

        status = f"Checkmate! {winner} wins"

    elif board.is_stalemate():

        status = "Stalemate"

    elif board.is_check():

        status = "CHECK!"

    else:

        status = "Game in progress"

    status_text = normal_font.render(
        status,
        True,
        SECONDARY_TEXT,
    )

    screen.blit(
        status_text,
        (BOARD_SIZE + 30, 170),
    )

    instructions = [
        "Click a piece",
        "Legal moves appear",
        "Click a dot to move",
        "",
        "R = Restart game",
    ]

    y = 240

    for line in instructions:

        text = normal_font.render(
            line,
            True,
            SECONDARY_TEXT,
        )

        screen.blit(
            text,
            (BOARD_SIZE + 30, y),
        )

        y += 35


# =========================================================
# SELECT PIECE
# =========================================================

def select_piece(square):

    global selected_square
    global legal_moves

    piece = board.piece_at(square)

    if piece is None:
        return

    if piece.color != board.turn:
        return

    selected_square = square

    legal_moves = [
        move
        for move in board.legal_moves
        if move.from_square == square
    ]


# =========================================================
# MOUSE
# =========================================================

def handle_click(position):

    global selected_square
    global legal_moves
    global last_move

    x, y = position

    if x >= BOARD_SIZE:
        return

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    clicked_square = screen_to_chess(row, col)

    # -----------------------------------------------------
    # Nothing currently selected
    # -----------------------------------------------------

    if selected_square is None:

        select_piece(clicked_square)
        return

    # -----------------------------------------------------
    # Try moving selected piece
    # -----------------------------------------------------

    matching_moves = [
        move
        for move in legal_moves
        if move.to_square == clicked_square
    ]

    if matching_moves:

        move = matching_moves[0]

        # Automatically promote pawns to queen for now
        if (
            board.piece_at(move.from_square).piece_type
            == chess.PAWN
        ):

            destination_rank = chess.square_rank(
                move.to_square
            )

            if destination_rank in (0, 7):

                move = chess.Move(
                    move.from_square,
                    move.to_square,
                    promotion=chess.QUEEN,
                )

        if move in board.legal_moves:

            board.push(move)

            last_move = move

            selected_square = None
            legal_moves = []

            return

    # -----------------------------------------------------
    # Select another piece
    # -----------------------------------------------------

    piece = board.piece_at(clicked_square)

    if piece is not None and piece.color == board.turn:

        select_piece(clicked_square)

    else:

        selected_square = None
        legal_moves = []


# =========================================================
# RESTART
# =========================================================

def restart_game():

    global selected_square
    global legal_moves
    global last_move

    board.reset()

    selected_square = None
    legal_moves = []
    last_move = None


# =========================================================
# MAIN
# =========================================================

def main():

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    handle_click(event.pos)

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    restart_game()

        draw_board()
        draw_highlights()
        draw_legal_moves()
        draw_pieces()
        draw_panel()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()