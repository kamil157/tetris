import curses
from curses import wrapper
from time import sleep, time

from copy import deepcopy

from tetris import Game

block_width = 2


def render_tetromino(stdscr, tetromino):
    for y, x in tetromino:
        for i in range(block_width):
            stdscr.insch(y, 2 * x + i, ' ', curses.color_pair(tetromino.color + 1))


def render_game(game, game_win):
    game_win.clear()

    # draw grid
    for y, row in enumerate(game.get_grid()):
        for x, color in enumerate(row):
            for i in range(block_width):
                game_win.insch(y, 2 * x + i, ' ', curses.color_pair(color + 1))

    render_tetromino(game_win, game.active_tetromino)

    game_win.refresh()


def render_info(game, fps_counter, key, info_win):
    info_win.clear()

    info_win.addstr(0, 0, "Fps: {}".format(fps_counter))
    info_win.addstr(1, 0, "Key: {}".format(key))
    info_win.addstr(2, 0, "Score: {}".format(game.get_score()))
    info_win.addstr(3, 0, "Next:")

    next_tetromino = deepcopy(game.next_tetromino)
    next_tetromino.position_y = 4
    next_tetromino.position_x = 0
    render_tetromino(info_win, next_tetromino)

    info_win.refresh()


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

    game_win = curses.newwin(game.rows, 2 * game.cols, 0, 0)
    info_win = curses.newwin(game.rows, 10, 0, 2 * game.cols)

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

        render_game(game, game_win)
        render_info(game, fps_counter, key, info_win)

        sleep_time = frame_start + 1 / desired_fps - time()
        if sleep_time > 0:
            sleep(sleep_time)

        if game.is_game_over():
            break

    # Game over
    stdscr.addstr(9, 5, "GAME OVER!")
    stdscr.addstr(10, 5, "Press enter")
    stdscr.nodelay(False)
    key = stdscr.getch()
    while key != 10:
        key = stdscr.getch()


wrapper(main)
