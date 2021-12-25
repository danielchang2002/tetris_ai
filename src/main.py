from game import Game
import sys
import os


def main():
    # textfile = open("./src/data/expectiminimax/10.csv", "w")
    # textfile.write("dropped, rows\n")
    # for i in range(2):
    #     print(i)
    #     g = Game(sys.argv[1])
    #     dropped, rows = g.run_no_visual()
    #     textfile.write(str(dropped) + ", " + str(rows) + "\n")
    # textfile.close()
    g = Game(sys.argv[1])
    # g.run_no_visual()
    g.run()


if __name__ == "__main__":
    main()
