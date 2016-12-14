import string
import curses


class Key(object):
    pass


K = Key()

L = dict([(k, ord(k)) for k in string.ascii_uppercase + string.ascii_lowercase])

K.UP = (ord('k'), curses.KEY_UP)
K.DOWN = (ord('j'), curses.KEY_DOWN)
K.LEFT = (ord('h'), curses.KEY_LEFT)
K.RIGHT = (ord('l'), curses.KEY_RIGHT)
K.QUIT = (L['q'],)
