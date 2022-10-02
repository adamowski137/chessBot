import random
import math
import numpy as np

from tree.tree import *
from static_evaluation.static_evaluation import *


def sigmoid(x):
    if x >= 0:
        return 1 / (1 + np.exp(-x))
    else:
        return 1 - 1/(1 + np.exp(x))


class Player():
    def __init__(self, depth, weights=None, show_branch=False):
        self.evaluation_function = Evaluation(weights)
        self.tree = Tree(depth, self.evaluation_function,
                         show_branch=show_branch)
        self.fitness = 0

    def move(self, board):
        return self.tree.iterative_dfs(board)

    def mutate(self, size):
        for key, val in self.evaluation_function.weights.items():
            sd = val * size / 3  # 97.5% ze zmieini sie o max (100*size)%
            diff = random.gauss(0, sd)
            self.evaluation_function.weights[key] = val + diff

    def get_weights(self):
        return self.evaluation_function.weights

    def get_depth(self):
        return self.tree.depth

    @staticmethod
    def create_offspring(parents, mutation_chance, mutation_size):
        if not parents:
            print("Created a default offspring, because no parents were provided.")
            return Player()
        new_weights = dict()
        for key in parents[0].get_weights():
            val = 0
            for p in parents:
                val += p.get_weights()[key]
            new_weights[key] = val / len(parents)

        player = Player(parents[0].get_depth(), new_weights)

        if random.uniform(0, 1) < mutation_chance:
            player.mutate(mutation_size)

        return player


class NN:
    class Layer:
        def __init__(self, my_size, previous_size):

            # my_size is number of nodes in this layer
            self.my_size = my_size

            # previous_size is number of nodes in preceding layer
            self.previous_size = previous_size

            self.weights = np.ndarray((my_size, previous_size))
            self.biases = np.ndarray((my_size))
            self.activation = sigmoid

        def __str__(self):
            out = ''
            out += f"Layer(Nodes: {self.my_size},"
            out += f" Weights: {self.my_size} x {self.previous_size}, "
            out += f"Biases: {self.my_size})"
            return out

        def feed(self, data):
            """
            put data and get result
            """
            return np.vectorize(self.activation)(self.weights @ data + self.biases)

        def set_weights(self, array):
            arr = np.array(array)
            if self.weights.shape != arr.shape:
                print(f"""ERROR: Shapes of weights does not match, 
                should be {(self.weights.shape)} but got {(arr.shape)}""")
                raise ValueError
            self.weights = arr

        def set_biases(self, array):
            arr = np.array(array)
            if self.biases.shape != arr.shape:
                print(f"""ERROR: Shapes of biases does not match, 
                should be {(self.biases.shape)} but got {(arr.shape)}""")
                raise ValueError
            self.biases = arr

    def __init__(self, structure):
        """
        Structure is a numpy 1-D array containing sizes of layers
        Where 0th element is input layer and last element is output layer
        """

        # Creating table of layers, without input layer, as we count it as non-existing
        self.layers = np.array([self.Layer(structure[i], structure[i - 1])
                                for i in range(1, len(structure))])

    def __str__(self):
        out = ''
        for layer in self.layers:
            out += "\n\n"
            out += str(layer)
            out += "\nWeights:\n"
            out += str(layer.weights)
            out += "\nBiases\n"
            out += str(layer.biases)
        return out

    def __getitem__(self, index):
        return self.layers[index]

    def __call__(self, data):
        """
        function that gets 1-D array of size of the input layer and returns the answer
        (1-D array of size of the output layer)
        """
        answer = np.array(data)
        for layer in self.layers:
            answer = layer.feed(answer)
        return answer
