from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState
from src.DefaultBoards import StartBoard1
from src.DefaultBoards import StartBoard2
from tests import tests


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
                    board_log.append(board)
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
                        board_log.append(board)
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
                    saved_board = board.copy()
                if event.key == pygame.K_l:
                    board = saved_board.copy()
                if event.key == pygame.K_LEFT:
                    if len(board_log) == 0:
                        print("It's first turn")
                    else:
                        board = board_log[-1]
                        board_log.pop()
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
if game_mod == 1:
    tests = tests()
safed_board = None
board_log = []
ai = AI(PositionEvaluation(), search_depth=4)
help_ = PositionEvaluation()
StartBoard = StartBoard1() if game_mod == 0 else StartBoard2()

screen: Surface = pygame.display.set_mode([512, 512])

game_loop(screen, BoardState(StartBoard.startboard), ai, game_mod)

pygame.quit()
