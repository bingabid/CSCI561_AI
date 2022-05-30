import numpy as np
from group import Group
from capture import Capture
from read_write import ReadWrite

class Atari:
    # initialize
    def __init__(self, agent, curr_game_state, prev_game_state):
        self.agent = agent
        self.opponent = 3 - agent
        self.curr_game_state = curr_game_state
        self.prev_game_state = prev_game_state
        self.board_size = 5
        self.visited = np.zeros((self.board_size,self.board_size)).astype(int)

    def count_atari_dfs(self):
        atari = 0
        for i in range(0,self.board_size):
            for j in range(0,self.board_size):
                if self.visited[i,j] == 0 and self.curr_game_state[i,j] == self.agent:
                    group = Group(self.agent, self.curr_game_state)
                    allies = group.get_allies_dfs(i,j)
                    liberties = []
                    for ally in allies:
                        row, col = ally[0], ally[1]
                        # get list of liberties of point row, col
                        liberty = group.get_liberty(row, col)
                        for lib in liberty: # avoid duplicate liberty
                            if lib not in liberties:
                                liberties.append(lib)
                    # check whether current group has atari - liberty == 1 and opponent should capture my stone/stones
                    if len(liberties) == 1:
                        liberty = liberties[0]
                        x, y = liberty[0], liberty[1]
                        capture = Capture(self.opponent, x, y, self.curr_game_state, self.prev_game_state)
                        if capture.capture() == True:
                            # print(allies)
                            atari += len(allies)
        return atari

if __name__ == "__main__":
    readWrite = ReadWrite("atariInput.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    # print(agent)
    # print(prev_game_state)
    # print(curr_game_state)
    atari_agent = Atari(agent, curr_game_state, prev_game_state)
    count_atari_agent = atari_agent.count_atari_dfs()
    atari_opponent = Atari(3-agent, curr_game_state, prev_game_state)
    count_atari_opponent = atari_opponent.count_atari_dfs()
    print(count_atari_agent - count_atari_opponent)
    print("atari_agent:", count_atari_agent == 0)
    print("atari_opponent:", count_atari_opponent == 2)
    