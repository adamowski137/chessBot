import chess
import random
import time
import math


class Tree:
    def __init__(self, depth):
        self.best_move = None
        self.evaluation = 0
        self.positions = 0
        self.max_positions = 5000
        self.depth = depth
        self.transposition_table = dict()

    def iterative_dfs(self, board, static_evaluation_function):
        self.static_evaluation_function = static_evaluation_function
        self.positions = 0
        self.transposition_table = dict()

        max_depth = int(self.depth)
        for i in range(1, max_depth+1):
            if self.positions > self.max_positions:
                print(f"Broke at {i}/{max_depth}")
                break
            self.depth = i
            self.evaluation = self.__minimax(
                board, self.depth, -math.inf, math.inf)

        self.depth = max_depth

        return self.evaluation, self.best_move

    def minimax(self, board, static_evaluation_function):
        self.best_move = None
        self.positions = 0
        self.static_evaluation_function = static_evaluation_function
        self.evaluation = self.__minimax(board, self.depth, -
                                         math.inf, math.inf)

        return self.evaluation, self.best_move

    def __children(self, board):
        """
        Function that yields all boards available from the given one,
        in a sorted order by calculated evaluations.
        """
        moves = []
        evaluations = []

        legal = board.legal_moves

        for move in legal:
            board.push(move)

            moves.append(move)
            evaluation = 0
            if (board.fen(), self.depth - 1) in self.transposition_table:
                evaluation = self.transposition_table[(
                    board.fen(), self.depth - 1)]
            evaluations.append(evaluation)

            board.pop()

        ordered_move_indices = [i[0] for i in sorted(
            enumerate(evaluations), key=lambda x:x[1])]

        if board.turn:
            ordered_move_indices = [i[0] for i in sorted(
                enumerate(evaluations), key=lambda x:x[1], reverse=True)]

        for idx in ordered_move_indices:
            board.push(moves[idx])
            yield board
            board.pop()

    def __minimax(self, board, depth, alpha, beta):
        self.positions += 1
        # or checkmate, or stalemate etc.
        if depth == 0 or board.outcome():
            evaluation = self.static_evaluation_function(board, depth)
            return evaluation

        if board.turn:
            maxEval = -1000000
            for child in self.__children(board):
                evaluation = 0
                if (child.fen(), self.depth) not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, alpha, beta)
                else:
                    evaluation = self.transposition_table[(
                        child.fen(), self.depth)]

                self.transposition_table[(
                    board.fen(), self.depth)] = evaluation

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
                if (child.fen(), self.depth) not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, alpha, beta)
                else:
                    evaluation = self.transposition_table[(
                        child.fen(), self.depth)]

                self.transposition_table[(
                    board.fen(), self.depth)] = evaluation

                if evaluation < minEval:
                    minEval = evaluation
                    if depth == self.depth:
                        self.best_move = board.peek()

                beta = min(beta, evaluation)
                if beta <= alpha:
                    board.pop()
                    break

            return minEval
