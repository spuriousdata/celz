import locale
import curses
from curses import panel
from celz.data import Workbook

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
        self.datapanel = None
        self.sheetpads = []
        curses.wrapper(self.run)

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        """
        self.datapanel = panel.new_panel(self.stdscr)
        self.datapanel.move(3, 0)
        self.datapanel.window().box()
        self.datapanel.top()
        self.datapanel.show()
        # for sheet in range(0, self.workbook.numsheets):
        #     self.sheetpads.append(curses.newpad(1000, 1000)
        """
        self.setupmenu()
        self.run_forever()

    def setupmenu(self):
        self.stdscr.addstr(0, 0, "File | Edit | View | Blah | Blah | Blah")
        self.stdscr.refresh()

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
            self.interpret_key(self.stdscr.getkey())

    def interpret_key(self, k):
            if k == 'q':
                raise SystemExit
            elif k == 'j':
                self.move_cursor(Direction.DOWN)
            elif k == 'k':
                self.move_cursor(Direction.UP)
            elif k == 'h':
                self.move_cursor(Direction.LEFT)
            elif k == 'l':
                self.move_cursor(Direction.RIGHT)
