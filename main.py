import sys

from game import Game

debug = "debug" in sys.argv

if __name__ == "__main__":
    game = Game(debug)
    game.run()