import chess
from tree.tree import *
from ui.ui import Board_displayer
import argparse

def run(args):
    if args.display:
        board = Board_displayer(fen = args.fen)
        board.display()

    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chess bot")

    # Values
    parser.add_argument('-f', '--fen', help="Name of the input XML file.", default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', required=False)

    # Flags
    parser.add_argument('--display', dest="display",
                        help="Run the UI", action='store_true')

    # Default flags
    parser.set_defaults(display=False)
    
    args = parser.parse_args()

    run(args)

    


