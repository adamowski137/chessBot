import chess



def static_evaluation_function(board, depth):
        outcome = board.outcome()
        if outcome:
            if outcome.termination in [
                chess.Termination.STALEMATE, 
                chess.Termination.INSUFFICIENT_MATERIAL, 
                chess.Termination.FIVEFOLD_REPETITION, 
                chess.Termination.SEVENTYFIVE_MOVES, 
                chess.Termination.THREEFOLD_REPETITION
                ]:
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