from prioritizations.Additional import Additional
from prioritizations.Random import Random
from prioritizations.Total import Branch


class StatementCoverage(object):

    def __init__(self, tests):
        self.tests = tests
        self.random = Random()
        self.branch = Branch()
        self.additional = Additional()
        self.minimal_set = []

    def find_minimum_coverage(self):
        for statement in self.tests:
            print statement
        pass
