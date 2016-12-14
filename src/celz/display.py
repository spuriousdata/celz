import curses


class Displayable(object):
    def __init__(self, owner):
        self.owner = owner
        self.window = None

    def refresh(self):
        self.owner.refresh()
        self.window.refresh()

    @property
    def height(self):
        raise NotImplemented()


class Menu(Displayable):
    def __init__(self, owner, y=0):
        super(Menu, self).__init__(owner)
        self.window = curses.newwin(self.height, curses.COLS, y, 0)
        self.window.box()
        self.window.addstr(1, 1, "| File | Edit | View | Help |",
                           curses.A_REVERSE)
        self.refresh()

    @property
    def height(self):
        return 3


class Sheet(Displayable):
    def __init__(self, owner, datasrc, y=0):
        self.y = y
        self.datasrc = datasrc
        super(Sheet, self).__init__(owner)
        self.window = curses.newwin(self.height, curses.COLS, y, 0)
        self.window.box()
        self.window.addstr(1, 1, "data blah blah" * 20)
        self.refresh()

    @property
    def height(self):
        return curses.LINES - self.y
