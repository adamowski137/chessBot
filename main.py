import chess
import chess.pgn
from tree.tree import *
from UI.ui import Board
import argparse
import math
from static_evaluation.static_evaluation import static_evaluation_function
import time
from timeit import default_timer as timer


def main(args):
    tree = Tree(args.depth)

    if args.display:
        from ui.ui import Board
        board = Board(fen=args.fen)
        print("DISPLAY")
        board.display()
    else:
        board = chess.Board(fen=args.fen)

    while True:
        if board.turn == chess.BLACK or args.self_play:
            start = timer()
            eval, move = tree.iterative_dfs(
                board, static_evaluation_function)
            end = timer()
            print("Time:", end - start)
            if move is None:
                print("Can't make a move.")
                break
            print(eval, move, tree.positions)
            board.push(move)
            print(board)
        elif not args.display:
            move = input("Input move: ")
            move = chess.Move.from_uci(move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print(f"Incorrect move.\nEnded with position: {board.fen()}")
                break

    game = chess.pgn.Game.from_board(board)
    print(game)


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
    parser.add_argument('--self-play', dest="self_play",
                        help="Play the game against itself.", action='store_true')

    # Default flags
    parser.set_defaults(display=False)
    parser.set_defaults(self_play=False)

    args = parser.parse_args()

    main(args)
