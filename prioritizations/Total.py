from .Prioritization import Prioritization
from benchmarks.Benchmark import Benchmark
import subprocess

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
time O(m n * m log m). Typically, n is greater than
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

    __universe = "universe.txt"
    __gcc_out = "out"
    __gcov = "gcov -abcn"

    """
    For every test case add the test cases which add to the
    aggregate coverage based on the statement or branches
    provided, if test A is a subset of test B do not add
    else add the test case
    """
    def __init__(self, tests):
        Prioritization.__init__(self, tests)

        # get the important part of the
        # input so we can re-run gcov
        self.tag = "[Total]\t"

        pass

    def build_single(self):
        self.statement_coverage_tests = sorted(self.statement_coverage_tests,
                                               key=lambda x: x['covered_count'], reverse=True)
        self.branch_coverage_tests = sorted(self.branch_coverage_tests, key=lambda x: x['covered_count'], reverse=True)

        self.build_branch_coverage_set()
        self.build_statement_coverage_set()

    def build_statement_coverage_set(self):
        for value in self.statement_coverage_tests:
            if self.mutate_statement_test(value):
                self.results['statements'].append(value)

    def build_branch_coverage_set(self):
        for x in self.branch_coverage_tests:
            if self.mutate_branch_test(x):
                self.results['branches'].append(x)

    def build_union(self):
        self.union_tests = sorted(self.union_tests, key=lambda x: x['covered_count'], reverse=True)

        for value in self.union_tests:
            if value['type'] == 'statement':
                if self.mutate_statement_test(value):
                    self.union_results['statements'].append(value)
            elif value['type'] == 'branch':
                if self.mutate_branch_test(value):
                    self.union_results['branches'].append(value)
