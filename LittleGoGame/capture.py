import numpy as np
from group import Group
from copy import deepcopy
from read_write import ReadWrite

class Capture:
    
    # initiliazer
    def __init__(self, agent, row, col, curr_game_state, prev_game_state):
        self.agent = agent
        self.opponent = 3 - self.agent
        self.board_size = 5
        self.curr_game_state = deepcopy(curr_game_state)
        self.prev_game_state = deepcopy(prev_game_state)
        self.row = row
        self.col = col

     # check is point is on board
    def is_on_board(self, x, y):
        return (x % self.board_size == x) and (y % self.board_size == y)

    # get location of immediate neighbors which are opponent stones
    def get_opponent_neighbors(self, new_game_state, x, y):
        potential_neighbors = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
        neighbors = []
        for point in potential_neighbors:
            i, j = point[0], point[1]
            if self.is_on_board(i, j) and self.curr_game_state[i][j] == self.opponent:
                neighbors.append(point)
        return neighbors

    # get dead stone of opponent
    def get_dead_stones(self, new_game_state, x, y):
        potentian_capture = self.get_opponent_neighbors(new_game_state, x, y)
        group = Group(self.opponent, new_game_state)
        dead_stones = []
        for point in potentian_capture:
            i, j = point[0], point[1]
            allies = group.get_allies_dfs(i, j)
            if group.check_liberty(allies) == False:
                # capture all stones in allies
                for ally in allies:
                    if ally not in dead_stones:
                        dead_stones.append(ally)
        return dead_stones

    # removes all dead stones
    def remove_dead_stone(self, new_game_state, x, y):
        dead_stones = self.get_dead_stones(new_game_state, x, y)
        new_state_to_remove_dead_stones = deepcopy(new_game_state)
        for stone in dead_stones:
            x, y = stone[0], stone[1]
            new_state_to_remove_dead_stones[x][y] = 0
        return dead_stones, new_state_to_remove_dead_stones

    # compare previous board and new board for ko test
    def compare_board(self, new_game_state_after_remove):
        for i in range(0,self.board_size):
            for j in range(0, self.board_size):
                if self.prev_game_state[i,j] != new_game_state_after_remove[i][j]:
                    # print(i, j)
                    return False
        return True

    # check if capturing a stone of opponent
    def capture(self):
        new_board = deepcopy(self.curr_game_state)
        new_board[self.row, self.col] = self.agent # placing agent to find opponent dead stones
        dead_stones, new_game_state_after_remove = self.remove_dead_stone(new_board, self.row, self.col)
        if len(dead_stones) == 0: # not capture despite having probable invalid moves
            return False
        #create object of type Group to get the allies
        group = Group(self.agent, new_board)
        allies = group.get_allies_dfs(self.row, self.col)
        liberties = set()  # store liberties of group
        for ally in allies:
            x, y = ally[0], ally[1]
            liberty = group.get_liberty(x, y)
            for point in liberty:
                liberties.add( (point[0], point[1]) )
        # print(len(liberties))
        # print(self.compare_board(new_game_state_after_remove))
        if len(liberties) == 0 and self.compare_board(new_game_state_after_remove) == True: # test ko by comparing board
            return False
        return True

if __name__ == "__main__":
    readWrite = ReadWrite("captureInput.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    # print(agent)
    # print(prev_game_state)
    # print(curr_game_state)
    capture = Capture(agent, 2, 1, curr_game_state, prev_game_state)
    print(capture.capture())
