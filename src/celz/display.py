import curses
import logging
from collections import namedtuple

logger = logging.getLogger()

Scroll = namedtuple('Scoll', ['y', 'x'])


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
        rows = self.datasrc.rowmgr.rowcount+10
        self.rows = rows
        cols = self.datasrc.rowmgr.rowwidth+1
        self.cols = cols
        self.window = curses.newpad(rows, cols)
        self.scroll = Scroll(0, 0)
        rownum = 0
        for row in self.datasrc.rowmgr.rows:
            try:
                self.window.addstr(rownum, 1, row.render())
            except:
                logger.critical("addstr(%d, 1, \"%s\") rowcount: %d, "
                                "strlen: %d, colcount: %d", rownum,
                                row.render(), rows, len(row.render()), cols)
                raise
            if rownum == 0:
                self.window.hline(1, 1, curses.ACS_HLINE, cols)
                rownum += 1
            rownum += 1
        for x in range(11, cols, 11):
            self.window.vline(0, x, curses.ACS_VLINE, rows)
        self.refresh()

    def addscroll(self, r=0, c=0):
        self.setscroll(self.scroll.y+r, self.scroll.x+c)

    def setscroll(self, r, c):
        self.scroll = Scroll(max(0, r), max(0, c))

    @property
    def height(self):
        return curses.LINES - self.y

    @property
    def width(self):
        return curses.COLS - 2

    @property
    def bottom(self):
        return self.scroll.y + (self.height - 2)

    @property
    def right(self):
        return self.scroll.x + self.width

    def refresh(self):
        super(Sheet, self).refresh(False)
        logger.debug("refresh(%d, %d, %d, %d, %d, %d)", self.scroll.y,
                     self.datasrc.rowmgr.leftof(self.scroll.x), self.y, 0,
                     self.height, self.width)
        self.window.refresh(self.scroll.y,
                            self.datasrc.rowmgr.leftof(self.scroll.x), self.y,
                            0, self.height, self.width)

    def hscroll(self, direction):
        """ direction should be 1 or -1 """
        self.addscroll(0, direction)
        logger.debug("Scrolling to (%d, %d)", *self.scroll)
        self.refresh()

    def vscroll(self, direction):
        """ direction should be 1 or -1 """
        self.addscroll(direction, 0)
        logger.debug("Scrolling to (%d, %d)", *self.scroll)
        self.refresh()

    def select(self, row, col):
        if self.scroll == (0, 0) and -1 in (row, col):
            row, col = (0, 0)
        if row > self.datasrc.rowmgr.rowcount or \
                col > self.datasrc.rowmgr.colcount:
            return
        logger.debug("row: %d < rows: %d & col: %d < cols: %d",
                     row, self.datasrc.rowmgr.rowcount, col,
                     self.datasrc.rowmgr.colcount)
        dirty = False
        oldsel = self.datasrc.selection
        if -1 not in (oldsel.row, oldsel.col):
            span = self.datasrc.get_span(oldsel.row, oldsel.col)
            try:
                self.window.chgat(span.y, span.x, span.len, 0)
                dirty = True
            except:
                pass

        span = self.datasrc.select(row, col)
        logger.debug("Moving selection to row: %d, col: %d, y: %d, x: %d",
                     row, col, span.y, span.x)
        if span.x > self.right:
            logger.debug("Scrolling right, span.x: %d > self.right: %d",
                         span.x, self.right)
            self.hscroll(1)
            dirty = True
        elif span.x < self.datasrc.rowmgr.leftof(self.scroll.x):
            logger.debug("Scrolling left, span.x: %d < self.scroll.x: %d",
                         span.x, self.scroll.x)
            self.hscroll(-1)
            dirty = True
        elif span.y > self.bottom:
            logger.debug("Scrolling down, span.y: %d > self.bottom: %d",
                         span.y, self.bottom)
            self.vscroll(1)
            dirty = True
        elif span.y < self.scroll.y:
            logger.debug("Scrolling up, span.y: %d < self.scroll.y(%d)",
                         span.y, self.scroll.y)
            self.vscroll(-1)
            dirty = True
        else:
            logger.debug("Not Scrolling -- span.x(%d), span.y(%d) "
                         "self.width(%d), self.height(%d), self.bottom(%d), "
                         "self.y(%d), self.right(%d), self.scroll(%d, %d)",
                         span.x, span.y, self.width, self.height, self.bottom,
                         self.y, self.bottom, *self.scroll)
        try:
            self.window.chgat(span.y, span.x, span.len, curses.A_STANDOUT)
            dirty = True
        except:
            pass
        if dirty:
            self.refresh()
