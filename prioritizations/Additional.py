from .Prioritization import Prioritization


"""
1) Sort the test cases by coverage_count
2) add the top element to the results
3) remove the element from the list
4) resort the test cases relative to the coverage of the first one
    -we want to resort based on previous coverage. So the
        test cases that have the most coverage of what is remaining
5) repeat 2-4 until as close to 100% as possible, or a test case
        provides no additional coverage
"""


class Additional(Prioritization):

    """
    Iteratively selects a test case which yields the greatest branch coverage,
    then adjusts the coverage information on subsequent test cases, do this until
    all branches are covered
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        self.tag = "[Additional]\t"

        # sort the branch and statement by their coverage count
        self.statement_coverage_tests = sorted(self.statement_coverage_tests,
                   key=lambda x: x['covered_count'], reverse=True)
        self.branch_coverage_tests = sorted(self.branch_coverage_tests, key=lambda x: x['covered_count'], reverse=True)

        # We automatically take the first element as it maintains the highest coverage
        self.results['statements'].append(self.statement_coverage_tests[0])
        self.results['branches'].append(self.branch_coverage_tests[0])

        self.mutate_statement_test(self.results['statements'][0])
        self.mutate_branch_test(self.results['branches'][0])

        del self.statement_coverage_tests[0]
        del self.branch_coverage_tests[0]

        if len(self.branch_coverage_tests) > 0:
            self.build_branch_coverage_set()
        if len(self.statement_coverage_tests) > 0:
            self.build_statement_coverage_set()

        pass

    def build_branch_coverage_set(self):
        working = True
        while working:
            # sort
            self.branch_coverage_tests = sorted(self.branch_coverage_tests, cmp=self.compare_branches)

            if self.mutate_branch_test(self.branch_coverage_tests[0]):
                self.results['branches'].append(self.branch_coverage_tests[0])
                del self.branch_coverage_tests[0]
            else:
                working = False

            if len(self.branch_coverage_tests) == 0:
                working = False

        pass

    def build_statement_coverage_set(self):
        working = True
        while working:
            # sort
            self.statement_coverage_tests = sorted(self.statement_coverage_tests, cmp=self.compare_statements)

            if self.mutate_statement_test(self.statement_coverage_tests[0]):
                self.results['statements'].append(self.statement_coverage_tests[0])
                del self.statement_coverage_tests[0]
            else:
                working = False

            if len(self.statement_coverage_tests) == 0:
                break

        pass

    def compare_statements(self, a, b):
        if len(a['covered'].intersection(self.statement_test_cases['not'])) < \
                len(b['covered'].intersection(self.statement_test_cases['not'])):
            return 1
        elif len(a['covered'].intersection(self.statement_test_cases['not'])) > \
                len(b['covered'].intersection(self.statement_test_cases['not'])):
            return -1
        else:
            return 0

    def compare_branches(self, a, b):
        a_changes = 0
        b_changes = 0

        for res in a['covered']:
            a_changes += len(a['covered'][res].intersection(self.branch_test_cases['not'][res]))
            b_changes += len(b['covered'][res].intersection(self.branch_test_cases['not'][res]))

        if a_changes < b_changes:
            return 1
        elif a_changes > b_changes:
            return -1
        else:
            return 0
