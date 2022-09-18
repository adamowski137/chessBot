import chess 
import random
import time

number_of_positions = 0


def static_evaluation_of_position(position):
    figures = position.piece_map()

    pieces = {"p": -1, "P": 1, "n": -3, "N": 3, "b": -3, "B":3, "r": -5, "R":5, "q":-9, "Q":9, "k": -0, "K": 0 }
    sum = 0
    for i, value in figures.items():
        sum += pieces[value.symbol()]
    return sum
        

def children(position):
    """
    Function that yields all positions available from the given one.
    """
    for move in position.legal_moves:
        position.push(move)
        yield position
        position.pop()


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0: #or checkmate, or stalemate etc.
        eval = static_evaluation_of_position(position)
        if abs(eval) > 5:
            print(f"{position.fen()}, --- {eval}")
        return eval
    if maximizingPlayer:
        maxEval = -1000000
        for child in children(position):
            eval = minimax(child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                position.pop()
                break
        return maxEval
    else:
        minEval = 1000000
        for child in children(position):
            eval = minimax(child, depth - 1, alpha, beta,  True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                position.pop()
                break
        return minEval

