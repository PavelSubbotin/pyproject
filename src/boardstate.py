import numpy as np
from typing import Optional, List
from queue import Queue
from itertools import product
from sys import exit
# from ai import PositionEvaluation


class BoardState:
    def __init__(self, board: np.ndarray, current_player: int = 1, rating=0):
        global help_
        self.board: np.ndarray = board
        self.current_player: int = current_player
        self.rating = rating
        self.WhiteInOtherHouse = 0
        self.WhiteInHouse = 9
        self.BlackInOtherHouse = 0
        self.BlackInHouse = 9
        # self.boards = PositionEvaluation()
        # self.rating = boards.get_value(self.bo)

    def __str__(self):
        result = self.board.__str__() + '\ncurrent_player: ' + str(self.current_player) + '\n'
        return result

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        new_board = BoardState(self.board.copy(), self.current_player, self.rating)
        new_board.WhiteInOtherHouse = self.WhiteInOtherHouse
        new_board.WhiteInHouse = self.WhiteInHouse
        new_board.BlackInOtherHouse = self.BlackInOtherHouse
        new_board.BlackInHouse = self.BlackInHouse
        return new_board

    def do_move(self, from_x, from_y, to_x, to_y, WhiteValueBoard, BlackValueBoard) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """
        from_x, from_y = from_y, from_x
        to_x, to_y = to_y, to_x
        if not self.board[from_x, from_y] == self.current_player:
            return None
        # print("Try to move from here:", from_x, from_y, self.board[from_x, from_y], "  to here:", to_x, to_y)
        # print(self.board[from_x, from_y], self.current_player)
        if not (to_x, to_y) in self.get_possible_moves(from_x, from_y):
            return None
        # invalid move
        # todo more validation here
        # from_x, from_y = from_y, from_x
        # to_x, to_y = to_y, to_x
        result = self.copy()
        result.move(from_x, from_y, to_x, to_y, WhiteValueBoard, BlackValueBoard)
        return result

    def get_possible_moves(self, x, y) -> List['BoardState']:
        if not self.board[x, y]:
            return []
        available_cells = set()
        q = Queue()
        q.put((x, y))
        while not q.empty():
            x_, y_ = q.get()
            for i, j in product(range(-2, 3, 2), range(-2, 3, 2)):
                to_x, to_y = x_ + i, y_ + j
                if not (0 <= to_x <= 7 and 0 <= to_y <= 7):
                    continue
                if self.board[to_x, to_y] or (to_x, to_y) in available_cells:
                    continue
                if not self.board[(to_x + x_) // 2, (to_y + y_) // 2]:
                    continue
                available_cells.add((to_x, to_y))
                q.put((to_x, to_y))

        for i, j in product(range(-1, 2), range(-1, 2)):
            to_x, to_y = x + i, y + j
            if 0 <= to_x <= 7 and 0 <= to_y <= 7 and not self.board[to_x, to_y]:
                available_cells.add((to_x, to_y))
        return list(available_cells)

    def get_possible_moves_(self) -> List['BoardState']:
        available_cells = set()
        q = Queue()
        for i, j in product(range(8), range(8)):
            if self.board[i, j] == self.current_player:
                q.put((i, j, i, j))
        while not q.empty():
            from_x_, from_y_, x_, y_ = q.get()
            for i, j in product(range(-2, 3, 2), range(-2, 3, 2)):
                to_x, to_y = x_ + i, y_ + j
                if not (0 <= to_x <= 7 and 0 <= to_y <= 7):
                    continue
                if self.board[to_x, to_y] or (from_x_, from_y_, to_x, to_y) in available_cells:
                    continue
                if not self.board[(to_x + x_) // 2, (to_y + y_) // 2]:
                    continue
                available_cells.add((from_x_, from_y_, to_x, to_y))
                q.put((from_x_, from_y_, to_x, to_y))
        for x, y in product(range(8), range(8)):
            if not self.board[x, y] == self.current_player:
                continue
            for i, j in product(range(-1, 2), range(-1, 2)):
                to_x, to_y = x + i, y + j
                if 0 <= to_x <= 7 and 0 <= to_y <= 7 and not self.board[to_x, to_y]:
                    available_cells.add((x, y, to_x, to_y))
        # exit()
        return list(available_cells)

    def update_houses(self, from_x, from_y, to_x, to_y):
        if self.current_player == 1:
            if from_x < 3 and from_y < 3:
                self.WhiteInOtherHouse -= 1
            if to_x < 3 and to_y < 3:
                self.WhiteInOtherHouse += 1
            if from_x > 4 and from_y > 4:
                self.WhiteInHouse -= 1
            if to_x > 4 and to_y > 4:
                self.WhiteInHouse += 1
        if self.current_player == -1:
            if from_x > 4 and from_y > 4:
                self.BlackInOtherHouse -= 1
            if to_x > 4 and to_y > 4:
                self.BlackInOtherHouse += 1
            if from_x < 3 and from_y < 3:
                self.BlackInHouse -= 1
            if to_x < 3 and to_y < 3:
                self.BlackInHouse += 1

    def move(self, from_x, from_y, to_x, to_y, WhiteValueBoard, BlackValueBoard):
        self.update_houses(from_x, from_y, to_x, to_y)
        if self.BlackInOtherHouse == 9:
            self.rating = -999999
        elif self.WhiteInOtherHouse == 9:
            self.rating = 999999
        self.board[to_x, to_y] = self.board[from_x, from_y]
        self.board[from_x, from_y] = 0
        self.rating -= WhiteValueBoard[from_x, from_y] if self.current_player == 1 else -BlackValueBoard[from_x, from_y]
        self.rating += WhiteValueBoard[to_x, to_y] if self.current_player == 1 else -BlackValueBoard[to_x, to_y]
        self.current_player *= -1

    @property
    def is_game_finished(self) -> bool:
        return True if self.WhiteInOtherHouse == 9 or self.BlackInOtherHouse == 9 else False

    @property
    def get_winner(self) -> Optional[int]:
        if self.WhiteInOtherHouse == 9:
            return 'White'
        return 'Black'

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)

        board[7, 0] = 1  # шашка первого игрока
        board[6, 1] = 2  # дамка первого игрока
        board[0, 1] = -1  # шашка противника

        return BoardState(board, 1)
