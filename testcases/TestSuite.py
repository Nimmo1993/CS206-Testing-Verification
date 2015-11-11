import Random
import Branch
import Additional


class TestSuite(object):
    """
    A class which handles the test case generation of our required classes
    """

    def __init__(self, tests):
        self.tests = tests
        self.random = Random.Random(self.tests)
        self.additional = Additional.Additional(self.tests)
        self.branch = Branch.Branch(self.tests)

    """
    Todo: these are too naive, change this to be a total count, not a first find exit
    """
    @staticmethod
    def is_branch_coverage_complete(list):
        for x in list:
            for index in list.get(x):
                if index is False:
                    return False
        return True

    @staticmethod
    def is_statement_coverage_complete(list):
        for x in list:
            for index in list[x]:
                if index is False:
                    return False
        return True
