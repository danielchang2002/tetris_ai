from random import randint


class Random_AI:
    def get_best_move(self, board, piece):
        x = randint(0, 9)
        rotations = randint(0, 3)
        for i in range(rotations):
            piece = piece.get_next_rotation()
        return x, piece
