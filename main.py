import chess
from tree.tree import *
from ui.ui import Board
import argparse
import math

def main(args):
    board = Board(fen = args.fen)

    if args.display:
        board.display()

    minimax(board, 5, -math.inf, math.inf, True)
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chess bot")

    # Values
    parser.add_argument('-f', '--fen', help="Name of the input XML file.", default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', required=False)
    parser.add_argument('-d', '--depth', help="Maximum search depth.", default=3, type=float, required=False)

    # Flags
    parser.add_argument('--display', dest="display",
                        help="Run the UI", action='store_true')

    # Default flags
    parser.set_defaults(display=False)
    
    args = parser.parse_args()

    main(args)

    


