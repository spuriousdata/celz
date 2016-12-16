import curses
import logging

logger = logging.getLogger()


class Displayable(object):
    def __init__(self, owner):
        self.owner = owner
        self.window = None

    def refresh(self, dowindow=True):
        self.owner.refresh()
        if dowindow:
            self.window.refresh()

    @property
    def height(self):
        raise NotImplemented()


class Menu(Displayable):
    def __init__(self, owner, y=0):
        super(Menu, self).__init__(owner)
        self.window = curses.newwin(self.height, curses.COLS, y, 0)
        self.window.addstr(0, 1, "| File | Edit | View | Help |",
                           curses.A_REVERSE)
        self.refresh()

    @property
    def height(self):
        return 2


class Sheet(Displayable):
    def __init__(self, owner, datasrc, y=0):
        self.y = y
        self.datasrc = datasrc
        super(Sheet, self).__init__(owner)
        self.window = curses.newpad(1000, 1000)
        rownum = 0
        for row in self.datasrc.rows:
            self.window.addstr(rownum, 1, row.render())
            if rownum == 0:
                self.window.hline(1, 1, curses.ACS_HLINE, curses.COLS)
                rownum += 1
            rownum += 1
            if rownum == (self.height-1):
                break
        for x in range(11, curses.COLS, 11):
            self.window.vline(0, x, curses.ACS_VLINE, self.height)
        self.refresh()

    @property
    def height(self):
        return curses.LINES - self.y

    def refresh(self):
        super(Sheet, self).refresh(False)
        self.window.refresh(0, 0, self.y, 0, self.height, curses.COLS-2)

    def select(self, row, col):
        oldsel = self.datasrc.selection
        if -1 not in (oldsel.row, oldsel.col):
            y, x, span = self.datasrc.rowcol2yx(oldsel.row, oldsel.col)
            self.window.chgat(y, x, span, 0)

        self.datasrc.selection.update(row, col)
        y, x, span = self.datasrc.rowcol2yx(row, col)
        logger.debug("Moving mouse to row: %d, col: %d, x: %d, y: %d",
                     row, col, y, x)
        self.window.chgat(y, x, span, curses.A_STANDOUT)
        self.refresh()
