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
            self.weights['points'] = max(0.2, random.gauss(1, 0.5))
            self.weights['tiles'] = max(0, random.gauss(0.1, 0.05))

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
