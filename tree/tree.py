import chess 
import random
import copy


class Counter:
    def __init__(self):
        Counter.x = 0



def static_evaluation_of_position(position):
    Counter.x += 1
    return random.uniform(-3.0, 3.0)


def children(position):
    for move in position.legal_moves:
        new_position = copy.copy(position)
        new_position.push(move)
        yield new_position


def minimax(position, depth, alpha, beta, maximizingPlayer):
    if depth == 0:
        print(position)
        print("\n\n")
        return static_evaluation_of_position(position)


    if maximizingPlayer:
        maxEval = -1000000000
        for child in children(position):
            eval = minimax(child, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = 1000000000
        for child in children(position):
            eval = minimax(child, depth - 1, alpha, beta,  True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def main():
    a = Counter()
    current_position = chess.Board(fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    minimax(current_position, 2, -1000000000, 1000000000, True)
    print(Counter.x)
    
    pass

if __name__ == "__main__":
    main()

