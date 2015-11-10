

class StatementCoverage(object):

    def __init__(self):
        self.statements = []
        self.minimal_set = []

    def find_minimum_coverage(self):
        for statement in self.statements:
            print statement
        pass
