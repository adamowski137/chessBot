import chess
import random
import time
import math


class Tree:
    def __init__(self, depth, static_evaluation_function, probability=0.0000001):
        self.best_move = None
        self.evaluation = 0
        self.positions = 0
        self.depth = depth
        self.max_depth = depth
        self.min_probability = probability

        self.max_reached_depth = 0

        self.transposition_table = dict()
        self.static_evaluation_function = static_evaluation_function

    def iterative_dfs(self, board):
        self.positions = 0
        self.transposition_table = dict()

        self.max_reached_depth = 0
        for i in range(1, self.max_depth+1, 1):
            self.depth = i
            self.evaluation = self.__minimax(
                board, self.depth, 1.0, -math.inf, math.inf)

        self.depth = self.max_depth

        print(f"Reached up to {self.max_reached_depth}")

        return self.evaluation, self.best_move

    def minimax(self, board):
        self.best_move = None
        self.positions = 0
        self.evaluation = self.__minimax(board, self.depth, 1.0, -
                                         math.inf, math.inf)

        return self.evaluation, self.best_move

    def __children(self, board, depth):
        """
        Function that yields all boards available from the given one,
        in a sorted order by calculated evaluations.
        """
        moves = []
        evaluations = []

        legal = board.legal_moves
        n = 0

        # TODO: faster function find
        is_check = board.is_check()

        d = self.depth - depth

        for move in legal:
            n += 1

            board.push(move)

            moves.append(move)

            evaluation = 0
            if (board.fen(), self.depth - 1) in self.transposition_table:
                evaluation = self.transposition_table[(
                    board.fen(), self.depth - 1)]
            evaluations.append(evaluation)

            board.pop()

        if not moves:
            yield 0, []

        if board.turn:
            ordered_move_indices = [i[0] for i in sorted(
                enumerate(evaluations), key=lambda x:x[1], reverse=True)]
        else:
            ordered_move_indices = [i[0] for i in sorted(
                enumerate(evaluations), key=lambda x:x[1])]

        for idx in ordered_move_indices:
            board.push(moves[idx])
            yield n, board
            board.pop()

    def __was_capture(self, board):
        if not board.move_stack:
            return True

        cur_pieces = len(board.piece_map().items())
        last_move = board.pop()
        bef_pieces = len(board.piece_map().items())
        board.push(last_move)

        if cur_pieces < bef_pieces:
            return True

        return False

    def __minimax(self, board, depth, probability, alpha, beta):
        self.positions += 1
        if board.outcome():
            return self.static_evaluation_function.evaluate(board, depth)
        elif self.depth < self.max_depth and (depth <= 0):
            return self.static_evaluation_function.evaluate(board, depth)
        elif self.depth == self.max_depth and not self.__was_capture(board):
            return self.static_evaluation_function.evaluate(board, depth)

        self.max_reached_depth = max(
            self.max_reached_depth, self.depth - depth + 1)

        if board.turn:
            maxEval = -1000000
            for n, child in self.__children(board, depth):
                if n == 0:
                    maxEval = max(
                        maxEval, self.static_evaluation_function(board, depth))
                    break

                evaluation = 0
                if (child.fen(), self.depth) not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, probability * (1 / n), alpha, beta)
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
            for n, child in self.__children(board, depth):
                if n == 0:
                    minEval = min(
                        minEval, self.static_evaluation_function(board, depth))
                    break

                evaluation = 0
                if (child.fen(), self.depth) not in self.transposition_table:
                    evaluation = self.__minimax(child, depth -
                                                1, probability * (1 / n), alpha, beta)
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
