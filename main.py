import sys

from game import game

debug_mode = "debug" in sys.argv

if __name__ == "__main__":
    game.run()