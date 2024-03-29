from copy import deepcopy

from tetromino import Tetromino, TetrominoFactory

invisible_rows = 20  # type: int
visible_rows = 20  # type: int
total_rows = invisible_rows + visible_rows
num_cols = 10  # type: int


class Tetris:
    def __init__(self):
        self._lines_per_level = 10
        self._tetromino_factory = TetrominoFactory()  # type: TetrominoFactory
        self._gravity_delay = 60
        self._initial_gravity = 30
        self._gravity_per_level = 1
        self._gravity = self._initial_gravity  # type: int
        self._gravity_countdown = self._gravity + self._gravity_delay  # type: int
        self._lock_delay = 30
        self._lock_countdown = 0

        self.playfield = [num_cols * [0] for _ in range(total_rows)]
        self.active_tetromino = self._tetromino_factory.create()  # type: Tetromino
        self.next_tetromino = self._tetromino_factory.next()  # type: Tetromino
        self.is_game_over = False  # type: bool
        self.score = 0  # type: int
        self.level = 0
        self.lines = 0

    def _move_to_bottom(self, tetromino):
        """Move tetromino down as much as possible."""
        while self._is_position_legal(tetromino):
            tetromino.position_y += 1
        tetromino.position_y -= 1

    def debug(self):
        """Return debug info."""
        return {'Gravity': self._gravity,
                'Gravity cd': self._gravity_countdown,
                'Lock cd': self._lock_countdown}

    def ghost(self):
        """Return ghost tetromino."""
        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        self._move_to_bottom(clone)
        clone.color = 8
        return clone

    def tick(self, key):
        """Update game state."""
        self._gravity_countdown -= 1
        self._lock_countdown -= 1
        self._handle_input(key)

        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        clone.position_y += 1
        if self._is_position_legal(clone):
            if self._gravity_countdown == 0:
                self.active_tetromino = clone
                self._gravity_countdown = self._gravity
        else:
            if self._lock_countdown < 0:
                self._lock_countdown = self._lock_delay

        if self._lock_countdown == 0:
            self._lock_tetromino()

            if self._game_over_condition():
                self.is_game_over = True

    def _game_over_condition(self):
        """Check if game is over."""
        return any(self.playfield[y][x] > 0 for y, x in self.active_tetromino)

    def _refresh_lock(self):
        """Refresh or remove lock delay as needed."""
        clone = deepcopy(self.active_tetromino)  # type: Tetromino
        clone.position_y += 1
        if self._is_position_legal(clone):
            self._lock_countdown = -1
        else:
            self._lock_countdown = self._lock_delay
            self._gravity_countdown = self._gravity

    def _handle_input(self, key):
        """Perform action specified by pressed key."""
        tetromino_clone = deepcopy(self.active_tetromino)  # type: Tetromino
        self._handle_shift(key, tetromino_clone)
        self._handle_drop(key, tetromino_clone)
        self._handle_rotation(key, tetromino_clone)

    def _handle_rotation(self, key, tetromino_clone):
        """Handle clockwise/counter-clockwise rotations."""
        if key == 'z':
            tetromino_clone.rotate_counter_clockwise()
        elif key == 'x':
            tetromino_clone.rotate_clockwise()
        else:
            return
        self._wall_kick(tetromino_clone)

    def _wall_kick(self, rotated_tetromino):
        """Try specified wall kicks until one works or none is possible."""
        wall_kicks_x = [0, 1, -1]
        for x in wall_kicks_x:
            clone = deepcopy(rotated_tetromino)  # type: Tetromino
            clone.position_x += x

            if self._is_position_legal(clone):
                self.active_tetromino = clone
                self._refresh_lock()
                return

    def _handle_shift(self, key, tetromino_clone):
        """Handle left and right shifts."""
        if key == 'KEY_LEFT':
            tetromino_clone.position_x -= 1
        elif key == 'KEY_RIGHT':
            tetromino_clone.position_x += 1
        else:
            return
        if self._is_position_legal(tetromino_clone):
            self.active_tetromino = tetromino_clone
            self._refresh_lock()

    def _handle_drop(self, key, tetromino_clone):
        """Handle soft and hard drops."""
        if key == 'KEY_DOWN':
            tetromino_clone.position_y += 1
            if self._is_position_legal(tetromino_clone):
                self.active_tetromino = tetromino_clone
                self.score += 1
        elif key == ' ':
            start = tetromino_clone.position_y
            self._move_to_bottom(tetromino_clone)
            self.active_tetromino = tetromino_clone
            end = tetromino_clone.position_y
            self.score += 2 * (end - start)
            self._lock_countdown = 0

    def _lock_tetromino(self):
        """Lock tetromino on the playfield."""
        for y, x in self.active_tetromino:
            self.playfield[y][x] = self.active_tetromino.color

        self._clear_lines()
        self.level = self.lines // self._lines_per_level
        self._gravity = max(1, int(self._initial_gravity - self._gravity_per_level * self.level))
        self.active_tetromino = self._tetromino_factory.create()
        self.next_tetromino = self._tetromino_factory.next()
        self._gravity_countdown = self._gravity + self._gravity_delay

    def _is_position_legal(self, tetromino):
        """Check if tetromino position is legal."""
        return all(self._can_be_placed(y, x) for y, x in tetromino)

    def _can_be_placed(self, y, x):
        """Check if position is inside playfield and doesn't collide with anything."""
        return 0 <= x < num_cols and y < total_rows and self.playfield[y][x] == 0

    def _clear_lines(self):
        """Remove full lines from playfield."""
        lines_cleared = [y for y, row in enumerate(self.playfield) if all(row)]

        score_table = [0, 100, 300, 500, 800]
        self.score += score_table[len(lines_cleared)]
        self.lines += len(lines_cleared)

        # Shift lines
        for line in lines_cleared:
            self.playfield[:line + 1:] = [num_cols * [0]] + self.playfield[:line]
