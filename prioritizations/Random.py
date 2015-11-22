import random
from .Prioritization import Prioritization


class Random(Prioritization):
    """
    Random test case prioritization
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        self.tag = "[Random]\t"

    def build_single(self):
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
        for index in self.statement_coverage_tests:
            if self.mutate_statement_test(index):
                self.results['statements'].append(index)

    def build_branch_coverage_set(self):
        for index in self.branch_coverage_tests:
            if self.mutate_branch_test(index):
                self.results['branches'].append(index)

    def build_union(self):
        random.shuffle(self.union_tests)
        self.build_union_coverage_set()

    def build_union_coverage_set(self):
        for index in self.union_tests:
            if index['type'] == 'statement':
                if self.mutate_statement_test(index):
                    self.union_results['statements'].append(index)
            elif index['type'] == 'branch':
                if self.mutate_branch_test(index):
                    self.union_results['branches'].append(index)
