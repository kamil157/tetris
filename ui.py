import curses
from copy import deepcopy
from curses import wrapper
from time import sleep, time

from tetris import Tetris, num_cols, visible_rows, invisible_rows

block_width = 2
desired_fps = 60


def init_colors():
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Empty space on playfield
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)  # I
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # O
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)  # T
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)  # J
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_GREEN)  # S
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)  # Z
    try:
        color_orange = 166
        curses.init_pair(6, curses.COLOR_WHITE, color_orange)  # L

        color_gray = 250
        curses.init_pair(9, curses.COLOR_WHITE, color_gray)  # ghost

    except curses.error:
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # L
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)  # ghost


def render_tetromino(window, tetromino):
    for y, x in tetromino:
        for i in range(block_width):
            try:
                window.addstr(y - invisible_rows, 2 * x + i, ' ', curses.color_pair(tetromino.color + 1))
            except curses.error:
                pass  # ignore errors, caused by drawing in the last tile or by bugs


class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.init_curses()

        self.game_win = curses.newwin(visible_rows, block_width * num_cols, 0, 0)
        self.info_win = curses.newwin(10, 20, 0, block_width * num_cols)
        self.debug_win = curses.newwin(10, 20, 10, block_width * num_cols)
        self.tetris = Tetris()

        self.pause = False
        self.debug = False

        self.fps_counter = 0
        self.frames_this_second = 0
        self.start_fps_timer = 0

    def init_curses(self):
        init_colors()
        curses.curs_set(False)
        self.stdscr.nodelay(True)

    def get_user_input(self):
        try:
            return self.stdscr.getkey()
        except curses.error:
            return None

    def handle_pause(self, key):
        if key == 'p':
            self.pause = not self.pause

    def handle_debug(self, key):
        if key == 'd':
            self.debug = not self.debug
            self.debug_win.clear()
            self.debug_win.refresh()

    def update_fps_counter(self):
        self.frames_this_second += 1
        if (time() - self.start_fps_timer) > 1:
            self.fps_counter = round(self.frames_this_second / (time() - self.start_fps_timer))
            self.frames_this_second = 0
            self.start_fps_timer = time()

    def render_game(self):
        self.game_win.clear()
        for y, row in enumerate(self.tetris.playfield[invisible_rows:]):
            for x, color in enumerate(row):
                for i in range(block_width):
                    self.game_win.insch(y, 2 * x + i, ' ', curses.color_pair(color + 1))

        if not self.tetris.is_game_over:
            render_tetromino(self.game_win, self.tetris.ghost())
        render_tetromino(self.game_win, self.tetris.active_tetromino)
        self.game_win.refresh()

    def render_info(self):
        self.info_win.clear()
        self.info_win.addstr(0, 0, "Score: {}".format(self.tetris.score))
        self.info_win.addstr(1, 0, "Lines: {}".format(self.tetris.lines))
        self.info_win.addstr(2, 0, "Level: {}".format(self.tetris.level))
        self.info_win.addstr(3, 0, "Next:")

        next_tetromino = deepcopy(self.tetris.next_tetromino)
        next_tetromino.position_y = invisible_rows + 4
        next_tetromino.position_x = 0
        render_tetromino(self.info_win, next_tetromino)
        self.info_win.refresh()

    def render_debug(self, key):
        self.debug_win.clear()
        self.debug_win.addstr(0, 0, "Fps: {}".format(self.fps_counter))
        self.debug_win.addstr(1, 0, "Key: {}".format(key))
        for i, (k, v) in enumerate(self.tetris.debug().items(), start=2):
            self.debug_win.addstr(i, 0, "{}: {}".format(k, v))
        self.debug_win.refresh()

    def show_game_over(self):
        self.stdscr.addstr(8, 4, "GAME OVER!!")
        self.stdscr.addstr(9, 4, "Your score:")
        self.stdscr.addstr(10, 4, "{:^11}".format(self.tetris.score))
        self.stdscr.addstr(11, 4, "Press enter")
        key = self.stdscr.getch()
        while key != 10:
            key = self.stdscr.getch()

    def run(self):
        self.start_fps_timer = time()
        while not self.tetris.is_game_over:
            frame_start = time()

            key = self.get_user_input()
            self.handle_pause(key)
            self.handle_debug(key)
            self.update_fps_counter()

            if not self.pause:
                self.tetris.tick(key)

            self.render_game()
            self.render_info()
            if self.debug:
                self.render_debug(key)

            sleep_time = frame_start + 1 / desired_fps - time()
            if sleep_time > 0:
                sleep(sleep_time)

        self.show_game_over()


def main(stdscr):
    game = Game(stdscr)
    game.run()


if __name__ == '__main__':
    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass
