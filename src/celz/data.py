class Selection(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def update(self, row, col):
        self.row = row
        self.col = col


class Spreadsheet(object):
    def __init__(self):
        self.selection = Selection(-1, -1)
        self.colwidth = 10

    def select(self, row, col):
        self.selection.update(row, col)

    def rowcol2yx(self, row, col):
        return row, col*self.colwidth


class Row(object):
    def __init__(self, sheet, row):
        self.sheet = sheet
        self.cells = [Cell(self, x) for x in row]

    def render(self, trunc=10):
        rowdata = ""
        for cell in self.cells:
            rowdata += cell.fmt(trunc) + " "
        return rowdata[:-1]


class Cell(object):
    def __init__(self, row, v):
        self.value = v
        self.row = row

    def fmt(self, trunc):
        s = "%%%ds" % trunc
        return s % self.value[:trunc]


class CSVFile(Spreadsheet):
    def __init__(self, f):
        super(CSVFile, self).__init__()
        self.rows = []
        import csv
        with open(f, 'r') as fp:
            reader = csv.reader(fp)
            for line in reader:
                self.rows.append(Row(self, line))


class Workbook(object):
    def __init__(self, f):
        self.data = None
        self.numsheets = 1
        if f.endswith('.csv'):
            self.spreadsheet = CSVFile(f)
        else:
            raise Exception("Filetype not implemented")
