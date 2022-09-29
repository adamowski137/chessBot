import chess
import random
import time
import math


class Tree:
    def __init__(self, depth, static_evaluation_function, probability=0.000000001):
        self.best_move = None
        self.evaluation = 0
        self.positions = 0
        self.max_positions = 5000

        self.depth = depth
        self.min_depth = depth
        self.min_probability = probability

        self.max_reached_depth = 0

        self.transposition_table = dict()
        self.static_evaluation_function = static_evaluation_function

    def iterative_dfs(self, board):
        self.positions = 0
        self.transposition_table = dict()

        max_depth = int(self.depth)
        self.max_reached_depth = 0
        for i in range(1, max_depth+1, 1):
            if self.positions > self.max_positions:
                print(
                    f"Broke after min:{self.depth}")
                break
            self.depth = i
            self.min_depth = self.depth
            self.evaluation = self.__minimax(
                board, self.depth, 1.0, -math.inf, math.inf)

        self.depth = max_depth

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
        cur_pieces = len(board.piece_map().items())
        is_check = True if board.is_check() else False

        d = self.depth - depth

        can_capture = False
        for move in legal:
            board.push(move)
            new_pieces = len(board.piece_map())
            if new_pieces < cur_pieces:
                can_capture = True
                board.pop()
                break
            board.pop()

        for move in legal:
            n += 1

            board.push(move)

            new_pieces = len(board.piece_map())

            moves.append(move)

            evaluation = 0
            if (board.fen(), self.depth - 1) in self.transposition_table:
                evaluation = self.transposition_table[(
                    board.fen(), self.depth - 1)]
            evaluations.append(evaluation)

            board.pop()

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

    def __minimax(self, board, depth, probability, alpha, beta):
        self.positions += 1
        # or checkmate, or stalemate etc.
        if depth == 0 or probability < self.min_probability or board.outcome():
            evaluation = self.static_evaluation_function(board, depth)
            return evaluation

        self.max_reached_depth = max(
            self.max_reached_depth, self.depth - depth)

        if board.turn:
            maxEval = -1000000
            for n, child in self.__children(board, depth):
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
