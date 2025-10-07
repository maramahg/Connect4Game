
import numpy as np  # For array handling and numerical operations
import pygame  # For game graphics and window handling
import sys  # For system-level functions like exiting the game
import math  # Provides mathematical functions
import random  # For generating random moves or selections
import time  # For managing delays and timing

COLORS = {  # Dictionary storing color names and their RGB values
    "red": (255, 0, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (100, 180, 255),
    "purple": (160, 32, 240)
}
COLOR_NAMES = list(COLORS.keys())  # Dictionary storing color names and their RGB values

def show_title_screen(screen, font):  # Define a function
    screen.fill(BLACK)
    title = font.render("Welcome to Connect 4 AI", True, YELLOW)
    instr = font.render("Press SPACE to continue", True, WHITE)
    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - 60))
    screen.blit(instr, (width // 2 - instr.get_width() // 2, height // 2))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def text_input(screen, font, prompt):  # Define a function
    input_str = ""
    entering = True
    while entering:
        screen.fill(BLACK)
        label = font.render(prompt + input_str, True, WHITE)
        screen.blit(label, (50, height // 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.unicode.isprintable():
                    input_str += event.unicode
    return input_str.strip()

def choose_color(screen, font):  # Define a function
    index = 0
    while True:
        screen.fill(BLACK)
        text = font.render("Use ← → to choose color, ENTER to select", True, WHITE)
        screen.blit(text, (50, 50))
        for i, color in enumerate(COLOR_NAMES):  # List of color names extracted from the COLORS dictionary
            box_color = COLORS[color]  # Dictionary storing color names and their RGB values
            x = 100 + i * 120
            y = height // 2
            pygame.draw.circle(screen, box_color, (x, y), 40)
            if i == index:
                pygame.draw.circle(screen, WHITE, (x, y), 45, 3)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    index = (index - 1) % len(COLOR_NAMES)  # List of color names extracted from the COLORS dictionary
                elif event.key == pygame.K_RIGHT:
                    index = (index + 1) % len(COLOR_NAMES)  # List of color names extracted from the COLORS dictionary
                elif event.key == pygame.K_RETURN:
                    return COLOR_NAMES[index]  # List of color names extracted from the COLORS dictionary


def show_color_confirmation(screen, font, player_color_name, player_color, ai_color_name, ai_color):  # Define a function
    screen.fill(BLACK)
    label = font.render(f"You chose {player_color_name.upper()}!", True, player_color)
    ai_msg = font.render(f"AI will be {ai_color_name.upper()}", True, ai_color)
    screen.blit(ai_msg, (width // 2 - ai_msg.get_width() // 2, height // 2))
    instr = font.render("Press SPACE to continue", True, WHITE)
    screen.blit(label, (width // 2 - label.get_width() // 2, height // 2 - 30))
    screen.blit(instr, (width // 2 - instr.get_width() // 2, height // 2 + 30))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

minimax_times = []
alphabeta_times = []

def create_board():  # Define a function
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):  # Define a function
    board[row][col] = piece

def is_valid_location(board, col):  # Define a function
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):  # Define a function
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):  # Define a function
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def get_valid_locations(board):  # Define a function
    return [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]

def score_position(board, piece):  # Define a function
    score = 0
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    score += center_array.count(piece) * 3
    return score

def is_terminal_node(board):  # Define a function
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizingPlayer):  # Define a function
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def alphabeta(board, depth, alpha, beta, maximizingPlayer):  # Define a function
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alphabeta(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alphabeta(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def draw_board(screen, board, player_color, ai_color):  # Define a function
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, player_color, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, ai_color, (int(c*SQUARESIZE + SQUARESIZE/2), height - int(r*SQUARESIZE + SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def display_timing_screen(screen, font, minimax_times, alphabeta_times):  # Define a function
    scroll_offset = 0
    line_height = 40
    max_visible = (height - 160) // line_height
    total_lines = len(minimax_times)
    clock = pygame.time.Clock()

    while True:
        screen.fill(BLACK)
        header = font.render("Round | Minimax (s) | Alpha-Beta (s)", True, YELLOW)
        screen.blit(header, (10, 40))

        for i in range(scroll_offset, min(scroll_offset + max_visible, total_lines)):
            row = font.render(f"{i+1:^6} | {minimax_times[i]:.5f}     | {alphabeta_times[i]:.5f}", True, RED)
            screen.blit(row, (10, 80 + (i - scroll_offset) * line_height))

        msg = font.render("Press SPACE to continue", True, WHITE)
        screen.blit(msg, (width // 2 - msg.get_width() // 2, height - 60))

        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_UP:
                    if scroll_offset > 0:
                        scroll_offset -= 1
                elif event.key == pygame.K_DOWN:
                    if scroll_offset + max_visible < total_lines:
                        scroll_offset += 1
    screen.fill(BLACK)
    header = font.render("Round | Minimax (s) | Alpha-Beta (s)", True, YELLOW)
    screen.blit(header, (10, 40))
    for i, (m, a) in enumerate(zip(minimax_times, alphabeta_times)):
        row = font.render(f"{i+1:^6} | {m:.5f}     | {a:.5f}", True, RED)
        screen.blit(row, (10, 80 + i * 40))
    msg = font.render("Press SPACE to continue", True, WHITE)
    screen.blit(msg, (width // 2 - msg.get_width() // 2, height - 60))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_scoreboard(screen, font, player_wins, ai_wins, nickname, player_color, ai_color):  # Define a function
    screen.fill(BLACK)
    title = font.render("Scoreboard", True, YELLOW)
    screen.blit(title, (width // 2 - title.get_width() // 2, 40))
    p_score = font.render(f"{nickname} Wins: {player_wins}", True, player_color)
    a_score = font.render(f"AI Wins: {ai_wins}", True, ai_color)
    screen.blit(p_score, (width // 2 - p_score.get_width() // 2, 100))
    screen.blit(a_score, (width // 2 - a_score.get_width() // 2, 160))
    msg = font.render("Press ENTER to play again", True, WHITE)
    screen.blit(msg, (width // 2 - msg.get_width() // 2, 260))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def game_loop(player_wins, ai_wins, nickname, player_color, ai_color):  # Define a function
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("monospace", 35)
    board = create_board()
    game_over = False
    turn = random.randint(PLAYER, AI)
    draw_board(screen, board, player_color, ai_color)
    minimax_times.clear()
    alphabeta_times.clear()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, player_color, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)
                        draw_board(screen, board, player_color, ai_color)
                        if winning_move(board, PLAYER_PIECE):
                            label = font.render(f"{nickname} Wins!", True, player_color)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            player_wins += 1
                            game_over = True
                        if not game_over and len(get_valid_locations(board)) == 0:
                            label = font.render("It's a tie!", True, WHITE)
                            screen.blit(label, (40, 10))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            game_over = True
                        turn = AI

        if turn == AI and not game_over:
            start = time.time()
            _ = minimax(board.copy(), 4, True)
            minimax_times.append(time.time() - start)
            start = time.time()
            col, _ = alphabeta(board.copy(), 4, -math.inf, math.inf, True)
            alphabeta_times.append(time.time() - start)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                draw_board(screen, board, player_color, ai_color)
                if winning_move(board, AI_PIECE):
                    label = font.render("AI Wins!", True, ai_color)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    ai_wins += 1
                    game_over = True
                if not game_over and len(get_valid_locations(board)) == 0:
                    label = font.render("It's a tie!", True, WHITE)
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    game_over = True
                turn = PLAYER

    display_timing_screen(screen, font, minimax_times, alphabeta_times)
    show_scoreboard(screen, font, player_wins, ai_wins, nickname, player_color, ai_color)
    game_loop(player_wins, ai_wins, nickname, player_color, ai_color)


def main():  # Define a function
    pygame.init()
    screen = pygame.display.set_mode(size)
    font = pygame.font.SysFont("monospace", 35)
    show_title_screen(screen, font)
    nickname = text_input(screen, font, "Enter your nickname: ")
    player_color_name = choose_color(screen, font)
    player_color = COLORS[player_color_name]  # Dictionary storing color names and their RGB values
    ai_color_name = random.choice([c for c in COLOR_NAMES if c != player_color_name])  # List of color names extracted from the COLORS dictionary
    ai_color = COLORS[ai_color_name]  # Dictionary storing color names and their RGB values
    show_color_confirmation(screen, font, player_color_name, player_color, ai_color_name, ai_color)
    game_loop(0, 0, nickname, player_color, ai_color)


if __name__ == "__main__":
    main()