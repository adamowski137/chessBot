
import random
import math
import numpy as np
import chess
import matplotlib.pyplot as plt

#from tree.tree import *
#from static_evaluation.static_evaluation import *


"""
Leave it here

indexing of squares:
1 56            63
2
3
4
5
6
7
8 0             7
  a b c d e f g h

"""





class Heatmap:
    def __init__(self, core = [[random.uniform(0,1) for i in range(8)] for j in range(8)]):
            self.core = core

    def __getitem__(self, index):
        if type(index) is tuple:
            return self.core[index[0]][index[1]]
        else:
            return self.core[index//8][index % 8]

    def __setitem__(self, index, item):
        if type(index) is tuple:
            self.core[index[0]][index[1]] = item
        else:
            self.core[index//8][index % 8] = item

    def __str__(self):
        out = ""
        for i in range(8):
            for j in range(8):
                out += f"{self[7 - i, j]} "
            out += "\n"
        return out

    def view(self):
        plt.imshow(self.core, cmap='hot', interpolation='nearest')
        plt.show()




class Params:
    def __init__(self, period):
        assert period in ["opening", "midgame", "endgame"]
        self.period = period #opening, midgame or endgame
        self.control_heatmap = 0


class Player():
    def __init__(self, depth):
        self.tree = Tree(depth, static_evaluation_function)
        self.fitness = 0


def main():
    print(type((1,2)))
    heatmap = Heatmap()
    heatmap.view()

if __name__ == "__main__":
    main()



