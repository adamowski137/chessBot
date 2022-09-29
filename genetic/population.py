import random
from multiprocess import Pool

from genetic.player import Player
from genetic.game import Game, GameType


class Population():
    def __init__(self, size, depth):
        self.population = [Player(depth) for i in range(size)]
        self.games = []
        pass

    def random_pairs(self, both_sides=False):
        indices = [i for i in range(len(self.population))]

        pairs = []

        while indices:
            idx1 = random.randrange(0, len(indices))
            player1 = self.population[indices.pop(idx1)]

            idx2 = random.randrange(0, len(indices))
            player2 = self.population[indices.pop(idx2)]

            pairs.append((player1, player2))

        if both_sides:
            for i in range(len(self.population) // 2):
                new_pair = pairs[i][1], pairs[i][0]
                pairs.append(new_pair)

        return pairs

    def run_games(self, pairs, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', game_type=GameType.START, reward=GameType.EVEN):
        self.games = []
        for i, pair in enumerate(pairs):
            self.games.append(
                Game(pair[0], pair[1], fen, game_type, f"Game {i}"))

        with Pool(len(pairs)) as p:
            self.games = p.map(lambda x: x.play(), self.games)

    def save_games(self, path, start_fen):
        for game in self.games:
            game.save(path, start_fen)
