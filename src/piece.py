from random import choice

BODIES = [
    ((0, 0), (0, 1), (0, 2), (0, 3)),  # stick
    ((0, 0), (0, 1), (0, 2), (1, 0)),  # L1
    ((0, 0), (1, 0), (1, 1), (1, 2)),  # L2
    ((0, 0), (1, 0), (1, 1), (2, 1)),  # S1
    ((0, 1), (1, 0), (1, 1), (2, 0)),  # S2
    ((0, 0), (0, 1), (1, 0), (1, 1)),  # Square
    ((0, 0), (1, 0), (1, 1), (2, 0)),  # pyramid
]


class Piece:
    def __init__(self, body=None):
        if body == None:
            self.body = choice(BODIES)
        else:
            self.body = body
        self.skirt = self.calc_skirt()

    def calc_skirt(self):
        skirt = []
        for i in range(4):
            low = 1000
            for b in self.body:
                if b[0] == i:
                    low = min(low, b[1])
            if low != 1000:
                skirt.append(low)
        return skirt

    def get_next_rotation(self):
        width = len(self.skirt)
        # height = max([b[1] for b in self.body])
        new_body = [(width - b[1], b[0]) for b in self.body]
        leftmost = min([b[0] for b in new_body])
        new_body = [(b[0] - leftmost, b[1]) for b in new_body]
        return Piece(new_body)


def main():
    for b in BODIES:
        p = Piece(b)
        print(p.skirt)


if __name__ == "__main__":
    main()
