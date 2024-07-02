import math
board = [' ' for _ in range(9)]
def display_board(board):
    for row in [board[i * 3:(i + 1) * 3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')
def is_valid_move(board, move):
    return board[move] == ' '
def make_move(board, move, player):
    board[move] = player
def check_win(board, player):
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  
                      (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                      (0, 4, 8), (2, 4, 6)]             
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)
def check_draw(board):
    return ' ' not in board
def minimax(board, depth, is_maximizing):
    if check_win(board, 'O'):
        return 1
    if check_win(board, 'X'):
        return -1
    if check_draw(board):
        return 0
    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if is_valid_move(board, i):
                board[i] = 'O'
                eval = minimax(board, depth + 1, False)
                board[i] = ' '
                max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if is_valid_move(board, i):
                board[i] = 'X'
                eval = minimax(board, depth + 1, True)
                board[i] = ' '
                min_eval = min(min_eval, eval)
        return min_eval
def ai_move(board):
    best_score = -math.inf
    best_move = None
    for i in range(9):
        if is_valid_move(board, i):
            board[i] = 'O'
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i
    make_move(board, best_move, 'O')
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    display_board(board)
    while True:
        move = int(input("Enter your move (0-8): "))
        if is_valid_move(board, move):
            make_move(board, move, 'X')
            if check_win(board, 'X'):
                display_board(board)
                print("You win!")
                break
            elif check_draw(board):
                display_board(board)
                print("It's a draw!")
                break
            ai_move(board)
            if check_win(board, 'O'):
                display_board(board)
                print("AI wins!")
                break
            elif check_draw(board):
                display_board(board)
                print("It's a draw!")
                break
        else:
            print("Invalid move. Try again.")
        display_board(board)
play_game()
