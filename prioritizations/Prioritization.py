import json


class Prioritization(object):
    """
    A class which handles the test case generation of our required classes
    """

    def __init__(self, tests):
        self.tests = tests
        self.statement_coverage_tests = []
        self.branch_coverage_tests = []

        self.tag = "[Prioritization]\t"

        self.branch_test_cases = {'covered': {}, 'not': {}}
        self.statement_test_cases = {'covered': set(), 'not': set()}

        # build the simple test cases we need to discern coverage
        for x in self.tests[1]['branches']['coverage']:
            self.branch_test_cases['not'][int(x)] = set()
            y = 0
            for index in self.tests[1]['branches']['coverage'].get(x):
                self.branch_test_cases['not'][int(x)].add(y)
                self.branch_test_cases['covered'][int(x)] = set()
                y += 1
                pass

        # build the simple test cases we need to discern coverage
        for x in self.tests[1]['statements']['coverage']:
            self.statement_test_cases['not'].add(int(x))

        # split the test up into their respective containers
        for key in self.tests:
            self.statement_coverage_tests.append(self.tests[key].get('statements'))
            self.branch_coverage_tests.append(self.tests[key].get('branches'))

        self.results = {'branches': [], 'statements': []}
        pass

    def mutate_statement_test(self, statements):
        mutated = False
        not_covered = self.statement_test_cases['not'] - statements['covered']
        covered = self.statement_test_cases['not'] - (self.statement_test_cases['not'] - statements['covered'])
        if len(covered) > 0:
            for x in covered:
                self.statement_test_cases['not'].remove(x)
                self.statement_test_cases['covered'].add(x)
            mutated = True
        return mutated

    def mutate_branch_test(self, branches):
        mutated = False

        for branch in branches['coverage']:
            if branch in self.branch_test_cases['not']:
                not_covered = self.branch_test_cases['not'][branch] - branches['covered'][branch]
                covered = self.branch_test_cases['not'][branch] - \
                          (self.branch_test_cases['not'][branch] - branches['covered'][branch])
                if len(covered) > 0:
                    for x in covered:
                        self.branch_test_cases['not'][branch].remove(x)
                        self.branch_test_cases['covered'][branch].add(x)
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
