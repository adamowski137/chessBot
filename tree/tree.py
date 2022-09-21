import chess
import random
import time
import math


class Tree:
    def __init__(self, depth):
        self.best_move = None
        self.evaluation = 0
        self.positions = 0
        self.depth = depth
        self.transposition_table = dict()

    def minimax(self, board, static_evaluation_function):
        self.best_move = None
        self.positions = 0
        self.static_evaluation_function = static_evaluation_function
        self.evaluation = self.__minimax(board, self.depth, -
                                         math.inf, math.inf)
        self.transposition_table = dict()

        return self.evaluation, self.best_move

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

    def __minimax(self, board, depth, alpha, beta):
        if depth == 0 or board.outcome():  # or checkmate, or stalemate etc.
            evaluation = self.static_evaluation_function(board, depth)
            return evaluation

        self.positions += 1

        if board.turn:
            maxEval = -1000000
            for child in self.__children(board):
                evaluation = 0
                if child.fen() not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, alpha, beta)
                else:
                    evaluation = self.transposition_table[child.fen()]

                self.transposition_table[board.fen()] = evaluation

                if evaluation > maxEval:
                    maxEval = evaluation
                    if depth == self.depth:
                        self.best_move = board.peek()

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    board.pop()
                    break

            return maxEval
        else:
            minEval = 1000000
            for child in self.__children(board):
                evaluation = 0
                if child.fen() not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, alpha, beta)
                else:
                    evaluation = self.transposition_table[child.fen()]

                self.transposition_table[board.fen()] = evaluation

                if evaluation < minEval:
                    minEval = evaluation
                    if depth == self.depth:
                        self.best_move = board.peek()

                beta = min(beta, evaluation)
                if beta <= alpha:
                    board.pop()
                    break

            return minEval
