import random
from multiprocess import Pool

from genetic.player import Player
from genetic.game import Game, GameType


class Population():
    def __init__(self, size, depth, min_depth):
        self.population = [Player(depth, min_depth) for i in range(size)]
        self.games = []
        self.generation = 0
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
            new_data = p.map(lambda x: x.play(), self.games)
            self.games = [data[0] for data in new_data]
            self.population = []

            for data in new_data:
                for player in data[1]:
                    self.population.append(player)

    def save_games(self, path, start_fen):
        for game in self.games:
            with open(path, 'a+') as f:
                # The indices pairs are always (0,1), (2,3) ... , because of reassignment at run_games()
                f.write(
                    f"\n({self.population.index(game.white)},{self.population.index(game.black)})")
                f.close()
            game.save(path, start_fen)

    def save_population(self, path):
        for player in self.population:
            with open(path, 'a+') as f:
                f.write(f"{player.evaluation_function.weights}\n")
                f.close()
