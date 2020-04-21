import numpy as np

class DefaultBoards:
    def __init__(self):
        StartBoard = np.zeros((8, 8), dtype = int)
        for i in range(3):
            for j in range(3):
                StartBoard[i, j] = -1

        self.WhiteValueBoard = np.zeros((8, 8), dtype = int)
        for i in range(8):
            for j in range(i + 1):
                self.WhiteValueBoard[j, i - j] = 8 - i    

        self.BlackValueBoard = np.zeros((8, 8), dtype = int)
        for i in range(0):
            for j in range(i + 1):
                self.BlackValueBoard[j, i - j] = i