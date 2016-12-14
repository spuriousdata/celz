import locale
import curses
# from curses import panel
from celz.data import Workbook
from celz.display import Menu, Sheet
from celz.keys import K

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


class Direction(object):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Celz(object):
    def __init__(self, f):
        self.workbook = Workbook(f)
        self.menu = None
        self.display_objects = []
        curses.wrapper(self.run)

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.move(2, 0)
        self.menu = Menu(self)
        self.sheet = Sheet(self, self.workbook.spreadsheet, self.menu.height)
        self.display_objects.append(self.menu)
        self.run_forever()

    def maxl(self):
        return curses.LINES - 1

    def maxc(self):
        return curses.COLS - 1

    def move_cursor(self, direction, win=None):
        if win is None:
            win = self.stdscr
        pos = list(win.getyx())
        if direction == Direction.UP:
            pos[0] = pos[0] - 1 if pos[0] > 0 else 0
        elif direction == Direction.DOWN:
            pos[0] = pos[0] + 1 if pos[0] < self.maxl() else self.maxl()
        elif direction == Direction.LEFT:
            pos[1] = pos[1] - 1 if pos[1] > 0 else 0
        elif direction == Direction.RIGHT:
            pos[1] = pos[1] + 1 if pos[1] < self.maxc() else self.maxc()
        self.stdscr.move(*pos)

    def run_forever(self):
        while True:
            self.stdscr.refresh()
            if self.get_input():
                return

    def get_input(self):
        k = self.stdscr.getch()
        if k in K.QUIT:
            return True
        elif k in K.DOWN:
            self.move_cursor(Direction.DOWN)
        elif k in K.UP:
            self.move_cursor(Direction.UP)
        elif k in K.LEFT:
            self.move_cursor(Direction.LEFT)
        elif k in K.RIGHT:
            self.move_cursor(Direction.RIGHT)
        return False

    def refresh(self):
        self.stdscr.refresh()

    def refreshall(self):
        for d in self.display_objects:
            d.refresh()
