from game import Game
import sys


def main():
    for i in range(20):
        g = Game(sys.argv[1])
        g.run_no_visual()


if __name__ == "__main__":
    main()
