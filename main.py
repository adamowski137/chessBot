import chess
from tree.tree import *
import argparse
import math
from static_evaluation.static_evaluation import static_evaluation_function
import time


def main(args):
    tree = Tree()

    if args.display:
        from UI.ui import Board
        board = Board(fen=args.fen)
        print("DISPLAY")
        board.display()
    else:
        board = chess.Board(fen = args.fen)

    while True:
        if board.turn == chess.BLACK:
            print("WAIT FOR THE MOVE")
            eval, move = tree.minimax(board, args.depth,static_evaluation_function) 
            if move is None:
                print("MOVE IS NONE")
                break
            print(eval, move)
            board.push(move)
        time.sleep(0.5)

    # for i in range(100):
    #     eval, move = tree.minimax(board, static_evaluation_function)
    
        


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
