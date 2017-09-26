class Piece:
    shape = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]
    initial_position_x = 3
    initial_position_y = -3
    color = 1

    position_y = initial_position_y
    position_x = initial_position_x


class Game:
    def __init__(self):
        self.rows = 20
        self.cols = 10
        self.grid = [self.cols * [0] for _ in range(self.rows)]
        self.active_piece = Piece()
        self.game_over = False
        self.game_time = 0
        self.gravity = 60
        self.next_gravity = self.game_time + self.gravity

    def get_grid(self):
        return self.grid

    def is_game_over(self):
        return self.game_over

    def tick(self, key):
        self.game_time += 1
        if key == 'KEY_LEFT':
            if self.can_move_left():
                self.active_piece.position_x -= 1
        elif key == 'KEY_RIGHT':
            if self.can_move_right():
                self.active_piece.position_x += 1
        elif key == 'KEY_DOWN':
            if self.can_move_down():
                self.active_piece.position_y += 1

        # TODO magic 15
        if self.active_piece.position_y <= 15 and self.can_move_down():
            if self.game_time >= self.next_gravity:  # is == enough?
                self.active_piece.position_y += 1
                self.next_gravity += self.gravity
        else:  # sliding doesn't work sometimes
            self.land_piece()
            if any(self.grid[0]):
                self.game_over = True
            self.active_piece = Piece()

    def land_piece(self):
        for y, row in enumerate(self.active_piece.shape):
            for x, field in enumerate(row):
                if field == 1:
                    pos_y = self.active_piece.position_y + y
                    pos_x = self.active_piece.position_x + x
                    self.grid[pos_y][pos_x] = 1

    def can_move_down(self):
        for y, row in enumerate(self.active_piece.shape):
            for x, field in enumerate(row):
                if field == 1:
                    pos_y = self.active_piece.position_y + y
                    pos_x = self.active_piece.position_x + x
                    if pos_y == self.rows - 1 or self.grid[pos_y + 1][pos_x] > 0:
                        return False
        return True

    def can_move_left(self):
        for y, row in enumerate(self.active_piece.shape):
            for x, field in enumerate(row):
                if field == 1:
                    pos_y = self.active_piece.position_y + y
                    pos_x = self.active_piece.position_x + x
                    if pos_x == 0 or self.grid[pos_y][pos_x - 1] > 0:
                        return False
        return True

    def can_move_right(self):
        for y, row in enumerate(self.active_piece.shape):
            for x, field in enumerate(row):
                if field == 1:
                    pos_y = self.active_piece.position_y + y
                    pos_x = self.active_piece.position_x + x
                    if pos_x == self.cols - 1 or self.grid[pos_y][pos_x + 1] > 0:
                        return False
        return True
