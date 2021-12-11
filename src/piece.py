from random import choice

RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (255, 0, 255)
TURQ = (64, 224, 208)

BODIES = [
    (((0, 0), (0, 1), (0, 2), (0, 3)), RED),  # stick
    (((0, 0), (0, 1), (0, 2), (1, 0)), ORANGE),  # L1
    (((0, 0), (1, 0), (1, 1), (1, 2)), YELLOW),  # L2
    (((0, 0), (1, 0), (1, 1), (2, 1)), GREEN),  # S1
    (((0, 1), (1, 0), (1, 1), (2, 0)), BLUE),  # S2
    (((0, 0), (0, 1), (1, 0), (1, 1)), INDIGO),  # Square
    (((0, 0), (1, 0), (1, 1), (2, 0)), TURQ),  # pyramid
]


class Piece:
    def __init__(self, body=None, color=None):
        if body == None:
            self.body, self.color = choice(BODIES)
        else:
            self.body = body
            self.color = color
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
        return Piece(new_body, self.color)


def main():
    for b in BODIES:
        p = Piece(b)
        print(p.skirt)


if __name__ == "__main__":
    main()
