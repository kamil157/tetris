import curses
from curses import wrapper
from time import sleep, time

from copy import deepcopy

from tetris import Game


def render_tetromino(stdscr, tetromino, block_width):
    for y, x in tetromino:
        for i in range(block_width):
            stdscr.addstr(y, 2 * x + i, ' ', curses.color_pair(tetromino.color + 1))


def render(game, stdscr, fps_counter, key):
    stdscr.clear()
    block_width = 2
    grid = game.get_grid()

    # draw grid
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            for i in range(block_width):
                stdscr.addstr(y, 2 * x + i, ' ', curses.color_pair(color + 1))

    render_tetromino(stdscr, game.active_tetromino, block_width)

    stdscr.addstr(0, 20, "Fps: {}".format(fps_counter))
    stdscr.addstr(1, 20, "Key: {}".format(key))
    stdscr.addstr(2, 20, "Score: {}".format(game.get_score()))
    stdscr.addstr(3, 20, "Next:")

    next_tetromino = deepcopy(game.next_tetromino)
    next_tetromino.position_y = 4
    next_tetromino.position_x = 10
    render_tetromino(stdscr, next_tetromino, block_width)

    stdscr.refresh()


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
    game = Game()

    desired_fps = 60
    start_fps = time()
    frames = 0
    fps_counter = 0

    while True:
        frame_start = time()

        # Get user input
        key = None
        stdscr.nodelay(True)
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
        render(game, stdscr, fps_counter, key)

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
