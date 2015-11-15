import random
from .Prioritization import Prioritization


class Random(Prioritization):
    """
    Random test case prioritization
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        self.coverage = 0
        self.branch_test_cases = {}
        self.statement_test_cases = {}

        for x in self.tests[0]['branches']['coverage']:
            self.branch_test_cases[int(x)] = []
            for index in self.tests[0]['branches']['coverage'].get(x):
                self.branch_test_cases[int(x)].append(False)

        for x in self.tests[0]['statements']['coverage']:
            self.statement_test_cases[int(x)] = []
            self.statement_test_cases[int(x)].append(False)

        # randomly shuffle the test cases
        random.shuffle(self.branch_coverage_tests)
        random.shuffle(self.statement_coverage_tests)

        self.build_statement_coverage_set()
        self.build_branch_coverage_set()

    """
    1) check each element in the input against the coverage set
    2) if we change one element in the coverage set we must take the test
    3) continue to do this until you have maximum coverage
    """
    def build_statement_coverage_set(self):
        found_solution = False
        x = 0
        for index in self.statement_coverage_tests:
            save_test = False
            for key in index['coverage']:
                #print "Random line no: {0} test case: {1}\t current coverage: {2}".format(key, index['statements'].get(key), self.statement_test_cases.get(key)[0])
                if index['coverage'].get(key) != self.statement_test_cases.get(key)[0] \
                        and index['coverage'].get(key) is True:
                    self.statement_test_cases.get(key)[0] = index['coverage'].get(key)
                    save_test = True
            # See if we need to save the test
            if save_test:
                self.results['statements'].append(index)
            # See if we are done with test coverage
            if Prioritization.is_statement_coverage_complete(self.statement_test_cases) is True:
                break
            x += 1
        if not found_solution:
            print "[Random]\tcould not achieve 100% statement coverage"

    def build_branch_coverage_set(self):
        found_solution = False
        for index in self.branch_coverage_tests:
            save_test = False
            for key in index['coverage']:
                x = 0
                for boolean in index['coverage'].get(key):
                    if boolean != self.branch_test_cases.get(key)[x] and boolean is True:
                        self.branch_test_cases.get(key)[x] = boolean
                        save_test = True
                    x += 1
            if save_test:
                self.results['branches'].append(index)
            if Prioritization.is_branch_coverage_complete(self.branch_test_cases) is True:
                break
        if not found_solution:
            print "[Random]\tcould not achieve 100% branch coverage"
