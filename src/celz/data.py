class Selection(object):
    class Span(object):
        def __init__(self, y, x, len):
            self.y = y
            self.x = x
            self.len = len

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def update(self, row, col):
        self.row = row
        self.col = col


class Spreadsheet(object):

    def __init__(self):
        self.rowmgr = RowManager()
        self.selection = Selection(-1, -1)

    def select(self, row, col):
        self.selection.update(row, col)
        return self.get_span(row, col)

    def get_span(self, row, col):
        return Selection.Span(row+2,
                              (col*(self.rowmgr.colwidth(col)+1))+1,
                              self.rowmgr.colwidth(col))

    def addrow(self, row):
        self.rowmgr.addrow(row)


class RowManager(object):
    def __init__(self, default_width=10):
        self.default_width = default_width
        self.columns = []
        self.rows = []

    def addrow(self, row):
        d = len(row.cells) - len(self.columns)
        if d > 0:
            for x in range(0, d):
                self.columns.append(self.default_width)
        self.rows.append(row)

    def colwidth(self, col):
        try:
            return self.columns[col]
        except IndexError:
            self.columns.append(self.default_width)
            return self.default_width

    def leftof(self, col):
        return sum(self.columns[:col])

    @property
    def rowwidth(self):
        return sum(self.columns)

    @property
    def rowcount(self):
        return len(self.rows)

    @property
    def colcount(self):
        return len(self.columns)


class Row(object):
    def __init__(self, sheet, row):
        self.sheet = sheet
        self.cells = [Cell(self, row[x], self.sheet.rowmgr.colwidth(x))
                      for x in range(0, len(row))]

    def render(self):
        rowdata = ""
        for cell in self.cells:
            rowdata += cell.fmt() + " "
        return rowdata[:-1]


class Cell(object):
    def __init__(self, row, v, trunc):
        self.value = v
        self.row = row
        self.trunc = trunc

    def fmt(self):
        s = "%%%ds" % self.trunc
        return s % self.value[:self.trunc]


class CSVFile(Spreadsheet):
    def __init__(self, f):
        super(CSVFile, self).__init__()
        import csv
        with open(f, 'r') as fp:
            reader = csv.reader(fp)
            for line in reader:
                self.addrow(Row(self, line))


class Workbook(object):
    def __init__(self, f):
        self.data = None
        self.numsheets = 1
        if f.endswith('.csv'):
            self.spreadsheet = CSVFile(f)
        else:
            raise Exception("Filetype not implemented")
