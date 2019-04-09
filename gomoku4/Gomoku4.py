#!/usr/bin/python3
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil
from simple_board import SimpleGoBoard
import numpy as np

class Gomoku():
      def __init__(self):
            """
            Gomoku player that selects moves randomly 
            from the set of legal moves.
            Passe/resigns only at the end of game.

            """
            self.name = "GomokuAssignment2"
            self.version = 1.0

      def get_move(self, board, color):
            return GoBoardUtil.generate_random_move_gomoku(board)

      def simulate_random(self,board,color):
            #get empty points from the board and simulate at random 10 times
            legal_moves = board.get_around_points()
            #win 2 score, draw 1 score, lose 0 score
            max_winrate = 0.0
            best_move = 0
            for move in legal_moves:
                  score = 0.0
                  for i in range(1):
                        temp_board = board.copy()
                        #play the first step
                        temp_board.play_move_gomoku(move,color)
                        #pass the board and the origianl color 
                        result = self.simulate_once(temp_board,color)
                        #add up the total score
                        
                        score+=result
                  
                  #find the winrate
                  score /= 10
                  if score>=max_winrate:
                        #evaluate if the winrate is higher than the current best move
                        max_winrate = score
                        best_move = move
            return best_move
            
      def simulate_rule_based(self,board,color):
            #####Fill in here#####
            temp_board = board.copy()
            rule,move = GoBoardUtil.generate_rule_move_gomoku(temp_board,color)
            if rule != "Random":
                  np.random.shuffle(move)
                  return rule,move[0]
                  # return move
            else:
                  move = self.simulate_random(board,color)
                  return "Random",move 
      
      def simulate_once(self,board,player_original_color):
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
            if move == None:
                  return 1
            
            #check the rules first
            temp_board = board.copy()
            rule,move = GoBoardUtil.generate_rule_move_gomoku(temp_board,board.current_player)
            if rule != "Random":
                  np.random.shuffle(move)
                  board.play_move_gomoku(move[0],board.current_player)
                  return self.simulate_once(board,player_original_color)  

            #if unable to generate a move based on the rule 
            #get random move from around all played points
            move = board.get_around_points()
            np.random.shuffle(move)
            board.play_move_gomoku(move[0],board.current_player)
            return self.simulate_once(board,player_original_color)

    
def run():
      """
      start the gtp connection and wait for commands.
      """
      #random.seed() no need to seed because we use np.random
      board = SimpleGoBoard(7)
      con = GtpConnection(Gomoku(), board)
      con.start_connection()

if __name__=='__main__':
      run() 
