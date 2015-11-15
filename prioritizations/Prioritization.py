

class Prioritization(object):
    """
    A class which handles the test case generation of our required classes
    """

    def __init__(self, tests):
        self.tests = tests
        self.statement_coverage_tests = []
        self.branch_coverage_tests = []

        for key in self.tests:
            self.statement_coverage_tests.append(self.tests[key].get('statements'))
            self.branch_coverage_tests.append(self.tests[key].get('branches'))

        self.results = {'branches': [], 'statements': []}
        pass

    """
    total_trues acts as the counter for total coverage.
    """
    @staticmethod
    def is_branch_coverage_complete(value):
        total_taken = 0
        total_branches = 0
        for x in value:
            for index in value.get(x):
                total_branches += 1
                if index is True:
                    total_taken += 1
        return total_taken == total_branches

    """
    trues acts as a counter for the number of executed statement.
    We can only stop when we have as many trues as there are
    statements covered in the test case
    """
    @staticmethod
    def is_statement_coverage_complete(value):
        total_trues = 0
        for x in value:
            for index in value[x]:
                if index is True:
                    total_trues += 1
        return total_trues == len(value)
