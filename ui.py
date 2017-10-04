import curses
from curses import wrapper
from functools import wraps
from time import sleep, time

from copy import deepcopy

from tetris import Game, num_cols, num_rows

block_width = 2


def render_tetromino(stdscr, tetromino):
    for y, x in tetromino:
        for i in range(block_width):
            stdscr.addstr(y, 2 * x + i, ' ', curses.color_pair(tetromino.color + 1))


def repaint(func):
    @wraps(func)
    def func_wrapper(window, *args, **kwargs):
        window.clear()
        func(window, *args, **kwargs)
        window.refresh()

    return func_wrapper


@repaint
def render_game(game_win, game):
    for y, row in enumerate(game.playfield):
        for x, color in enumerate(row):
            for i in range(block_width):
                game_win.insch(y, 2 * x + i, ' ', curses.color_pair(color + 1))

    render_tetromino(game_win, game.active_tetromino)


@repaint
def render_info(info_win, game, fps_counter, key):
    info_win.addstr(0, 0, "Fps: {}".format(fps_counter))
    info_win.addstr(1, 0, "Key: {}".format(key))
    info_win.addstr(2, 0, "Score: {}".format(game.score))
    info_win.addstr(3, 0, "Next:")

    next_tetromino = deepcopy(game.next_tetromino)
    next_tetromino.position_y = 4
    next_tetromino.position_x = 0
    render_tetromino(info_win, next_tetromino)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)  # I
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)  # O
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_MAGENTA)  # T
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)  # J

    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_GREEN)  # S
    curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_RED)  # Z

    try:
        color_orange = 166
        curses.init_pair(6, curses.COLOR_WHITE, color_orange)  # L

    except curses.error:
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # L

    curses.curs_set(False)
    stdscr.nodelay(True)
    game = Game()

    desired_fps = 60
    start_fps = time()
    frames = 0
    fps_counter = 0

    game_win = curses.newwin(num_rows, block_width * num_cols, 0, 0)
    info_win = curses.newwin(num_rows, 20, 0, block_width * num_cols)

    while True:
        frame_start = time()

        # Get user input
        key = None
        try:
            key = stdscr.getkey()
        except curses.error:
            pass

        # Update fps counter
        frames += 1
        if (time() - start_fps) > 1:
            fps_counter = round(frames / (time() - start_fps))
            frames = 0
            start_fps = time()

        game.tick(key)

        render_game(game_win, game)
        render_info(info_win, game, fps_counter, key)

        sleep_time = frame_start + 1 / desired_fps - time()
        if sleep_time > 0:
            sleep(sleep_time)

        if game.is_game_over:
            break

    # Game over
    stdscr.addstr(9, 5, "GAME OVER!")
    stdscr.addstr(10, 5, "Press enter")
    stdscr.nodelay(False)
    key = stdscr.getch()
    while key != 10:
        key = stdscr.getch()


if __name__ == '__main__':
    wrapper(main)
