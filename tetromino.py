from copy import deepcopy
from random import shuffle


class Tetromino:
    def __init__(self, shape, position_x, position_y, color):
        self.shape = shape
        self.position_y = position_y
        self.position_x = position_x
        self.color = color

    def rotate(self):
        self.shape.reverse()
        self.shape = list(zip(*self.shape))


class TetrominoFactory:
    def __init__(self):
        I = Tetromino([
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ], 3, -1, 1)

        O = Tetromino([
            [1, 1],
            [1, 1],
        ], 4, -1, 2)

        T = Tetromino([
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
        ], 3, -1, 3)

        J = Tetromino([
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0],
        ], 3, -1, 4)

        L = Tetromino([
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0],
        ], 3, -1, 5)

        S = Tetromino([
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0],
        ], 3, -1, 6)

        Z = Tetromino([
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ], 3, -1, 7)

        self.tetrominos = [
            I, O, T, J, L, S, Z
        ]

        self.bag = []

    def refill_bag(self):
        if not self.bag:
            self.bag = deepcopy(self.tetrominos)
            shuffle(self.bag)

    def create(self):
        self.refill_bag()
        return self.bag.pop()

    def next(self):
        self.refill_bag()
        return self.bag[-1]
