"""
Performs MCTS to return the best move
"""


class MCTS_AI:
    def get_best_move(self, board, piece):
        best_x = 0
        best_piece = piece.get_next_rotation()
        return best_x, best_piece
