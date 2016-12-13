import curses


class Displayable(object):
    def __init__(self, owner):
        self.owner = owner

    def height(self):
        raise NotImplemented()


class Menu(Displayable):
    def __init__(self, owner, stdscr):
        super(Menu, self).__init__(owner)
        self.stdscr = stdscr
        self.menubar = curses.newwin(self.height, curses.COLS)
        self.stdscr.refresh()
        self.menubar.box()
        self.menubar.addstr(1, 1, "| File | Edit | View | Help |",
                            curses.A_REVERSE)
        self.menubar.refresh()

    @property
    def height(self):
        return 3
