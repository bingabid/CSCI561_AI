import numpy as np
from copy import deepcopy
from read_write import ReadWrite

class EulerNumber:
    n1_pat = [
        np.array([[1, 0], [0, 0]]),
        np.array([[0, 1], [0, 0]]),
        np.array([[0, 0], [1, 0]]),
        np.array([[0, 0], [0, 1]]),
    ]
    n3_pat = [
        np.array([[1, 1], [1, 0]]),
        np.array([[1, 1], [0, 1]]),
        np.array([[1, 0], [1, 1]]),
        np.array([[0, 1], [1, 1]]),
    ]
    nd_pat = [
        np.array([[1, 0], 
                  [0, 1]]),
        np.array([[0, 1],
                  [1, 0]]),
    ]
    

    def __init__(self, agent, curr_game_state):
        self.agent = agent
        self.euler_curr_state = deepcopy(curr_game_state)
        self.board_size = 5
        # setting all points 0 except the agent stones
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.euler_curr_state[i,j] == self.agent:
                    self.euler_curr_state[i,j] = 1
                else:
                    self.euler_curr_state[i,j] = 0

    def get_euler_number(self):   
            n1_type, n3_type, nd_type = 0, 0, 0

            #count hole type
            for i in range(0, self.board_size):  # go over rows
                for j in range(0, self.board_size):  # go over colums
                    slice_window = self.euler_curr_state[i : i + 2, j : j + 2]
                    n1_type += self.find_n1_match( slice_window )
                    n3_type += self.find_n3_match( slice_window )
                    nd_type += self.find_nd_match( slice_window )

            #print("n1_type:", n1_type, "n3_type: ", n3_type, "nd_type: ", nd_type) 
            return (n1_type  - n3_type + 2*nd_type) / 4
        
    def find_n1_match(self, window):
        for slice in EulerNumber.n1_pat:
            if np.all(slice == window):
                return 1
        return 0
        
    def find_n3_match(self, window):
        for slice in EulerNumber.n3_pat:
            if np.all(slice == window):
                return 1
        return 0
    
    def find_nd_match(self, window):
        for slice in EulerNumber.nd_pat:
            if np.all(slice == window):
                return 1
        return 0

if __name__ == "__main__":
    readWrite = ReadWrite("eulerInput.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    # print(agent)
    # print(prev_game_state)
    # print(curr_game_state)
    euler_agent = EulerNumber(agent, curr_game_state)
    eulerNumber_agent = euler_agent.get_euler_number()

    euler_opponent = EulerNumber(3-agent, curr_game_state)
    eulerNumber_opponent = euler_opponent.get_euler_number()
    print("agent_euelr:", eulerNumber_agent)
    print("opponent_euler:", eulerNumber_opponent)
