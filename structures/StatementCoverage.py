from testcases.Additional import Additional
from testcases.Random import Random
from testcases.Branch import Branch


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
