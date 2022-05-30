import numpy as np

class ReadWrite:

    def __init__(self, input, output):
        self.input = input
        self.output = output
        self.board_size = 5

    def readInputFromFile(self):
        prev, curr = [], []
        with open(self.input, 'r') as rf:
            player_type = int(rf.readline().strip('\n'))
            for i in range(0, self.board_size):
                data = [ int(char) for char in rf.readline().strip('\n')]
                prev.append(data)
            for i in range(0, self.board_size):
                data = [ int(char) for char in rf.readline().strip('\n')]
                curr.append(data)
        prev_state = np.asarray(prev,dtype=np.int32)
        curr_state = np.asarray(curr,dtype=np.int32)
        return player_type, prev_state, curr_state

    def writeOutputToFile(self, x, y, Pass=False):
        with open(self.output, 'w') as wf:
            if Pass is True:
                wf.write("PASS")
            else:
                move = str(x) + ',' + str(y)
                wf.write(move)