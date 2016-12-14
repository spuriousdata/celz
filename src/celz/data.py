class Spreadsheet(object):
    pass


class Row(object):
    def __init__(self, r):
        self.cells = r


class Cell(object):
    def __init__(self, v):
        self.value = v


class CSVFile(Spreadsheet):
    def __init__(self, f):
        self.rows = []
        import csv
        with open(f, 'r') as fp:
            reader = csv.reader(fp)
            for line in reader:
                self.rows.append(Row([Cell(x) for x in line]))


class Workbook(object):
    def __init__(self, f):
        self.data = None
        self.numsheets = 1
        if f.endswith('.csv'):
            self.spreadsheet = CSVFile(f)
        else:
            raise Exception("Filetype not implemented")
