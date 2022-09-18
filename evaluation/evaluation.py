import chess 
import constants


def material(figures):
    pieces = {"p": -1, "P": 1, "n": -3, "N": 3, "b": -3, "B":3, "r": -5, "R":5, "q":-9, "Q":9, "k": -0, "K": 0 }
    sum = 0
    for i, value in figures.items():
        # print(type(value.symbol()))
        sum += pieces[value.symbol()]
    return sum
        



def main():
    position =  chess.Board(fen = "rn1qkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    print(material(chess.Board.piece_map(position)))

if __name__ == "__main__":
    main()

