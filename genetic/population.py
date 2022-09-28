import random

from genetic.player import Player
from genetic.game import Game, GameType


class Population():
    def __init__(self, size, depth):
        self.population = [Player(depth) for i in range(size)]
        self.games = []
        pass

    def random_pairs(self):
        indices = [i for i in range(len(self.population))]

        pairs = []

        while indices:
            idx1 = random.randrange(0, len(indices))
            player1 = self.population[indices.pop(idx1)]

            idx2 = random.randrange(0, len(indices))
            player2 = self.population[indices.pop(idx2)]

            pairs.append((player1, player2))

        return pairs

    def run_games(self, pairs, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', game_type=GameType.START, reward=GameType.EVEN):
        games = []
        for i, pair in enumerate(pairs):
            games.append(Game(pair[0], pair[1], fen, game_type, f"Game {i}"))

        for g in games:
            g.play()
