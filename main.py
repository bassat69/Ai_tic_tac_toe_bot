import numpy as np
import pygame
import sys

pygame.init()

# Colors
white = (255, 255, 255)
grey = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Proportions and sizes
height = 300
width = 300
line_width = 15
board_rows = 3
board_cols = 3
square_size = width // board_cols
circle_radius = square_size // 3
circle_width = 15
cross_width = 25

# Initialize the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(black)

# Board initialization
board = np.zeros((board_rows, board_cols))

# Font initialization
font = pygame.font.SysFont(None, 48)


def draw_lines(color=white):
    for i in range(1, board_rows):
        pygame.draw.line(screen, color, (0, square_size * i), (width, square_size * i), line_width)
        pygame.draw.line(screen, color, (square_size * i, 0), (square_size * i, height), line_width)


def draw_fig(color=white):
    for i in range(board_rows):
        for j in range(board_cols):
            if board[i][j] == 1:
                pygame.draw.circle(screen, color,
                                   (int(j * square_size + square_size // 2), int(i * square_size + square_size // 2)),
                                   circle_radius, circle_width)
            elif board[i][j] == 2:
                pygame.draw.line(screen, color,
                                 (j * square_size + square_size // 4, i * square_size + square_size // 4),
                                 (j * square_size + 3 * square_size // 4, i * square_size + 3 * square_size // 4),
                                 cross_width)
                pygame.draw.line(screen, color,
                                 (j * square_size + square_size // 4, i * square_size + 3 * square_size // 4),
                                 (j * square_size + 3 * square_size // 4, i * square_size + square_size // 4),
                                 cross_width)


def mark_square(row, col, player):
    board[row][col] = player


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                return False
    return True


def check_win(player):
    for row in range(board_rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    for col in range(board_cols):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


def minimax(minimax_board, depth, is_maximizing):
    if check_win(2):  # Assuming AI is player 2
        return 1  # AI wins
    if check_win(1):  # Assuming Human is player 1
        return -1  # Human wins
    if is_board_full():
        return 0  # Draw

    if is_maximizing:
        best_score = -float('inf')
        for i in range(board_rows):
            for j in range(board_cols):
                if minimax_board[i][j] == 0:
                    minimax_board[i][j] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(board_rows):
            for j in range(board_cols):
                if minimax_board[i][j] == 0:
                    minimax_board[i][j] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[i][j] = 0
                    best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -float('inf')
    move = None
    for i in range(board_rows):
        for j in range(board_cols):
            if board[i][j] == 0:
                board[i][j] = 2
                score = minimax(board, 0, False)
                board[i][j] = 0
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def display_message(text, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)


# Main game loop
running = True
player = 1
game_over = False

draw_lines()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and player == 1 and not game_over:
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y
            clicked_row = mouseY // square_size
            clicked_col = mouseX // square_size

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    screen.fill(green)
                    display_message("Player 1 wins!", white)
                    game_over = True
                elif is_board_full():
                    screen.fill(grey)
                    display_message("It's a tie!", black)
                    game_over = True
                player = 2

    if player == 2 and not is_board_full() and not game_over:
        move = best_move()
        if move:
            mark_square(move[0], move[1], player)
            if check_win(player):
                screen.fill(red)
                display_message("The AI wins!", white)
                game_over = True
            elif is_board_full():
                screen.fill(grey)
                display_message("It's a tie!", black)
                game_over = True
            player = 1

    draw_fig()
    pygame.display.update()

pygame.quit()
sys.exit()
