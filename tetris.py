from copy import deepcopy
from typing import List

from tetromino import Tetromino, TetrominoFactory

num_rows = 20  # type: int
num_cols = 10  # type: int

Playfield = List[List[int]]


class Game:
    def __init__(self):
        self._tetromino_factory = TetrominoFactory()  # type: TetrominoFactory
        self._gravity_delay = 60
        self._gravity = 30  # type: int
        self._gravity_countdown = self._gravity + self._gravity_delay  # type: int

        self.playfield = [num_cols * [0] for _ in range(num_rows)]  # type: Playfield
        self.active_tetromino = self._tetromino_factory.create()  # type: Tetromino
        self.next_tetromino = self._tetromino_factory.next()  # type: Tetromino
        self.is_game_over = False  # type: bool
        self.score = 0  # type: int

    def _move_to_bottom(self, tetromino):
        while self._can_move(tetromino):
            tetromino.position_y += 1
        tetromino.position_y -= 1

    def ghost(self):
        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        self._move_to_bottom(clone)
        clone.color = 8
        return clone

    def tick(self, key):
        self._gravity_countdown -= 1
        self._handle_input(key)

        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        clone.position_y += 1
        if self._can_move(clone):
            if self._gravity_countdown == 0:
                self.active_tetromino = clone
                self._gravity_countdown = self._gravity
        else:
            self._land_tetromino()
            if any(self.playfield[0]):
                self.is_game_over = True
                return
            self._clear_lines()
            self.active_tetromino = self._tetromino_factory.create()
            self.next_tetromino = self._tetromino_factory.next()
            self._gravity_countdown = self._gravity + self._gravity_delay

    def _handle_input(self, key):
        tetromino_clone = deepcopy(self.active_tetromino)  # type: Tetromino
        if key == 'KEY_LEFT':
            tetromino_clone.position_x -= 1
        elif key == 'KEY_RIGHT':
            tetromino_clone.position_x += 1
        elif key == 'KEY_DOWN':
            tetromino_clone.position_y += 1
        elif key == ' ':
            self._move_to_bottom(tetromino_clone)

        # TODO wall kick
        elif key == 'z':
            tetromino_clone.rotate_counter_clockwise()
        elif key == 'x':
            tetromino_clone.rotate_clockwise()
        if self._can_move(tetromino_clone):
            self.active_tetromino = tetromino_clone

    def _land_tetromino(self):
        for y, x in self.active_tetromino:
            self.playfield[y][x] = self.active_tetromino.color

    def _can_move(self, tetromino):
        return all(self._can_be_placed(y, x) for y, x in tetromino)

    def _can_be_placed(self, y, x):
        # Check if position is inside visible playfield and doesn't collide with anything
        return 0 <= x < num_cols and y < num_rows and self.playfield[y][x] == 0

    def _clear_lines(self):
        lines_cleared = [y for y, row in enumerate(self.playfield) if all(row)]
        if not lines_cleared:
            return

        score_table = [100, 300, 500, 800]
        self.score += score_table[len(lines_cleared) - 1]

        # Shift lines
        self.playfield = [num_cols * [0] for _ in range(len(lines_cleared))] \
                         + self.playfield[:min(lines_cleared)] \
                         + self.playfield[max(lines_cleared) + 1:]
