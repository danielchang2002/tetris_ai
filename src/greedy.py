from copy import copy, deepcopy
import numpy as np
from genetic_helpers import *
from piece import BODIES, Piece
from board import Board
from random import randint

"""
Performs a heuristic search of depth = 1
Generates all possible placements with the current piece
(all possible horizontal positions, all possible rotations)
chooses the placement that minimizes the cost function
"""

A = 0.5
B = 0.5


class Greedy_AI:
    def get_best_move(self, board, piece, depth=1):
        best_x = -1
        best_piece = None
        min_cost = 100000000
        # moves = []
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue
                c = self.cost(board.board, x, y, piece)
                if c < min_cost:
                    min_cost = c
                    best_x = x
                    best_y = y
                    best_piece = piece
        # return best_x, best_piece
        return best_x, best_piece

    def get_best_move_new(self, board, piece):
        best_x = -1
        best_piece = None
        min_cost = 100000000
        # moves = []
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue
                costs = []
                moved_board = Board()
                moved_board.board = deepcopy(board.board)
                moved_board.widths = deepcopy(board.widths)
                moved_board.heights = deepcopy(board.heights)
                moved_board.place(x, y, piece)
                # for next_body_idx in range(len(BODIES2)):
                #     new_piece = Piece(body=BODIES2[next_body_idx][0])
                #     for j in range(4):
                #         new_piece = new_piece.get_next_rotation()
                #         for x2 in range(moved_board.width):
                #             try:
                #                 y2 = moved_board.drop_height(new_piece, x2)
                #             except:
                #                 continue
                #             c = self.cost(moved_board.board, x2, y2, new_piece)
                #             costs.append(c)
                for j in range(5):
                    new_piece = Piece(body=BODIES[randint(0, 9)][0])
                    x2 = randint(0, 9)
                    try:
                        y2 = moved_board.drop_height(new_piece, x2)
                    except:
                        continue
                    c = self.cost(moved_board.board, x2, y2, new_piece)
                    costs.append(c)

                cost = np.mean(costs)
                if cost < min_cost:
                    min_cost = cost
                    best_x = x
                    best_piece = piece

        # return best_x, best_piece
        return best_x, best_piece

    def cost(self, board, x, y, piece):
        """
        COST = #holes + max height
        """

        board_copy = deepcopy(board)

        for pos in piece.body:
            board_copy[y + pos[1]][x + pos[0]] = True

        holes = 0
        max_height = 0
        num_cleared = 0
        cum_wells = 0
        for i in range(len(board_copy)):
            if all(board_copy[i]):
                num_cleared += 1
            for j in range(len(board_copy[0])):

                if board_copy[i][j]:
                    max_height = max(max_height, i)
                    # filled, can't be a hole
                    continue
                has = False
                for k in range(i + 1, len(board_copy)):
                    if board_copy[k][j]:
                        has = True
                        break
                if has:
                    # has a block above
                    holes += 1
                # if not has:
                #     left_blocked = j == 0 or board_copy[i][j - 1]
                #     right_blocked = j == 9 or board_copy[i][j + 1]
                #     if left_blocked and right_blocked:
                #         cum_wells += 1
        agg_height = 0
        for col in range(len(board_copy[i])):
            agg = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    agg = row
            agg_height += agg
        heights = []
        for col in range(len(board_copy[i])):
            mh = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    mh = row
            heights.append(mh)
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        c = 0.5 * agg_height + 0.35 * holes + 0.18 * bumpiness - 0.76 * num_cleared
        # c = agg_height + holes + bumpiness - num_cleared
        return c

    def cost0(self, board):
        """
        COST = #holes + max height
        """
        # board_copy = deepcopy(board.board)
        board_copy = board.board

        # for pos in piece.body:
        #     board_copy[y + pos[1]][x + pos[0]] = True

        holes = 0
        max_height = 0
        num_cleared = 0
        cum_wells = 0
        for i in range(len(board_copy)):
            if all(board_copy[i]):
                num_cleared += 1
            for j in range(len(board_copy[0])):

                if board_copy[i][j]:
                    max_height = max(max_height, i)
                    # filled, can't be a hole
                    continue
                has = False
                for k in range(i + 1, len(board_copy)):
                    if board_copy[k][j]:
                        has = True
                        break
                if has:
                    # has a block above
                    holes += 1
                # if not has:
                #     left_blocked = j == 0 or board_copy[i][j - 1]
                #     right_blocked = j == 9 or board_copy[i][j + 1]
                #     if left_blocked and right_blocked:
                #         cum_wells += 1
        agg_height = 0
        for col in range(len(board_copy[i])):
            agg = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    agg = row
            agg_height += agg
        heights = []
        for col in range(len(board_copy[i])):
            mh = 0
            for row in range(len(board_copy)):
                if board_copy[row][col]:
                    mh = row
            heights.append(mh)
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])

        c = 0.5 * agg_height + 0.35 * holes + 0.18 * bumpiness - 0.76 * num_cleared
        return c
