import sys

from source import game

debug = "debug" in sys.argv

if __name__ == "__main__":
    game.run(debug)