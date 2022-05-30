import numpy as np
from board import Board
from copy import deepcopy
from random import shuffle
from heuristic import Heuristic

class Alpha_Beta:
    # initialize 
    def __init__(self, agent, prev_game_state, curr_game_state):
        self.agent = agent
        self.opponent = 3 - self.agent
        self.prev_game_state = prev_game_state
        self.curr_game_state = curr_game_state
        self.board_size = 5

    # evaluating next move:
    def get_next_move(self):
        board = Board(self.agent, self.curr_game_state, self.prev_game_state)
        postion, initial_move = board.get_initial_move() 
        if initial_move == True:
            return postion[0], postion[1], False
        else:
            # heuristic = Heuristic(self.agent, self.curr_game_state, self.prev_game_state)
            # current_score = heuristic.heuristic_evaluation()
            location, dummy_score = self.maximize(board, 3, -12345, 12345)
            x, y = location[0], location[1]

            valid_moves = board.get_valid_moves()
            if len(valid_moves) == 0 or x < 0 or y<0:
                # print("dummy_score", dummy_score)
                # print(x, y)
                return 0,0,True
            # new_game_state = self.curr_game_state
            # new_game_state[x, y] = self.agent
            # expected = Heuristic(self.agent, new_game_state, self.curr_game_state)
            # expected_score = expected.heuristic_evaluation()
            # print(current_score)
            # print(expected_score)
            # if current_score > expected_score:
            #     return x, y, True
            return x, y, False

    def is_terminal_state(self, board: Board):
        agent_moves, opponent_moves = board.get_stones_on_board()
        if agent_moves + opponent_moves == 25:
            return True
        return False

    def maximize(self, board: Board, depth, alpha, beta):
        # if depth != 0:
        #     valid_moves = board.get_valid_moves()
        if self.is_terminal_state(board) or depth == 0 :
            huristic = Heuristic(board.agent, board.curr_game_state, board.prev_game_state)
            hueristic_score = huristic.heuristic_evaluation()
            return [-1,-1], hueristic_score
        
        max_value = -12345.0
        valid_moves = board.get_valid_moves()
        # print(board.agent)
        # print(valid_moves)
        #shuffle(valid_moves)
        best_stone_position = [-2,-2]
        copy_curr_game_state = deepcopy(board.curr_game_state)
        
        if len(valid_moves) != 0 :  #if valid move exists then play
            for valid_move in valid_moves:
                x, y = valid_move[0], valid_move[1]
                board.update_board(x, y)
                dead_stones, new_game_state = board.remove_dead_stones()
                new_board = Board(board.opponent, new_game_state, copy_curr_game_state)
                value = self.minimize(new_board, depth - 1, alpha, beta)[1]
                board.revert_board(x, y)
                if value > max_value:
                    max_value = value
                    best_stone_position[0], best_stone_position[1] = x, y
                if max_value >= beta:
                    print("maxi prunning")
                    return best_stone_position, value
                alpha = max(alpha, max_value)
        else:  #if valid move does not exists then pass
            new_board = Board(board.opponent, copy_curr_game_state, copy_curr_game_state)
            value = self.minimize(new_board, depth - 1, alpha, beta)[1]
            if value > max_value:
                max_value = value
            if max_value >= beta:
                print("maxi prunning for no valid move")
                return best_stone_position, value
            alpha = max(alpha, max_value)
        return best_stone_position, max_value

    def minimize(self, board: Board, depth, alpha, beta):
        # if depth != 0:
        #     valid_moves = board.get_valid_moves()
        if self.is_terminal_state(board) or depth == 0 :
            huristic = Heuristic(board.agent, board.curr_game_state, board.prev_game_state)
            hueristic_score = huristic.heuristic_evaluation()
            return [-1,-1], -hueristic_score

        min_value = 12345.0
        valid_moves = board.get_valid_moves()
        # print(board.agent)
        # print(valid_moves) 
        #shuffle(valid_moves)
        best_stone_position = [-3,-3]
        copy_curr_game_state = deepcopy(board.curr_game_state)
        if len(valid_moves) != 0 :
            for valid_move in valid_moves:
                x, y = valid_move[0], valid_move[1]
                board.update_board(x, y)
                dead_stones, new_game_state = board.remove_dead_stones()
                new_board = Board(board.opponent, new_game_state, copy_curr_game_state)
                value = self.maximize(new_board, depth - 1, alpha, beta)[1]
                board.revert_board(x, y)
                if value < min_value:
                    min_value = value
                    best_stone_position[0], best_stone_position[1] = x, y
                if min_value <= alpha:
                    print("mini prunning")
                    return best_stone_position, min_value
                beta = min(beta, min_value)
        else:
            new_board = Board(board.opponent, copy_curr_game_state, copy_curr_game_state)
            value = self.maximize(new_board, depth - 1, alpha, beta)[1]
            if value < min_value:
                min_value = value
            if min_value <= alpha:
                print("mini prunning no valid moves")
                return best_stone_position, min_value
            beta = min(beta, min_value)
        return best_stone_position, min_value