import chess 
import random
import time



class Counter:
    def __init__(self):
        Counter.number_of_positions = 0



def static_evaluation_of_position(position):
    """
    Fake evaluation function that draws number from (-3.0, 3.0),
    but also increments Counter.number_of_positions
    """
    Counter.number_of_positions += 1
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

def main():
    Counter()
    depth = 6
    current_position = chess.Board(fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    start_time = time.time()
    minimax(current_position, depth, -1000000, 1000000, True)  
    print(f"On depth {depth} it took {time.time() - start_time}s to statically evaluate {Counter.number_of_positions} positions.")
    print(f"Without move ordering and without transposition table.")

if __name__ == "__main__":
    main()

