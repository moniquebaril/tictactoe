import random
from random import randint


board_in_play = [["-", "-", "-"],
                 ["-", "-", "-"],
                 ["-", "-", "-"]]


def print_board():
    for row in board_in_play:
        line = row[0] + " | " + row[1] + " | " + row[2]
        print(line)


def set_position(board, xy_pos, player):
    position_set = False
    while not position_set:
        if xy_pos == "":
            xy_pos = raw_input("Provide x, y position: ")
        try:
            xy_array = xy_pos.split(',')
            x = int(xy_array[0])
            y = int(xy_array[1])
            if x < 0 or x > 2 or y < 0 or y > 2:
                print "Invalid position"
            if board[y][x] != "-" and player != "-":
                print "Position already occupied"
            elif board[y][x] == "-" or player == "-":
                board[y][x] = player
                position_set = True
        except ValueError:
            print("That was not a valid position, please provide integers between 0 and 2 in the format x, y")
        if not player == humanPlayer:
            return


def board_is_full():
    for row in board_in_play:
        if "-" in row:
            return False
    return True


def winner(board, player):
    for row in board:
        if row == [player, player, player]:
            return True
    for col in range(0, 3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False


def empty_spots(board):
    empties = []
    for row in range(0, 3):
        for col in range(0, 3):
            if board[row][col] == "-":
                empties.append([row, col])
    return empties


def compute_next_move(board, player):
    available_positions = empty_spots(board)
    moves = []
    if winner(board, humanPlayer):
        return -1
    elif winner(board, computerPlayer):
        return 1
    elif len(available_positions) == 0:
        return 0
    for available_position in available_positions:
        new_board = [list(board[0]), list(board[1]), list(board[2])]
        set_position(new_board, str(available_position[1]) + "," + str(available_position[0]), player)
        if player == computerPlayer:
            result = compute_next_move(new_board, humanPlayer)
        else:
            result = compute_next_move(new_board, computerPlayer)
        if result == -1 or result == 0 or result == 1:
            moves.append([available_position, result])
        else:
            moves.append([available_position, result[1]])
    best_move = ""
    if player == computerPlayer:
        best_score = -2
        for currentMove in moves:
            if currentMove[1] > best_score:
                best_score = currentMove[1]
                best_move = currentMove[0]
    else:
        best_score = 2
        for currentMove in moves:
            if currentMove[1] < best_score:
                best_score = currentMove[1]
                best_move = currentMove[0]
    return [best_move, best_score]


def compute_next_random_move(board):
    available_positions = empty_spots(board)
    return available_positions[randint(0, len(available_positions) - 1)]


humanPlayer = raw_input("Do you want to be X or O? ").capitalize()
computerPlayer = "O"
while not humanPlayer == "X" and not humanPlayer == "O":
    humanPlayer = raw_input("Invalid input. Do you want to be X or O? ").capitalize()
if humanPlayer == "O":
    computerPlayer = "X"
ai = raw_input("Do you want to use the AI or Random algorithm? A for AI, R for Random: ").capitalize()
while not humanPlayer == "X" and not humanPlayer == "O":
    ai = raw_input("Invalid input. "
                   "Do you want to use the AI or Random algorithm? A for AI or R for Random: ").capitalize()
print_board()
computer_next = bool(random.getrandbits(1))
if computer_next:
    print("Computer goes first.")
else:
    print("You go first. Please provide integers between 0 and 2 in the format x, y")
while not board_is_full():
    if computer_next:
        print("Computer's turn...")
        if len(empty_spots(board_in_play)) == 9 or ai == "R":
            computer_move = compute_next_random_move(board_in_play)
        else:
            temp_board = [list(board_in_play[0]), list(board_in_play[1]), list(board_in_play[2])]
            next_move = compute_next_move(temp_board, computerPlayer)
            computer_move = next_move[0]
        set_position(board_in_play, str(computer_move[1]) + "," + str(computer_move[0]), computerPlayer)
        computer_next = False
    else:
        set_position(board_in_play, "", humanPlayer)
        computer_next = True
    print_board()
    if winner(board_in_play, humanPlayer):
        print("Winner Winner Chicken Dinner! You WIN! You beat me.")
        exit(0)
    if winner(board_in_play, computerPlayer):
        print("I WIN! MUHAHAHHAA...")
        exit(0)
    if board_is_full():
        break
print("Cat's Game! That was fun.")
