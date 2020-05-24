from typing import Optional

from .boardstate import BoardState

import numpy as np
from itertools import product
from sys import exit
import time


class PositionEvaluation:
    def __init__(self):
        self.WhiteValueBoard = np.ndarray((8, 8), int)
        self.WhiteValueBoard = np.ndappay([[20, 16, 12, 7, 5, 4, 2, 1],
                                          [16, 14, 12, 8, 6, 4.6, 4, 2],
                                          [12, 12, 11, 8, 7, 5.7, 2, 2.5],
                                          [7, 8, 8, 7, 6.5, 5.5, 3, 2.6],
                                          [5, 6, 7, 6.5, 6, 5, 3, 2.4],
                                          [4, 4.6, 5.7, 5.5, 5, 4, 4, 2],
                                          [2, 4, 3, 5, 3, 4, 3, 1],
                                          [1, 2, 2.5, 2.6, 2.4, 2, 1, 0]
                                          ])
        self.BlackValueBoard = self.WhiteValueBoard[::-1, ::-1].copy()

    def get_value(self, board) -> int:
        result = 0
        for i, j in product(range(0, 8), range(0, 8)):
            if not board[i, j]:
                continue
            if board[i, j] == 1:
                result += self.WhiteValueBoard[i, j]
            else:
                result -= self.BlackValueBoard[i, j]
        return result

    def update(self):
        for i, j in product(range(5, 8), range(5, 8)):
            self.WhiteValueBoard[i, j] -= 10 + 16 - i - j
        # не совсем понял вашу правку в данном месте, так как в развернутом массиве все равно придется менять значения
        # хочу отметить, что данные значения не обязаны быть равны, так как первый кейс уменьшений отвечает за то, чтобы
        #    бот не оставлял до последнего свои фишки на базе, а второй кейс уменьшений отвечает за то, чтобы бот стремился быстрее занять 
        #                                                                                        освободившиеся клетки на базе противника.
        
        self.WhiteValueBoard[7, 7] -= 10
        self.WhiteValueBoard[7, 6] -= 5
        self.WhiteValueBoard[6, 7] -= 5
        self.WhiteValueBoard[6, 6] -= 2
        for i, j in product(range(3), range(3)):
            self.BlackValueBoard[i, j] -= 10 + 16 - (8 - i) - (8 - j)
        self.BlackValueBoard[0, 0] -= 10
        self.BlackValueBoard[0, 1] -= 5
        self.BlackValueBoard[1, 0] -= 5
        self.BlackValueBoard[1, 1] -= 2

    def update_information(self, board):
        board.rating = self.get_value(board.board)
        WhiteInHouse, WhiteInOtherHouse, BlackInHouse, BlackInOtherHouse = 0, 0, 0, 0
        BlackInHouse = (board.board[0:3, 0:3] == -1).sum()
        WhiteInOtherHouse = (board.board[0:3, 0:3] == 1).sum()
        BlackInOtherHouse = (board.board[5:8, 5:8] == -1).sum()
        WhiteInHouse = (board.board[5:8, 5:8] == 1).sum()
        
        board.WhiteInOtherHouse = WhiteInOtherHouse
        board.BlackInOtherHouse = BlackInOtherHouse
        board.WhiteInHouse = WhiteInHouse
        board.BlackInHouse = BlackInHouse


class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int):
        self.depth: int = search_depth
        self.boards = PositionEvaluation()

    def time_of_function(function):
        def wrapped(*args):
            start_time = time.clock()
            res = function(*args)
            print('Move time:', time.clock() - start_time, '\n')
            return res
        return wrapped

    @time_of_function
    def next_move(self, board: BoardState) -> Optional[BoardState]:
        board_ = board.copy()
        # print('qqqqqqqqqqqqqqqqq')
        rating, move = self.make_tree(board_, 3)
        # print('old rating, rating, move: ', board.rating, rating, move)
        # print('bbbbbbbbbbbbbbbbb')
        board_.move(move[0], move[1], move[2], move[3], self.boards.WhiteValueBoard, self.boards.BlackValueBoard)
        # todo better implementation
        return board_

    def make_tree(self, board_, depth):
        if depth == 0:
            return board_.rating, (1, 1, 1, 1)
        possible_moves = board_.get_possible_moves_()
        #print('quantity: ', len(possible_moves))
        INF = 1000000
        rating = INF
        now_rating = board_.rating
        now_player = board_.current_player
        if board_.current_player == 1:
            rating *= -1
        move = (2, 2, 2, 2)
        for from_x, from_y, to_x, to_y in possible_moves:
            board_.move(from_x, from_y, to_x, to_y, self.boards.WhiteValueBoard, self.boards.BlackValueBoard)
            if abs(rating) != INF and (board_.rating > now_rating and now_player < 0 or board_.rating < now_rating and now_player == 1):  # if move is bad with high probability
                board_.current_player *= -1
                board_.move(to_x, to_y, from_x, from_y, self.boards.WhiteValueBoard, self.boards.BlackValueBoard)
                board_.current_player *= -1
                continue
            best_rating, best_move = self.make_tree(board_, depth - 1)
            if (best_rating < rating and now_player == -1 or best_rating > rating and now_player == 1):
                move = (from_x, from_y, to_x, to_y)
                rating = best_rating
            if board_.WhiteInOtherHouse == 9 * now_player == 1 or board_.BlackInOtherHouse == 9:
                rating = 999999 * now_player
                move = (from_x, from_y, to_x, to_y)

            board_.current_player *= -1
            board_.move(to_x, to_y, from_x, from_y, self.boards.WhiteValueBoard, self.boards.BlackValueBoard)
            board_.current_player *= -1
        rating = max(rating, board_.rating) if now_player == 1 else min(rating, board_.rating)
        return rating, move


