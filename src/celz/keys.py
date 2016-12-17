import string
import curses


def append_tuples(*args):
    t = []
    for x in args:
        t += list(x)
    return tuple(t)


class Key(object):
    pass


K = Key()

K.__dict__.update(dict([(k, ord(k)) for k in string.ascii_uppercase +
                        string.ascii_lowercase]))

K.UP = curses.KEY_UP
K.DOWN = curses.KEY_DOWN
K.LEFT = curses.KEY_LEFT
K.RIGHT = curses.KEY_RIGHT


class Command(object):
    UP = (K.k, K.UP)
    DOWN = (K.j, K.DOWN)
    LEFT = (K.h, K.LEFT)
    RIGHT = (K.l, K.RIGHT)
    CURMOVE = append_tuples(UP, DOWN, LEFT, RIGHT)
    QUIT = (K.q,)
