import chess
import random
import time
import math


class Tree:
    def __init__(self):
        self.best_move = None
        self.eval = 0
        self.positions = 0
        self.transposition_table = dict()

    def minimax(self, board, depth, static_evaluation_function):
        self.depth = depth
        self.best_move = None
        self.positions = 0
        self.static_evaluation_function = static_evaluation_function
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
            eval = self.static_evaluation_function(board, depth)
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
