"""
Tic Tac Toe Player
"""

import math

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

    if board == initial_state():
        return X #X starts 
    
    num_X = 0 # used to find number of X in a row
    num_O = 0 # used to find number of O in a row

    num_X = sum(row.count(X) for row in board)
    num_O = sum(row.count(O) for row in board)

    if num_X <= num_O:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set() # initializes a empty set

    if terminal(board):
        return set()
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: #checks if the cell is empty 
                possible_actions.add((i,j)) #if it is adds it to the set of actions since either x or o can be placed there

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i,j = action
    if not (0<=i<3 and 0<=j<3) or board[i][j] is not EMPTY:
        raise ValueError("Invalid move")
    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #There are 8 ways for either X or O to win otherwise the game the game goes or if there are no more empty cells there is no winner
    if board[0][0] == board[0][1] == board[0][2] != None:
        return board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != None:
        return board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != None:
        return board[2][0]
    elif board[0][0] == board[1][0] == board[2][0] != None:
        return board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != None:
        return board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != None:
        return board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] != None:
        return board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] != None:
        return board[2][0]
    else:
        return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True # there is a winner either X or O
    
    for row in board:
        if EMPTY in row:
            return False # The game is still going on as long as there are empty cells
        
    return True #No winner and all cells have been filled

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): #if the game is over 
        return None
    curr_ply = player(board)

    def max_val(board):
        """
        Returns the optimum option by predicting what is the best option for opponent and maximize that outcome
        """
        if terminal(board):
            return utility(board),None
        v = float('-inf')
        best_action = None
        for action in actions(board):
            min_v,_ = min_val(result(board,action))
            if min_v>v:
                v=min_v
                best_action = action 
        return v, best_action
    
    def min_val(board):
        """
        Returns the optimum option by predicting what is the best option for opponent and minimize that outcome
        """
        if terminal(board):
            return utility(board),None
        v = float('inf')
        best_action = None
        for action in actions(board):
            max_v,_ = max_val(result(board,action))
            if max_v < v:
                v = max_v
                best_action = action 
        return v, best_action 

        
    if curr_ply == X:
        _,best_action = max_val(board)
    else:
        _,best_action = min_val(board)
    
    return best_action
    
