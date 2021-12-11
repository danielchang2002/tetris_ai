from copy import copy, deepcopy

"""
Performs a heuristic search of depth = 1
Generates all possible placements with the current piece
(all possible horizontal positions, all possible rotations)
chooses the placement that minimizes the cost function
"""


class Greedy_AI:
    def get_best_move(self, board, piece):
        best_x = -1
        best_piece = None
        min_cost = 20 + 10 * 24
        for i in range(4):
            piece = piece.get_next_rotation()
            for x in range(board.width):
                try:
                    y = board.drop_height(piece, x)
                except:
                    continue
                c = self.cost(board, x, y, piece)
                if c < min_cost:
                    min_cost = c
                    best_x = x
                    best_piece = piece
        return best_x, best_piece

    def cost(self, board, x, y, piece):
        """
        COST = # of holes + max height
        """
        board_copy = deepcopy(board.board)

        for pos in piece.body:
            board_copy[y + pos[1]][x + pos[0]] = True

        holes = 0
        for i in range(len(board_copy)):
            for j in range(len(board_copy[0])):
                if board_copy[i][j]:
                    # filled, can't be a hole
                    continue

                if i - 1 < 0:
                    top = True
                else:
                    top = board_copy[i - 1][j]

                if i + 1 >= len(board_copy):
                    bottom = True
                else:
                    bottom = board_copy[i + 1][j]

                if j - 1 < 0:
                    left = True
                else:
                    left = board_copy[i][j - 1]

                if j + 1 >= len(board_copy[0]):
                    right = True
                else:
                    right = board_copy[i][j + 1]

                if top and right and bottom and left:
                    holes += 1
        c = y + max(piece.skirt) + holes
        return c
