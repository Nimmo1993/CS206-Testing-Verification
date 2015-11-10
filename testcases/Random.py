import random


class Random(object):
    """
    Random test case prioritization
    """

    def __init__(self, tests):
        self.tests = tests
        self.coverage = 0
        self.coverage_set = self.tests[0]
        print self.coverage_set
        pass

    def build_coverage_set(self):
        pass
