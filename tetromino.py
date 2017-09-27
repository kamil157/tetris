from copy import copy
from random import choice


class Tetromino:
    def __init__(self, shapes, position_x, position_y, color):
        self.rotation_index = 0
        self.shapes = shapes
        self.current_shape = shapes[self.rotation_index]
        self.position_y = position_y
        self.position_x = position_x
        self.color = color

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.shapes)
        self.current_shape = self.shapes[self.rotation_index]

        # TODO wall kick crashes


class TetrominoFactory:
    def __init__(self):
        I = Tetromino([
            [
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 0],
            ],
            [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 1, 1, 1],
                [0, 0, 0, 0],
            ],
        ], 3, -3, 1)

        O = Tetromino([
            [
                [1, 1],
                [1, 1],
            ],
        ], 3, -3, 2)

        T = Tetromino([
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 1, 0],
            ],
            [
                [0, 1, 0],
                [1, 1, 0],
                [0, 1, 0],
            ],
            [
                [0, 1, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 1, 0],
            ],
        ], 3, -3, 3)

        J = Tetromino([
            [
                [0, 0, 0],
                [1, 1, 1],
                [0, 0, 1],
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 0],
            ],
            [
                [1, 0, 0],
                [1, 1, 1],
                [0, 0, 0],
            ],
            [
                [0, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ],
        ], 3, -3, 4)

        L = Tetromino([
            [
                [0, 0, 0],
                [1, 1, 1],
                [1, 0, 0],
            ],
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
            ],
            [
                [0, 0, 1],
                [1, 1, 1],
                [0, 0, 0],
            ],
            [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 1],
            ],
        ], 3, -3, 5)

        S = Tetromino([
            [
                [0, 0, 0],
                [0, 1, 1],
                [1, 1, 0],
            ],
            [
                [0, 1, 0],
                [0, 1, 1],
                [0, 0, 1],
            ],
        ], 3, -3, 6)

        Z = Tetromino([
            [
                [0, 0, 0],
                [1, 1, 0],
                [0, 1, 1],
            ],
            [
                [0, 0, 1],
                [0, 1, 1],
                [0, 1, 0],
            ],
        ], 3, -3, 7)

        self.tetrominos = [
            I, O, T, J, L, S, Z
        ]

    def create(self):
        return copy(choice(self.tetrominos))


def new_tetromino():
    new_tetromino.factory = TetrominoFactory()
    return new_tetromino.factory.create()
