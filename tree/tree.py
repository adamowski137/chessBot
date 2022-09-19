import chess
import random
import time
import math


class Tree:
    def __init__(self, depth):
        self.depth = depth
        self.best_move = None
        self.eval = 0
        self.positions = 0
        self.transposition_table = dict()

    def static_evaluation_of_board(self, board, depth):
        outcome = board.outcome()
        if outcome:
            if outcome.termination in [chess.Termination.STALEMATE, chess.Termination.INSUFFICIENT_MATERIAL, chess.Termination.FIVEFOLD_REPETITION, chess.Termination.SEVENTYFIVE_MOVES, chess.Termination.THREEFOLD_REPETITION]:
                return 0
            if outcome.termination is chess.Termination.CHECKMATE and outcome.winner is True:
                return 100000 + depth
            elif outcome.termination is chess.Termination.CHECKMATE and outcome.winner is False:
                return -100000 - depth

        figures = board.piece_map()
        pieces = {"p": -1, "P": 1, "n": -3, "N": 3, "b": -3, "B": 3,
                  "r": -5, "R": 5, "q": -9, "Q": 9, "k": -0, "K": 0}
        sum = 0
        for i, value in figures.items():
            sum += pieces[value.symbol()]
        return sum

    def minimax(self, board):
        self.best_move = None
        self.positions = 0
        self.eval = self.__minimax(board, self.depth, -
                                   math.inf, math.inf, board.turn)
        self.transposition_table = dict()

        return self.eval, self.best_move

    def __children(self, board):
        """
        Function that yields all boards available from the given one.
        """
        for move in board.legal_moves:
            try:
                board.push(move)
            except:
                print(move)
            yield board
            board.pop()

    def __minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.outcome():  # or checkmate, or stalemate etc.
            eval = self.static_evaluation_of_board(board, depth)
            return eval

        self.positions += 1

        if maximizingPlayer:
            maxEval = -1000000
            for child in self.__children(board):
                eval = 0
                if child.fen() not in self.transposition_table:
                    eval = self.__minimax(child, depth -
                                          1, alpha, beta, False)
                else:
                    eval = self.transposition_table[child.fen()]

                self.transposition_table[board.fen()] = eval

                if eval >= maxEval:
                    maxEval = eval
                    if depth == self.depth:
                        self.best_move = board.peek()

                alpha = max(alpha, eval)
                if beta <= alpha:
                    board.pop()
                    break

            return maxEval
        else:
            minEval = 1000000
            for child in self.__children(board):
                eval = 0
                if child.fen() not in self.transposition_table:
                    eval = self.__minimax(child, depth -
                                          1, alpha, beta,  True)
                else:
                    eval = self.transposition_table[child.fen()]

                self.transposition_table[board.fen()] = eval

                if eval <= minEval:
                    minEval = eval
                    if depth == self.depth:
                        self.best_move = board.peek()

                beta = min(beta, eval)
                if beta <= alpha:
                    board.pop()
                    break

            return minEval
