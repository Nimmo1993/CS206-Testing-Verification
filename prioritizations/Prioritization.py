

class Prioritization(object):
    """
    A class which handles the test case generation of our required classes
    """

    def __init__(self, tests):
        self.tests = tests
        self.statement_coverage_tests = []
        self.branch_coverage_tests = []

        self.branch_test_cases = {}
        self.statement_test_cases = {}

        for x in self.tests[0]['branches']['coverage']:
            self.branch_test_cases[int(x)] = []
            for index in self.tests[0]['branches']['coverage'].get(x):
                self.branch_test_cases[int(x)].append(False)

        for x in self.tests[0]['statements']['coverage']:
            self.statement_test_cases[int(x)] = False

        for key in self.tests:
            self.statement_coverage_tests.append(self.tests[key].get('statements'))
            self.branch_coverage_tests.append(self.tests[key].get('branches'))

        self.results = {'branches': [], 'statements': []}
        pass

    def mutate_statement_test(self, statements):
        mutated = False
        for x in self.statement_test_cases:
            if self.statement_test_cases[x] == False and statements[x] == True:
                self.statement_test_cases[x] = True
                mutated = True
        return mutated

    def mutate_branch_test(self, branches):
        mutated = False
        for x in self.branch_test_cases:
            for y, value in enumerate(self.branch_test_cases[x]):
                if self.branch_test_cases[x][y] == False and branches[x][y] == True:
                    self.branch_test_cases[x][y] = True
                    mutated = True
        return mutated

    """
    Checks for similarity of test cases
    """
    @staticmethod
    def same_coverage(s1, s2):
        if len(s1) is not len(s2):
            return False
        for x in range(0, len(s1)):
            if s1[x] != s2[x]:
                return False
        return True

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
