"""
board_util.py
Utility functions for Go board.
"""

import numpy as np
"""
Encoding of colors on and off a Go board.
FLODDFILL is used internally for a temporary marker
"""
EMPTY = 0
BLACK = 1
WHITE = 2
BORDER = 3

def is_black_white(color):
    return color == BLACK or color == WHITE
"""
Encoding of special pass move
"""
PASS = None

"""
Encoding of "not a real point", used as a marker
"""
NULLPOINT = 0

"""
The largest board we allow. 
To support larger boards the coordinate printing needs to be changed.
"""
MAXSIZE = 25

"""
where1d: Helper function for using np.where with 1-d arrays.
The result of np.where is a tuple which contains the indices 
of elements that fulfill the condition.
For 1-d arrays, this is a singleton tuple.
The [0] indexing is needed toextract the result from the singleton tuple.
"""
def where1d(condition):
    return np.where(condition)[0]

def coord_to_point(row, col, boardsize):
    """
    Transform two dimensional (row, col) representation to array index.

    Arguments
    ---------
    row, col: int
             coordinates of the point  1 <= row, col <= size

    Returns
    -------
    point
    
    Map (row, col) coordinates to array index
    Below is an example of numbering points on a 3x3 board.
    Spaces are added for illustration to separate board points 
    from BORDER points.
    There is a one point BORDER between consecutive rows (e.g. point 12).
    
    16   17 18 19   20

    12   13 14 15
    08   09 10 11
    04   05 06 07

    00   01 02 03

    File board_util.py defines the mapping of colors to integers,
    such as EMPTY = 0, BORDER = 3.
    For example, the empty 3x3 board is encoded like this:

    3  3  3  3  3
    3  0  0  0
    3  0  0  0
    3  0  0  0
    3  3  3  3

    This board is represented by the array
    [3,3,3,3,  3,0,0,0,  3,0,0,0,  3,0,0,0,  3,3,3,3,3]
    """
    assert 1 <= row
    assert row <= boardsize
    assert 1 <= col
    assert col <= boardsize
    NS = boardsize + 1
    return NS * row + col

class GoBoardUtil(object):
    
    @staticmethod
    def generate_legal_moves(board, color):
        """
        generate a list of all legal moves on the board.
        Does not include the Pass move.

        Arguments
        ---------
        board : np.array
            a SIZExSIZE array representing the board
        color : {'b','w'}
            the color to generate the move for.
        """
        moves = board.get_empty_points()
        legal_moves = []
        for move in moves:
            if board.is_legal(move, color):
                legal_moves.append(move)
        return legal_moves
    
    @staticmethod
    def generate_legal_moves_gomoku(board):
        """
        generate a list of all legal moves on the board for gomoku, where
        all empty positions are legal.
        """
        moves = board.get_empty_points()
        legal_moves = []
        for move in moves:
            legal_moves.append(move)
        return legal_moves
            
    @staticmethod
    def generate_random_move_gomoku(board):
        """
        Generate a random move for the game of Gomoku.
        """
        moves = board.get_empty_points()
        if len(moves) == 0:
            return PASS
        np.random.shuffle(moves)
        return moves[0]

    @staticmethod
    @staticmethod
    def generate_legal_moves_gomoku(board):
        """
        generate a list of all legal moves on the board for gomoku, where
        all empty positions are legal.
        """
        moves = board.get_empty_points()
        legal_moves = []
        for move in moves:
            legal_moves.append(move)
        return legal_moves
            
    @staticmethod
    def generate_random_move_gomoku(board):
        """
        Generate a random move for the game of Gomoku.
        """
        moves = board.get_empty_points()
        if len(moves) == 0:
            return PASS
        np.random.shuffle(moves)
        return moves[0]

    @staticmethod
    def generate_rule_move_gomoku(board, color):
        """
        Generate a  move for the game of Gomoku.
        """
        moves = board.get_empty_points()
        if len(moves) == 0:
            return PASS
        moveList = []
        # rule 1
        for move in moves:
            board.play_move_gomoku(move, color)
            win, winner = board.check_game_end_gomoku()
            board.undo(move)
            if win and winner == color:
                moveList.append(move)
        if len(moveList) != 0:
            return "Win", moveList

        # rule 2
        for move in moves:
            board.play_move_gomoku(move, WHITE+BLACK-color)
            win, winner = board.check_game_end_gomoku()
            board.undo(move)
            if win and winner == WHITE+BLACK-color:
                moveList.append(move)
        if len(moveList) != 0:
            return "BlockWin", moveList

        # rule 3
        for m in moves:
            board.play_move_gomoku(m, color)
            # new_moves = board.get_empty_points()
            # for move in new_moves:
            #     board.play_move_gomoku(move, color)
            #     win, winner = board.check_game_end_gomoku()
            #     board.undo(move)
            #     if win and winner == color:
            #         moveList.append(move)
            if board.point_check_openfour(m):
                moveList.append(m)
            board.undo(m)
        if len(moveList) != 0:
            return "OpenFour", moveList

        # rule 4
        for m in moves:
            board.play_move_gomoku(m, WHITE+BLACK-color)
            new_moves = board.get_empty_points()
            for move in new_moves:
                board.play_move_gomoku(move, WHITE+BLACK-color)
                win, winner = board.check_game_end_gomoku()
                board.undo(move)
                if win and winner == WHITE+BLACK-color:
                    moveList.append(move)
            # if board.point_check_openfour(m):
            #     moveList.append(m)
            board.undo(m)
        if len(moveList) != 0:
            moveList = np.unique(moveList)
            return "BlockOpenFour", moveList.tolist()

        # rule 5
        return "Random", moves


    @staticmethod       
    def generate_random_move(board, color, use_eye_filter):
        """
        Generate a random move.
        Return PASS if no move found

        Arguments
        ---------
        board : np.array
            a 1-d array representing the board
        color : BLACK, WHITE
            the color to generate the move for.
        """
        moves = board.get_empty_points()
        np.random.shuffle(moves)
        for move in moves:
            legal = not (use_eye_filter and board.is_eye(move, color)) \
                    and board.is_legal(move, color)
            if legal:
                return move
        return PASS

    @staticmethod
    def opponent(color):
        return WHITE+BLACK-color    

    @staticmethod
    def get_twoD_board(goboard):
        """
        Return: numpy array
        a two dimensional numpy array with the stones as the goboard.
        Does not pad with BORDER
        Rows 1..size of goboard are copied into rows 0..size - 1 of board2d
        """
        size = goboard.size
        board2d = np.zeros((size, size), dtype = np.int32)
        for row in range(size):
            start = goboard.row_start(row + 1)
            board2d[row, :] = goboard.board[start : start + size]
        return board2d

    @staticmethod
    def simulate_random(board, player_original_color):
        #input board is a temporary board
        
        #base case: when the game has ended
        is_end,victor = board.check_game_end_gomoku()
        #check who has won
        if is_end:
            if victor == player_original_color:
                return 2
            else:
                return 0
        #check if draw
        move = GoBoardUtil.generate_random_move_gomoku(board)
        if move == PASS:
            return 1
        board.play_move_gomoku(move,board.current_player)
        return GoBoardUtil.simulate_random(board,player_original_color)
    
    # @staticmethod
    # def simulate_rule_based(board, player_original_color):
    #     #input board is a temporary board
        
    #     #base case: when the game has ended
    #     is_end,victor = board.check_game_end_gomoku()
    #     #check who has won
    #     if is_end:
    #         if victor == player_original_color:
    #             return 2
    #         else:
    #             return 0
    #     #check if draw
    #     move = GoBoardUtil.generate_random_move_gomoku(board)
    #     if move == PASS:
    #         return 1
        
        
    #     rule, moves = GoBoardUtil.generate_rule_move_gomoku(board, player_original_color)
    #     if rule != "Random":
    #         return rule,np.random.shuffle(moves)[0]
    #     else:
    #         return "random",moves
