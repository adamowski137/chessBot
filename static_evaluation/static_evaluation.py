import argparse
import random

import chess


def evaluate(board):
    return material(board) + 0.1 * controlledTiles(board)


def static_evaluation_function(board, depth):
    outcome = board.outcome()
    if outcome:
        if outcome.termination in [
            chess.Termination.STALEMATE,
            chess.Termination.INSUFFICIENT_MATERIAL,
            chess.Termination.FIVEFOLD_REPETITION,
            chess.Termination.SEVENTYFIVE_MOVES,
            chess.Termination.THREEFOLD_REPETITION
        ]:
            return 0
        if outcome.termination is chess.Termination.CHECKMATE and outcome.winner is True:
            return 100000 + depth
        elif outcome.termination is chess.Termination.CHECKMATE and outcome.winner is False:
            return -100000 - depth

    return evaluate(board)


class Evaluation():
    def __init__(self, weights=None):
        # self.weights powinno byc tablica zeby miec szybszy access
        if weights:
            self.weights = weights
        else:
            self.weights = dict()
            self.weights['points'] = max(0.2, random.gauss(1, 0.005))
            self.weights['tiles'] = 0

            print(self.weights)

    def evaluate(self, board, depth):
        outcome = board.outcome()
        if outcome:
            if outcome.termination in [
                chess.Termination.STALEMATE,
                chess.Termination.INSUFFICIENT_MATERIAL,
                chess.Termination.FIVEFOLD_REPETITION,
                chess.Termination.SEVENTYFIVE_MOVES,
                chess.Termination.THREEFOLD_REPETITION
            ]:
                return 0
            if outcome.termination is chess.Termination.CHECKMATE and outcome.winner is True:
                return 100000 + depth
            elif outcome.termination is chess.Termination.CHECKMATE and outcome.winner is False:
                return -100000 - depth

        return self.__evaluate_static(board)

    def __evaluate_static(self, board):
        # Network architecture
        e = self.weights['points'] * self.__material(board)
        e += self.weights['tiles'] * self.__controlled_tiles(board)
        return e

    def __material(self, board):
        figures = board.piece_map()
        amounts = {"p": 0, "P": 0, "n": 0, "N": 0, "b": 0, "B": 0,
                   "r": 0, "R": 0, "q": 0, "Q": 0, "k": 0, "K": 0}
        pieces = {"p": -1, "P": 1, "n": -3, "N": 3, "b": -3, "B": 3,
                  "r": -5, "R": 5, "q": -9, "Q": 9, "k": -0, "K": 0}
        sum = 0
        for i, value in figures.items():
            sum += pieces[value.symbol()]
            amounts[value.symbol()] += 1
        return sum

    def __controlled_tiles(self, board):
        attackerTiles = board.legal_moves.count()
        board.push(chess.Move.null())
        defenderTiles = board.legal_moves.count()
        board.pop()

        if board.turn:
            return attackerTiles - defenderTiles
        else:
            return defenderTiles - attackerTiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chess evaluation")
    parser.add_argument('-f', '--fen', help="Name of the input XML file.",
                        default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', required=False)
    args = parser.parse_args()

    evaluation = Evaluation()
    board = chess.Board(args.fen)

    print(evaluation.evaluate(board, 0))
