from enum import Enum
import time

import chess


class GameType(Enum):
    START = 0
    EARLY = 1
    MID = 2
    END = 3

    EVEN = 4
    WHITE_ADVANTAGE = 5
    BLACK_ADVANTAGE = 6


class Game():
    def __init__(self, white_player, black_player, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', type=GameType.START, name="Game"):
        self.white = white_player
        self.black = black_player
        self.board = chess.Board(fen=fen)
        self.type = type
        self.name = name

    def play():
        while not self.board.outcome():
            start_timer = time.perf_counter()
            eval, move = 0, None
            if self.board.turn == chess.color.WHITE:
                eval, move = self.white.move(board)
            else:
                eval, move = self.black.move(board)
            end_timer = time.perf_counter()
            if move is None:
                print(
                    f"No available move for white at game: \"{self.name}\"")
                break
            print(f"Eval: {eval}, {move}")
            self.board.push(move)
