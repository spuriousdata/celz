class Workbook(object):
    def __init__(self, f):
        self.data = None
        with open(f, 'rb') as fp:
            self.data = fp.read()
        self.numsheets = 2
