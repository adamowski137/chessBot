import random
import math


class Player():
    def __init__(self, n_of_parameters):
        self.weights = self.__initialize_weights(n_of_parameters)
        pass

    def get_eval(self):
        parameters = [1, 5, 2, -1]  # get parameters from outside

        evaluation = 0

        for w, par in zip(self.weights, parameters):
            evaluation += self.__sigmoid(w*par)

        return get_eval

    def __sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def __initialize_weights(self, n):
        for i in range(n):
            self.weights.append(random.random() * 2 - 1)
