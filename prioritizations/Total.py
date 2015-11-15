from .Prioritization import Prioritization

"""
T4: Total branch coverage prioritization. By instrumenting
a program, we can determine, for any test case,
the number of decisions (branches) in that program that
were exercised by that test case. We can prioritize these
test cases according to the total number of branches they
cover simply by sorting them in order of total branch coverage
achieved. This prioritization can thus be accomplished
in time O(n log n) for programs containing n branches.

T3: Total statement coverage prioritization. Using program
instrumentation, we can measure the coverage of statements
in a program by its test cases. We can then prioritize
test cases in terms of the total number of statements they
cover by sorting them in order of coverage achieved. (If
multiple test cases cover the same number of statements, we
can order them pseudorandomly.)
Given a test suite of m test cases and a program of
n statements, total statement coverage prioritization requires
time O(m n þ m log m). Typically, n is greater than
m, making this equivalent to O(m n).

The total statement (total-st) test case prioritization technique
sorts test cases in descending order of the total number
of statements covered by each test case. In case of a tie, it
selects the involved test cases randomly. The total function
(total-fn) and total branch (total-br) test case prioritization
techniques are the same as total-st, except that it uses
function and branch coverage information instead of statement
coverage information [11].
"""
class Total(Prioritization, object):

    """
    For every test case add the test cases which add to the
    aggregate coverage based on the statement or branches
    provided, if test A is a subset of test B do not add
    else add the test case
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        self.results = {'statements': [], 'branches': []}

        self.statement_coverage_tests = sorted(self.statement_coverage_tests,
                                               key=lambda x: x['covered_count'], reverse=True)
        self.branch_coverage_tests = sorted(self.branch_coverage_tests, key=lambda x: x['covered_count'], reverse=True)

        self.build_statement_coverage_set()
        self.build_branch_coverage_set()
        pass

    """
    percent is monotonic.  Thus, we only add to our results when our coverage is
    greater than the percent.  If it's not we can safely ignore it!
    """
    def build_statement_coverage_set(self):
        percent = 0.0
        for index in self.statement_coverage_tests:
            index_total_coverage = float(index.get('covered_count') + float(index.get('not_count')))
            index_coverage = float(index.get('covered_count'))

            coverage = float(index_coverage / index_total_coverage)

            # force this to be monotonic!
            if coverage > percent and percent < float(100):
                percent = coverage
                self.results['statements'].append(index)
    """
    This is the same as build_statement_coverage_set,
    but separate for ease of use and flexibility
    """
    def build_branch_coverage_set(self):
        percent = 0.0
        for index in self.branch_coverage_tests:
            index_total_coverage = float(index.get('covered_count') + float(index.get('not_count')))
            index_coverage = float(index.get('covered_count'))

            coverage = float(index_coverage / index_total_coverage)

            # force this to be monotonic!
            if coverage > percent and percent < float(100):
                percent = coverage
                self.results['branches'].append(index)
