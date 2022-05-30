import board as board
from alpha_beta import Alpha_Beta
from read_write import ReadWrite
if __name__ == '__main__':

    readWrite = ReadWrite("input.txt", "output.txt")
    agent, prev_game_state, curr_game_state = readWrite.readInputFromFile()
    alpha_beta = Alpha_Beta(agent, prev_game_state, curr_game_state)
    x, y, Pass = alpha_beta.get_next_move()
    readWrite.writeOutputToFile(x, y, Pass)