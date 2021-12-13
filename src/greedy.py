from copy import copy, deepcopy

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
            if all(board_copy[i]):
                return -100000
            for j in range(len(board_copy[0])):
                if board_copy[i][j]:
                    # filled, can't be a hole
                    continue
                has = False
                for k in range(i + 1, len(board_copy)):
                    if board_copy[k][j]:
                        has = True
                        break
                if has:
                    holes += 1
        c = A * (y + max([body[1] for body in piece.body])) + B * holes
        return c
