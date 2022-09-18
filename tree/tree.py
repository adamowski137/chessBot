import chess 
import random
import time

number_of_positions = 0

def static_evaluation_of_position(position):
    """
    Fake evaluation function that draws number from (-3.0, 3.0),
    but also increments Counter.number_of_positions
    """
    global number_of_positions
    number_of_positions += 1
    return random.uniform(-3.0, 3.0)


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
        print(position.fen())
        return static_evaluation_of_position(position)
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

