import numpy as np
from read_write import ReadWrite
# given a game state and point, this class will find allies
# given a point, this will return list of liberties of the point
class Group:
    #initialize the class
    def __init__(self, agent, curr_game_state):
        self.agent = agent
        self.opponent = 3 - self.agent
        self.curr_game_state = curr_game_state
        self.board_size = 5
        self.visited = np.zeros((self.board_size,self.board_size)).astype(int)

    # check is point is on board
    def is_on_board(self, x, y):
        return (x % self.board_size == x) and (y % self.board_size == y)

    # get valid neighbors( all neighbors of point on board) of a point [x, y]
    def get_valid_neighbors(self, x, y):
        neighbors = [[x+1, y], [x-1, y], [x, y+1], [x, y-1]]
        return [[point[0],point[1]] for point in neighbors if self.is_on_board(point[0],point[1])]
    
    # get neighbors ally of a stone
    def get_neighbors_ally(self, x, y):
        neighbors = self.get_valid_neighbors(x,y)
        neighbor_allies = []
        for point in neighbors:
            i, j = point[0], point[1]
            if self.curr_game_state[i][j] == self.curr_game_state[x][y]:
                neighbor_allies.append(point)
        return neighbor_allies

    # get allies of a given point uisng dfs
    def get_allies_dfs(self, x, y):
        stack = [[x,y]]
        allies = []
        while stack:
            stone = stack.pop()
            allies.append(stone)
            i, j = stone[0], stone[1]
            self.visited[i,j] = 1
            neighbors_allies = self.get_neighbors_ally(i,j)
            for ally in neighbors_allies:
                if ally not in stack and ally not in allies:
                    stack.append(ally)
        return allies

    # check liberty of allies - return boolen value
    def check_liberty(self, allies):
        for ally in allies:
            dx, dy = ally[0], ally[1]
            neighbors = self.get_valid_neighbors(dx,dy)
            for stone in neighbors:
                if self.curr_game_state[stone[0], stone[1]] == 0:
                    return True
        return False

    # get list of liberties of a point represented by [row, col]  - return list
    def get_liberty(self, x, y):
        liberties = []
        if x>0 and self.curr_game_state[x - 1, y] == 0:
            liberties.append([x - 1, y])
        if x<4 and self.curr_game_state[x + 1, y] == 0:
            liberties.append([x + 1, y])
        if y>0 and self.curr_game_state[x, y - 1] == 0:
            liberties.append([x, y - 1])
        if y<4 and self.curr_game_state[x, y + 1] == 0:
            liberties.append([x, y + 1])

        return liberties

if __name__ == "__main__":
    readWrite = ReadWrite("groupInput.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    # print(agent)
    # print(prev_game_state)
    # print(curr_game_state)
    group = Group(agent, curr_game_state)
    allies = group.get_allies_dfs(4,3)
    print(allies)