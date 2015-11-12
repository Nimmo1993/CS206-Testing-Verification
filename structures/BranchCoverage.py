from prioritizations.Additional import Additional
from prioritizations.Random import Random
from prioritizations.Branch import Branch


class BranchCoverage(object):

    def __init__(self, tests):
        self.tests = tests
        self.random = Random()
        self.branch = Branch()
        self.additional = Additional()
        self.minimum_set = []

    def find_minimum_coverage(self):
        pass
