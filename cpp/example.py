import build.chess_lib as fmaf_chess
import chess

if __name__ == "__main__":
    board = chess.Board()
    fmaf_chess.evaluate(board.piece_map())
