import numpy as np


class StartBoard1:
    def __init__(self):
        self.StartBoard = np.zeros((8, 8), dtype=int)
        for i in range(3):
            for j in range(3):
                self.StartBoard[i, j] = -1
        for i in range(5, 8):
            for j in range(5, 8):
                self.StartBoard[i, j] = 1

    @property
    def startboard(self):
        return self.StartBoard.copy()


class StartBoard2:
    def __init__(self):
        self.StartBoard = np.zeros((8, 8), dtype=int)

    @property
    def startboard(self):
        return self.StartBoard.copy()
