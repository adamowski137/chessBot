def material(position):
    figures = position.piece_map()

    pieces = {"p": -1, "P": 1, "n": -3, "N": 3, "b": -3, "B":3, "r": -5, "R":5, "q":-9, "Q":9, "k": -0, "K": 0 }
    sum = 0
    for i, value in figures.items():
        sum += pieces[value.symbol()]
    return sum

def controlledTiles(position):
    position.legal_moves().count()

def evaluate(position):
    print(controlledTiles(position))
    return material(position)