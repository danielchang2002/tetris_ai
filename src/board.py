from copy import deepcopy


class Board:
    def __init__(self):
        self.width, self.height = 10, 20
        self.board = self.init_board()
        self.colors = self.init_board()
        self.widths = [0] * (self.height + 4)
        self.heights = [0] * self.width

    def init_board(self):
        b = []
        for row in range(self.height + 4):
            row = []
            for col in range(self.width):
                row.append(False)
            b.append(row)
        return b

    def place(self, x, y, piece):
        # check if valid
        for pos in piece.body:
            target_y = y + pos[1]
            target_x = x + pos[0]
            if (
                target_y < 0
                or target_y >= self.height + 4
                or target_x < 0
                or target_x >= self.width
                or self.board[y + pos[1]][x + pos[0]]
            ):
                return Exception("Bad placement")
        for pos in piece.body:
            self.board[y + pos[1]][x + pos[0]] = True
            self.colors[y + pos[1]][x + pos[0]] = piece.color
            self.widths[y + pos[1]] += 1
            self.heights[x + pos[0]] = max(self.heights[x + pos[0]], y + pos[1] + 1)
        return 0

    def drop_height(self, piece, x):
        y = -1
        for i in range(len(piece.skirt)):
            y = max(self.heights[x + i] - piece.skirt[i], y)
        return y

    def top_filled(self):
        return sum([w for w in self.widths[-4:]]) > 0
