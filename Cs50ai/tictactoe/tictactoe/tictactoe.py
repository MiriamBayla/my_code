"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    x_count = 0
    o_count = 0

# Count how many Xs and how many Os there are in the current board
    for row in board:
        for place in row:
            if place == X:
                x_count += 1
            elif place == O:
                o_count += 1

# If there are more Xs - make turn to O
    if x_count > o_count:
        return O

# Else (if there are more Os or same amount as Xs) - make turn to X
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = set()

    for i in range(3):
        for j in range(3):
            # If place is empty - it's an available option
            if board[i][j] == EMPTY:
                available_actions.add((i, j))
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # Define i and j as places in given action
    i, j = action

    # Raise an exception if action isn't valid
    if i < 0 or i > 2 or j < 0 or j > 2 or board[i][j] != EMPTY:
        raise Exception("Invalid Move.")

    # Make a deepcopy of the board
    temp_board = copy.deepcopy(board)

    # Add action to board
    temp_board[i][j] = player(board)

    # Return updated board after the move
    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check for winning row
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    # Check for winning column
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check for left to right diagonal winning
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]

    # Check for right to left diagonal winning
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # If game is in progress or there is draw - return none
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If someone has won or board is full - game is over
    if winner(board) is not None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    result = winner(board)
    # If X is the winner return 1
    if result == X:
        return 1
    # If O is the winner return -1
    elif result == O:
        return -1
    else:
        # If there is a tie or game in progress (no winner)
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If game is over - return None (for best move)
    if terminal(board):
        return None

    # When it's player Xs turn
    if player(board) == X:

        # Best_score will always be the greater option so for beginning comparison it needs to be low
        best_score = float('-inf')

        # Define set of possible actions
        possible_actions = actions(board)

        # Incase there is no best move - to not cause a prob
        best_move = None

        # For every possible action in the board
        for action in possible_actions:
            new_board = result(board, action)
            score = min_value(new_board)

            # Get the greatest low value and call it best_move
            if score > best_score:
                best_score = score
                best_move = action
        return best_move

    # When it's player Os turn
    else:
        best_score = float('inf')
        possible_actions = actions(board)

        # Incase there is no best move - to not cause a prob
        best_move = None

        for action in possible_actions:
            new_board = result(board, action)
            score = max_value(new_board)

            # Get the lowest great value and call it best_move
            if score < best_score:
                best_score = score
                best_move = action
        return best_move

# Calc max value (for X)


def max_value(board):

    # If the game is over - return the board score
    if terminal(board):
        return utility(board)

    # max_option will always be the greater option so for beginning comparison it needs to be low
    max_option = float('-inf')

    # Set of possible actions for X
    possible_actions = actions(board)

    # For each of Xs possible actions
    for action in possible_actions:

        # The new board after doing this action
        new_board = result(board, action)
        # Make max_action the greatest out of what O would choose (the lowest)
        max_option = max(max_option, min_value(new_board))

    return max_option


# Calc min value (for O)
def min_value(board):

    # If the game is over - return the board score
    if terminal(board):
        return utility(board)

    # max_option will always be the greater option so for beginning comparison it needs to be low
    min_option = float('inf')

    # Set of possible actions for O
    possible_actions = actions(board)

    # For each of Os possible actions
    for action in possible_actions:

        # The new board after doing this action
        new_board = result(board, action)
        # Make min_action the lowest out of what X would choose (the greatest)
        min_option = min(min_option, max_value(new_board))

    return min_option
