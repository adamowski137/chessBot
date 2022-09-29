import argparse
import math
import time
from timeit import default_timer as timer
import os
import glob

import chess
import chess.pgn

from tree.tree import Tree
from static_evaluation.static_evaluation import static_evaluation_function
from genetic.population import Population
from genetic.player import Player
from genetic.game import Game


def simple_play(args):
    white_player = Player(args.depth) if args.self_play else None
    black_player = Player(args.depth)

    game = Game(white_player, black_player, display=args.display)

    game.play()

    if args.save_games:
        game.save("games.txt", args.fen)


def genetic_algorithm(args):
    population = Population(args.population_size, args.depth)
    pairs = population.random_pairs(both_sides=False)

    population.run_games(pairs, fen=args.fen)

    if args.save_games:
        files = glob.glob(f"{args.out}/*")
        for f in files:
            os.remove(f)

        population.save_population(
            os.path.join(args.out, "population.txt"))
        population.save_games(os.path.join(args.out, "games.txt"), args.fen)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chess bot")

    # Values
    parser.add_argument('-f', '--fen', help="Name of the input XML file.",
                        default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', required=False)
    parser.add_argument('-d', '--depth', help="Maximum search depth.",
                        default=16, type=float, required=False)
    parser.add_argument('-p', '--population-size',
                        help="Population size. Must be even and at least 2.", default=0, type=int)
    parser.add_argument('-o', '--out', help="Directory to save output files.", type=str,
                        default='./out/', required=False)

    # Flags
    parser.add_argument('--display', dest="display",
                        help="Run the UI", action='store_true')
    parser.add_argument('--self-play', dest="self_play",
                        help="Play the game against itself.", action='store_true')
    parser.add_argument('--save-games', dest="save_games",
                        help="Save played games into a file.", action='store_true')

    # Default flags
    parser.set_defaults(display=False)
    parser.set_defaults(self_play=False)
    parser.set_defaults(save_games=False)

    args = parser.parse_args()

    if args.population_size > 1:
        genetic_algorithm(args)
    else:
        simple_play(args)
