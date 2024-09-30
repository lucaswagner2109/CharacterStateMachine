import sys

from game import game

debug = "debug" in sys.argv

if __name__ == "__main__":
    game.run(debug)