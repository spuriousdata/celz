import locale
import curses
# from curses import panel
from celz.data import Workbook
from celz.display import Menu, Sheet
from celz.keys import Command

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


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
        curses.curs_set(0)  # hide cursor
        self.menu = Menu(self)
        self.sheet = Sheet(self, self.workbook.spreadsheet, self.menu.height)
        self.display_objects.append(self.menu)
        self.run_forever()

    def maxl(self):
        return curses.LINES - 1

    def maxc(self):
        return curses.COLS - 1

    def move_cursor(self, key):
        sel = self.sheet.datasrc.selection
        x, y = sel.col, sel.row
        if key in Command.UP:
            y = y - 1 if y > 0 else 0
        elif key in Command.DOWN:
            y = y + 1 if y < self.maxl() else self.maxl()
        elif key in Command.LEFT:
            x = x - 1 if x > 0 else 0
        elif key in Command.RIGHT:
            x = x + 1 if x < self.maxc() else self.maxc()
        self.sheet.select(y, x)

    def run_forever(self):
        while True:
            self.stdscr.refresh()
            if self.get_input():
                return

    def get_input(self):
        k = self.stdscr.getch()
        if k in Command.QUIT:
            return True
        elif k in Command.CURMOVE:
            self.move_cursor(k)
        return False

    def refresh(self):
        self.stdscr.refresh()

    def refreshall(self):
        for d in self.display_objects:
            d.refresh()
