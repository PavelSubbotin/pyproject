from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState
from src.DefaultBoards import StartBoard1
from src.DefaultBoards import StartBoard2
from tests import Tests

class cons:
    def __init__(self):
        self.saved_board = None
        self.saved_log = None
        self.board_log = []
    
    def prev(self):
        return None if len(self.board_log) == 0 else self.board_log.pop()
    
    def save(self, board):
        self.saved_board = board.copy()
        self.saved_log = self.board_log.copy()
    
    def download(self):
        if self.saved_board is None:
            return None
        self.board_log = self.saved_log.copy()
        return self.saved_board.copy()

    def new_move(self, board):
        self.board_log.append(board.copy())


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    dark = (0, 0, 0)
    white = (200, 200, 200)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else dark
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = 255, 255, 255
        else:
            figure_color = 100, 100, 100
        r = elem_size // 2 - 10

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        if abs(figure) == 2:
            r = 5
            negative_color = [255 - e for e in figure_color]
            pygame.draw.circle(screen, negative_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)


def game_loop(screen: Surface, board: BoardState, ai: AI, game_mod):
    grid_size = screen.get_size()[0] // 8
    moves = 0
    while True:
        for event in pygame.event.get():
            #print("It's ", moves, 'move now!')
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]

                new_board = board.do_move(old_x, old_y, new_x, new_y, help_.WhiteValueBoard, help_.BlackValueBoard)
                if new_board is not None:
                    pers.new_move(board)
                    board = new_board
                    moves += 1

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3 and game_mod == 1:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 1) % 3 - 1  # change figure
                help_.update_information(board)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_board = ai.next_move(board)
                    if new_board is not None:
                        pers.new_move(board)
                        board = new_board
                        moves += 1
                if event.key == pygame.K_t:
                    print("Please, enter test number")
                    test_number = input()
                    if tests[test_number] is not None:
                        board = tests[test_number]
                        help_.update_information(board)
                    else:
                        print('There are only', len(tests), 'tests')
                if event.key == pygame.K_s:
                    pers.save(board.copy())
                if event.key == pygame.K_l:
                    board_ = pers.download()
                    if board_ is not None:
                        board = board_
                if event.key == pygame.K_LEFT:
                    prev = pers.prev()
                    if prev is None:
                        print("It's first turn")
                    else:
                        board = prev
                        
            if moves == 16:
                ai.boards.update()
            if board.is_game_finished:
                print(board.get_winner, 'won!')
                return

        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()


pygame.init()
help
print("Do you want to enter change mode?\nWrite 1 or 0")
game_mod = int(input())
pers = cons()
if game_mod == 1:
    tests = Tests()
ai = AI(PositionEvaluation(), search_depth=4)
help_ = PositionEvaluation()
StartBoard = StartBoard1() if game_mod == 0 else StartBoard2()

screen: Surface = pygame.display.set_mode([512, 512])

game_loop(screen, BoardState(StartBoard.startboard), ai, game_mod)

pygame.quit()
