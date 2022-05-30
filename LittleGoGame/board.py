import random
from group import Group
from copy import deepcopy

class Board:

    # initialize board
    def __init__(self, agent, curr_game_state, prev_game_state):
        self.agent = agent
        self.opponent = 3 - self.agent
        self.board_size = 5
        self.curr_game_state = curr_game_state
        self.prev_game_state = prev_game_state

    # update current board
    def update_board(self, x, y):
        self.curr_game_state[x,y] = self.agent
    
    # revert current board state
    def revert_board(self, x, y):
        self.curr_game_state[x, y] = 0
    
    # get number of stones present in board of each player
    def get_stones_on_board(self):
        agent_stones, opponent_stones = [], []
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.curr_game_state[i][j] == self.agent:
                    agent_stones.append([i, j])
                elif self.curr_game_state[i][j] == self.opponent:
                    opponent_stones.append([i, j])
        return agent_stones, opponent_stones

    # if opponent is present in [[2,1],[2,3],[1,2],[1,3]] coordinate
    def check_opponent_optimal_location(self, optimal):
        for point in optimal:
            x, y = point[0], point[1]
            if self.curr_game_state[x, y] == self.opponent:
                return True
        return False

    # get minimum distance from optimal location to opponent stones
    def get_min_euclidian_distance_point(self, optimal, opponent_stone):
        pos, dist = [], 100
        x, y = opponent_stone[0], opponent_stone[1]
        for point in optimal:
            i, j = point[0], point[1]
            dx, dy = i - x, j - y
            if dx*dx + dy*dy < dist:
                dist = dx*dx + dy*dy
                pos = point
        
        return pos

    # get maximum distance from optimal location to opponent stones
    def get_max_euclidian_distance_point(self, optimal, opponent_stone):
        pos, dist = [], -100
        x, y = opponent_stone[0], opponent_stone[1]
        for point in optimal:
            i, j = point[0], point[1]
            dx, dy = i - x, j - y
            if dx*dx + dy*dy < dist:
                dist = dx*dx + dy*dy
                pos = point
        return pos

    # get list of free_optimal_point
    def get_free_optimal_point(self, optimal):
        free_optimal_point = []
        for point in optimal:
            x, y = point[0], point[1]
            if self.curr_game_state[x, y] == 0:
                free_optimal_point.append(point)
        return free_optimal_point

    # checking initial game strategy:
    def get_initial_move(self):
        best = [2,2]
        optimal = [[2,1],[2,3],[1,2],[3,2]]
        agent_stones, opponent_stones = self.get_stones_on_board()
        len_agent_stones, len_opponent_stones = len(agent_stones), len(opponent_stones)
        total_stones = len_agent_stones + len_opponent_stones
        if total_stones == 0:
            return best, True
        elif total_stones == 1:
            if self.curr_game_state[2][2] == 0:
                return best, True
            else:
                pos = random.choice(optimal)
                return pos, True
        elif total_stones == 2:
            free_optimal_point = self.get_free_optimal_point(optimal)
            if len_agent_stones == 2 or len_opponent_stones == 2:
                if self.curr_game_state[2,2] == 0:
                    return best, True
                else:
                    pos = random.choice(free_optimal_point)
                    return pos, True
            else:
                if self.curr_game_state[2][2] == 0: # center piece is empty
                    return best, True
                elif self.curr_game_state[2, 2] == self.opponent:
                    pos = random.choice(free_optimal_point)
                    return pos, True
                elif self.check_opponent_optimal_location(optimal): # my opponent is optimal position
                    opponent_point = opponent_stones[0]
                    x, y = opponent_point[0], opponent_point[1]
                    if self.curr_game_state[2, 1] == self.opponent or self.curr_game_state[2, 3] == self.opponent:
                        pos = random.choice([[1, 2],[3,2]])
                        return pos, True
                    else:
                        pos = random.choice([[2, 1],[2, 3]])
                        return pos, True
                else: # my opponent is not in optimal position
                    pos = self.get_min_euclidian_distance_point(optimal, opponent_stones[0])
                    #pos = self.get_max_euclidian_distance_point(optimal, opponent_stones[0])
                    return pos, True
        elif total_stones == 3:
            if len_opponent_stones == 3:
                pass
            elif len_agent_stones == 3:
                traingle_stones = []
                for point in optimal:
                    if point not in agent_stones:
                        traingle_stones.append(point)
                if len(traingle_stones) == 1:
                    pos = traingle_stones[0]
                    return pos, True
                elif self.curr_game_state[2][2] == 0:
                    return best, True
                else:
                    pos = random.choice(traingle_stones)
                    return pos, True
            else: # len_agent_stones == 2 or len_opponent_stones == 2:
                if self.curr_game_state[2][2] == 0:
                    return best, True
                else:
                    free_optimal_point = self.get_free_optimal_point(optimal)
                    pos = random.choice(free_optimal_point)
                    return pos, True

        return [0,0], False

    # get the liberty of the stone position
    def check_stone_liberty(self, x, y):
        group = Group(self.agent, self.curr_game_state)
        allies = group.get_allies_dfs(x, y)
        return group.check_liberty(allies)

    # get the liberty of opponent stone position
    def check_opponent_stone_liberty(self, x, y):
        group = Group(self.opponent, self.curr_game_state)
        allies = group.get_allies_dfs(x, y)
        return group.check_liberty(allies)
    
    # get list of dead_stones
    def get_dead_stones(self):
        dead_stones = []
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                if  self.curr_game_state[x, y] == self.opponent and self.check_opponent_stone_liberty(x, y) == False :
                    dead_stones.append([x, y])
        return dead_stones
            
    # remove dead stones from board
    def remove_dead_stones(self):
        dead_stones = self.get_dead_stones()
        new_game_state = deepcopy(self.curr_game_state)
        for stone in dead_stones:
            x , y = stone[0], stone[1]
            new_game_state[x, y] = 0
        return dead_stones, new_game_state

    #compare new_game_state with prev_game_state for KO rule
    def compare_game_state_for_KO(self, new_game_state):
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.prev_game_state[i][j] != new_game_state[i][j]:
                    return False
        return True

    # check for KO rule
    def check_ko_move(self, x, y):
        dead_stones, new_game_state = self.remove_dead_stones()
        if len(dead_stones) != 0 and self.compare_game_state_for_KO(new_game_state) == False:
            return True
        return False
    
    # get all the valid moves of given board
    def get_valid_moves(self):
        valid_moves = []
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.curr_game_state[i][j] == 0:
                    self.curr_game_state[i][j] = self.agent
                    if self.check_stone_liberty(i, j) == True:
                        valid_moves.append([i, j])
                    elif self.check_ko_move(i, j) == True: # liberty is 0 and capture and not ko move
                        valid_moves.append([i, j])
                    self.curr_game_state[i][j] = 0
        return valid_moves
