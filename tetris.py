from copy import deepcopy

from tetromino import Tetromino, TetrominoFactory


class Game:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.grid = [self.cols * [0] for _ in range(self.rows)]
        self.tetromino_factory = TetrominoFactory()
        self.active_tetromino = self.tetromino_factory.create()  # type: Tetromino
        self.next_tetromino = self.tetromino_factory.next()  # type: Tetromino
        self.game_over = False
        self.game_time = 0
        self.gravity = 60
        self.next_gravity = self.game_time + self.gravity
        self.score = 0

    def get_grid(self):
        return self.grid

    def get_score(self):
        return self.score

    def is_game_over(self):
        return self.game_over

    def tick(self, key):
        self.game_time += 1
        self.handle_input(key)

        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        clone.position_y += 1
        if self._can_move(clone):
            if self.game_time >= self.next_gravity:  # is == enough?
                self.active_tetromino = clone
                self.next_gravity += self.gravity
        else:  # sliding doesn't work sometimes
            self.land_tetromino()
            if any(self.grid[0]):
                self.game_over = True
                return
            self.clear_lines()
            self.active_tetromino = self.tetromino_factory.create()
            self.next_tetromino = self.tetromino_factory.next()

    def handle_input(self, key):
        tetromino_clone = deepcopy(self.active_tetromino)  # type: Tetromino
        if key == 'KEY_LEFT':
            tetromino_clone.position_x -= 1
        elif key == 'KEY_RIGHT':
            tetromino_clone.position_x += 1
        elif key == 'KEY_DOWN':
            tetromino_clone.position_y += 1
        # TODO wall kick
        elif key == 'z':
            tetromino_clone.rotate_left()
        elif key == 'x':
            tetromino_clone.rotate_right()
        if self._can_move(tetromino_clone):
            self.active_tetromino = tetromino_clone

    def land_tetromino(self):
        for y, x in self.active_tetromino:
            self.grid[y][x] = self.active_tetromino.color

    def _can_move(self, tetromino):
        return all(self.can_be_placed(y, x) for y, x in tetromino)

    def can_be_placed(self, y, x):
        # Check if position is inside grid and doesn't collide with anything
        return 0 <= x < self.cols and y < self.rows and self.grid[y][x] == 0

    def clear_lines(self):
        lines_cleared = [y for y, row in enumerate(self.grid) if all(row)]
        if not lines_cleared:
            return

        self.score += self.line_score(len(lines_cleared))

        # Shift lines
        self.grid = [self.cols * [0] for _ in range(len(lines_cleared))] \
                    + self.grid[:min(lines_cleared)] \
                    + self.grid[max(lines_cleared) + 1:]

    def line_score(self, line_count):
        score_table = [100, 300, 500, 800]
        return score_table[line_count - 1]
