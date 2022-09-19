import chess
from tree.tree import *
from ui.ui import Board
import argparse
import math


def main(args):
    board = Board(fen=args.fen)
    tree = Tree(depth=args.depth)

    if args.display:
        board.display()

    for i in range(100):
        eval, move = tree.minimax(board)

        if move is None:
            break

        print(eval, move)
        board.push(move)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chess bot")

    # Values
    parser.add_argument('-f', '--fen', help="Name of the input XML file.",
                        default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', required=False)
    parser.add_argument('-d', '--depth', help="Maximum search depth.",
                        default=6, type=float, required=False)

    # Flags
    parser.add_argument('--display', dest="display",
                        help="Run the UI", action='store_true')

    # Default flags
    parser.set_defaults(display=False)

    args = parser.parse_args()

    main(args)
