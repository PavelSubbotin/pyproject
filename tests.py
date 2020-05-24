import numpy as np
import os
from src.boardstate import BoardState


class Tests:
    def __init__(self):
        self.tests = []
        ind = 1
        while os.path.exists('Tests/test' + str(ind) + '.txt'):
            fin = open('Tests/test' + str(ind) + '.txt', 'r')
            board = np.ndarray((8, 8), int)
            s = [fin.readline().split() for i in range(8)]
            cur_player = int(fin.readline())
            for i in range(8):
                for j in range(8):
                    board[i, j] = s[i][j]
            self.tests.append(BoardState(board, cur_player))
            print(self.tests[-1])
            fin.close()
            ind += 1

    def __getitem__(self, ind):
        ind = int(ind)
        if ind > len(self.tests):
            print('govno')
            return None
        return self.tests[ind - 1]

    def __len__(self):
        return len(self.tests)
