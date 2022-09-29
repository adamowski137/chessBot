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
    def __init__(self, white_player, black_player, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', game_type=GameType.START, name="Game", display=False):
        self.white = white_player
        self.black = black_player
        self.type = game_type
        self.name = name
        self.display = display

        if self.display:
            from UI.ui import Board
            self.board = Board(fen=fen)
            self.board.display()
        else:
            self.board = chess.Board(fen=fen)

    def play(self):
        if self.white and self.black:
            return self.__self_play()
        else:
            return self.__human_play()

    def save(self, path):
        if not self.board.move_stack:
            return

        game = chess.pgn.Game()
        node = game.add_variation(self.board.move_stack[0])
        for move in self.board.move_stack[1:]:
            node = node.add_variation(move)

        with open(path, 'a+') as f:
            f.write(f"\nGame: {self.name}\n")
            f.write(f"{game}")
            f.close()

    def __human_play(self):
        computer_player = self.white if self.white else self.black
        while not self.board.outcome():
            if (self.white and self.board.turn) or (self.black and not self.board.turn):
                start_timer = time.perf_counter()
                evaluation, move = 0, None

                evaluation, move = computer_player.move(self.board)

                end_timer = time.perf_counter()

                if move is None:
                    print(
                        f"No available move at game: \"{self.name}\"")
                    break

                print(
                    f"{self.name} - E: {round(evaluation, 2)}, M: {move}, T: {round(end_timer-start_timer, 2)}s, P: {computer_player.tree.positions}")

                self.board.push(move)

            else:
                made_legal_move = False
                while not made_legal_move:
                    move = input("Input move:")
                    move = chess.Move.from_uci(move)
                    if move in self.board.legal_moves:
                        self.board.push(move)
                        made_legal_move = True
                    else:
                        print(f"Incorrect move. Try again")

        return self

    def __self_play(self):
        while not self.board.outcome() and len(self.board.move_stack) < 5:
            start_timer = time.perf_counter()
            evaluation, move = 0, None

            if self.board.turn == chess.WHITE:
                evaluation, move = self.white.move(self.board)
            else:
                evaluation, move = self.black.move(self.board)

            end_timer = time.perf_counter()

            if move is None:
                print(
                    f"No available move at game: \"{self.name}\"")
                break

            if self.board.turn == chess.WHITE:
                print(
                    f"{self.name} - E: {round(evaluation, 2)}, M: {move}, T: {round(end_timer-start_timer, 2)}s, P: {self.white.tree.positions}")
            else:
                print(
                    f"{self.name} - E: {round(evaluation, 2)}, M: {move}, T: {round(end_timer-start_timer, 2)}s, P: {self.black.tree.positions}")

            self.board.push(move)

        return self
