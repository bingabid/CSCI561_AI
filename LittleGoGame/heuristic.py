import numpy as np
from atari import Atari
from euler import EulerNumber
from read_write import ReadWrite

class Heuristic:
    # initializer
    def __init__(self, agent, curr_game_state, prev_game_state):
        self.agent = agent
        self.opponent = 3 - agent
        self.curr_game_state = curr_game_state
        self.prev_game_state = prev_game_state
        self.board_size = 5
        self.visited = np.zeros((self.board_size,self.board_size)).astype(int)

    # count difference of inner stones on the board
    def get_inner_stones(self):
        agent_stones, opponent_stones = 0, 0

        for i in range(1, self.board_size-1):
            for j in range(1, self.board_size-1):
                if self.curr_game_state[i,j] == self.agent:
                    agent_stones += 1
                elif self.curr_game_state[i,j] == self.opponent:
                    opponent_stones += 1
        return agent_stones - opponent_stones

    # count diffeence of edge stones
    def get_edge_stones(self):
        agent_edge_stones, opponent_edge_stones = 0, 0

        # count on first row
        for j in range(0, self.board_size):
            if self.curr_game_state[0, j] == self.agent:
                agent_edge_stones += 1
            elif self.curr_game_state[0, j] == self.opponent:
                opponent_edge_stones += 1
        # count on last row
        for j in range(0, self.board_size):
            if self.curr_game_state[self.board_size - 1, j] == self.agent:
                agent_edge_stones += 1
            elif self.curr_game_state[self.board_size - 1, j] == self.opponent:
                opponent_edge_stones += 1
        
        # count on fist column
        for i in range(1, self.board_size - 1) :
            if self.curr_game_state[i, 0] == self.agent:
                agent_edge_stones += 1
            elif self.curr_game_state[i, 0] == self.opponent:
                opponent_edge_stones += 1
        # count of last column
        for i in range(1, self.board_size - 1) :
            if self.curr_game_state[i, self.board_size - 1] == self.agent:
                agent_edge_stones += 1
            elif self.curr_game_state[i, self.board_size - 1] == self.opponent:
                opponent_edge_stones += 1

        return agent_edge_stones - opponent_edge_stones

    # get euler number
    def get_euler_number(self):
        #print("agent euler:", self.agent)
        agent_euler = EulerNumber(self.agent, self.curr_game_state)
        agent_eulerNumber = agent_euler.get_euler_number()

        #print("opponent euler:", self.opponent)
        opponent_euler = EulerNumber(self.opponent, self.curr_game_state)
        opponent_eulerNumber = opponent_euler.get_euler_number()

        return agent_eulerNumber - opponent_eulerNumber

    # count liberty of a point represented by [row, col]
    def count_liberty(self, row, col):
        liberty = 0
        if row>0 and self.curr_game_state[row - 1, col] == 0:
            liberty += 1
        if row<4 and self.curr_game_state[row + 1, col] == 0:
            liberty += 1
        if col>0 and self.curr_game_state[row, col - 1] == 0:
            liberty += 1
        if col<4 and self.curr_game_state[row, col + 1] == 0:
            liberty += 1

        return liberty

    # count liberty of stones
    def get_liberty(self):
        agent_liberty, opponent_liberty = 0, 0
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.curr_game_state[i,j] == self.agent:
                    agent_liberty += self.count_liberty(i, j)
                elif self.curr_game_state[i, j] == self.opponent:
                    opponent_liberty += self.count_liberty(i, j)
        liberty = agent_liberty - opponent_liberty
        # print(liberty)
        return liberty

    def count_atari(self):
        agent_atari = Atari(self.agent, self.curr_game_state, self.prev_game_state)
        agent_atari_count = agent_atari.count_atari_dfs()
        # print("agent_atari: ", self.agent, "-->", agent_atari_count)
        opponent_atari = Atari(self.opponent, self.curr_game_state, self.prev_game_state)
        opponent_atari_count = opponent_atari.count_atari_dfs()
        # print("opponent_atari: ", self.opponent, "-->", opponent_atari_count)
        atari = agent_atari_count - opponent_atari_count
        # print("(agent_atari - opponent_atari):", atari)
        return atari

    # evaluation/heuristic function
    def heuristic_evaluation(self):
        inner_stones = self.get_inner_stones()
        edge_stones = self.get_edge_stones()

        # stones = 1.4*inner_stones + 0.6*edge_stones
        liberty = min(max(self.get_liberty(), -4),4)
        atari = self.count_atari()
        euler_number = self.get_euler_number()

        # evalue = (-4.0*euler_number) + (4.7*stones) + (1.0*liberty) + (-0.5*atari)
        evalue = (-4.0*euler_number) + (6.5*inner_stones) + (1.6*edge_stones) + (1.1*liberty) + (-0.5*atari)
        return evalue

if __name__ == "__main__":
    readWrite = ReadWrite("heuristicInput.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    # print(agent)
    # print(prev_game_state)
    # print(curr_game_state)
    heuristic = Heuristic(agent, curr_game_state, prev_game_state)
    evalue = heuristic.heuristic_evaluation()
    print(evalue)