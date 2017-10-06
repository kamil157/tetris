import curses
from curses import wrapper
from functools import wraps
from time import sleep, time

from copy import deepcopy

from tetris import Game, num_cols, num_rows

block_width = 2


def render_tetromino(stdscr, tetromino):
    for y, x in tetromino:
        if y >= 0:
            for i in range(block_width):
                try:
                    stdscr.addstr(y, 2 * x + i, ' ', curses.color_pair(tetromino.color + 1))
                except curses.error:
                    pass  # ignore errors, caused by drawing in the last tile or by bugs


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

    if not game.is_game_over:
        render_tetromino(game_win, game.ghost())
    render_tetromino(game_win, game.active_tetromino)


@repaint
def render_info(info_win, game):
    info_win.addstr(0, 0, "Score: {}".format(game.score))
    info_win.addstr(1, 0, "Lines: {}".format(game.lines))
    info_win.addstr(2, 0, "Level: {}".format(game.level))
    info_win.addstr(3, 0, "Next:")

    next_tetromino = deepcopy(game.next_tetromino)
    next_tetromino.position_y = 4
    next_tetromino.position_x = 0
    render_tetromino(info_win, next_tetromino)


@repaint
def render_debug(info_win, game, fps_counter, key):
    info_win.addstr(0, 0, "Fps: {}".format(fps_counter))
    info_win.addstr(1, 0, "Key: {}".format(key))
    for i, (k, v) in enumerate(game.debug().items(), start=2):
        info_win.addstr(i, 0, "{}: {}".format(k, v))


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

        color_gray = 250
        curses.init_pair(9, curses.COLOR_WHITE, color_gray)  # ghost

    except curses.error:
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # L
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)  # ghost

    curses.curs_set(False)
    stdscr.nodelay(True)
    game = Game()

    desired_fps = 60
    start_fps = time()
    frames = 0
    fps_counter = 0

    game_win = curses.newwin(num_rows, block_width * num_cols, 0, 0)
    info_win = curses.newwin(10, 20, 0, block_width * num_cols)
    debug_win = curses.newwin(10, 20, 10, block_width * num_cols)

    pause = False
    debug = False
    while True:
        frame_start = time()

        # Get user input
        key = None
        try:
            key = stdscr.getkey()
        except curses.error:
            pass

        if key == 'p':
            pause = not pause

        if key == 'd':
            debug = not debug
            debug_win.clear()
            debug_win.refresh()

        # Update fps counter
        frames += 1
        if (time() - start_fps) > 1:
            fps_counter = round(frames / (time() - start_fps))
            frames = 0
            start_fps = time()

        if not pause:
            game.tick(key)

        render_game(game_win, game)
        render_info(info_win, game)
        if debug:
            render_debug(debug_win, game, fps_counter, key)

        sleep_time = frame_start + 1 / desired_fps - time()
        if sleep_time > 0:
            sleep(sleep_time)

        if game.is_game_over:
            break

    # Game over
    stdscr.addstr(8, 4, "GAME OVER!!")
    stdscr.addstr(9, 4, "Your score:")
    stdscr.addstr(10, 4, "{:^11}".format(game.score))
    stdscr.addstr(11, 4, "Press enter")
    key = stdscr.getch()
    while key != 10:
        key = stdscr.getch()


if __name__ == '__main__':
    try:
        wrapper(main)
    except KeyboardInterrupt:
        pass
