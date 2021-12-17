from copy import copy, deepcopy
from genetic_helpers import *

"""
Performs a heuristic search of depth = 1
Generates all possible placements with the current piece
(all possible horizontal positions, all possible rotations)
chooses the placement that minimizes the cost function
"""

A = 0.5
B = 0.5


class Greedy_AI:
    def get_best_move(self, board, piece):
        best_x = -1
        best_piece = None
        min_cost = 10000000000
        # moves = []
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue
                c = self.cost(board, x, y, piece)
                # moves.append({"cost": c, "x": x, "piece": piece})
                if c < min_cost:
                    min_cost = c
                    best_x = x
                    best_piece = piece
        # print(min_cost)
        # list.sort(moves, key=lambda x: (x["cost"][0], x["cost"][1]))
        return best_x, best_piece
        # return moves[0]["x"], moves[0]["piece"]

    def cost(self, board, x, y, piece):
        """
        COST = #holes + max height
        """
        board_copy = deepcopy(board.board)

        for pos in piece.body:
            board_copy[y + pos[1]][x + pos[0]] = True

        holes = 0
        max_height = 0
        num_cleared = 0
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
                    holes += 1
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

        # c = 0.5 * agg_height + 0.35 * holes + 0.18 * bumpiness - 0.76 * num_cleared
        c = agg_height + holes + bumpiness - num_cleared
        return c
