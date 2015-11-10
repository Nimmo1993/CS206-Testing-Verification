from Random import Random
from Branch import Branch
from Additional import Additional


class TestSuite(object):
    """
    A class which handles the test case generation of our required classes
    """

    def __init__(self, tests):
        self.tests = tests
        self.random = Random(self.tests)
        self.additional = Additional(self.tests)
        self.branch = Branch(self.tests)

        self.random.build_coverage_set()
