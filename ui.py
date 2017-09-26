import curses
from curses import wrapper
from time import sleep

from tetris import Game


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.curs_set(False)
    game = Game()
    while True:
        stdscr.clear()

        grid = game.get_grid()

        # draw landed pieces
        for y, row in enumerate(grid):
            for x, color in enumerate(row):
                stdscr.addstr(y, 2 * x, ' ', curses.color_pair(color + 1))
                stdscr.addstr(y, 2 * x + 1, ' ', curses.color_pair(color + 1))

        # draw active piece
        piece = game.active_piece
        for y, row in enumerate(piece.shape):
            for x, field in enumerate(row):
                # stdscr.addstr(0, 20, str(y) + str(x))
                pos_x = x + piece.position_x
                pos_y = y + piece.position_y
                if field == 1 and pos_y >= 0:
                    stdscr.addstr(pos_y, 2 * pos_x, ' ', curses.color_pair(piece.color + 1))
                    stdscr.addstr(pos_y, 2 * pos_x + 1, ' ', curses.color_pair(piece.color + 1))

        stdscr.refresh()
        sleep(0.1)
        # stdscr.getkey()
        game.tick()

        if game.is_game_over():
            stdscr.addstr(9, 5, "GAME OVER!")
            stdscr.getkey()




wrapper(main)

