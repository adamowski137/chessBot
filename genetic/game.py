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
    def __init__(self, white_player, black_player, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', game_type=GameType.START, name="Game"):
        self.white = white_player
        self.black = black_player
        self.board = chess.Board(fen=fen)
        self.type = game_type
        self.name = name

    def play(self):
        while not self.board.outcome():
            start_timer = time.perf_counter()
            eval, move = 0, None
            if self.board.turn == chess.WHITE:
                eval, move = self.white.move(self.board)
            else:
                eval, move = self.black.move(self.board)
            end_timer = time.perf_counter()
            if move is None:
                print(
                    f"No available move for white at game: \"{self.name}\"")
                break

            if self.board.turn == chess.WHITE:
                print(
                    f"E: {eval}, M: {move}, T: {end_timer-start_timer}s, P: {self.white.tree.positions}")
            else:
                print(
                    f"E: {eval}, M: {move}, T: {end_timer-start_timer}s, P: {self.black.tree.positions}")
            self.board.push(move)
