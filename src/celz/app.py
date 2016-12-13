import locale
import curses
# from curses import panel
from celz.data import Workbook
from celz.display import Menu

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


class Direction(object):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Keys(object):
    UP = (ord('k'), curses.KEY_UP)
    DOWN = (ord('j'), curses.KEY_DOWN)
    LEFT = (ord('h'), curses.KEY_LEFT)
    RIGHT = (ord('l'), curses.KEY_RIGHT)


class Celz(object):
    def __init__(self, f):
        self.workbook = Workbook(f)
        self.menu = None
        self.datapanel = None
        self.sheetpads = []
        self.display_objects = []
        curses.wrapper(self.run)

    def run(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.move(2, 0)
        """
        self.datapanel = panel.new_panel(self.stdscr)
        self.datapanel.move(3, 0)
        self.datapanel.window().box()
        self.datapanel.top()
        self.datapanel.show()
        # for sheet in range(0, self.workbook.numsheets):
        #     self.sheetpads.append(curses.newpad(1000, 1000)
        """
        self.menu = Menu(self, self.stdscr)
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
        if k == ord('q'):
            return True
        elif k in Keys.DOWN:
            self.move_cursor(Direction.DOWN)
        elif k in Keys.UP:
            self.move_cursor(Direction.UP)
        elif k in Keys.LEFT:
            self.move_cursor(Direction.LEFT)
        elif k in Keys.RIGHT:
            self.move_cursor(Direction.RIGHT)
        return False
