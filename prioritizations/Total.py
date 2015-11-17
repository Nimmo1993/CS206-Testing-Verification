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
    def __init__(self, tests, path, name):
        Prioritization.__init__(self, tests)

        # get the important part of the
        # input so we can re-run gcov
        self.name = name
        self.path = path
        self.tag = "[Total]\t"

        self.results = {'statements': [], 'branches': []}

        # self.statement_coverage_tests = sorted(self.statement_coverage_tests,
                                               # key=lambda x: x['covered_count'], reverse=True)
        # self.branch_coverage_tests = sorted(self.branch_coverage_tests, key=lambda x: x['covered_count'], reverse=True)

        # self.build_statement_coverage_set()
        # self.build_branch_coverage_set()

        self.build_coverage()
        pass

    def build_coverage(self):
        x = 0
        line_coverage = float(0)
        branch_coverage = float(0)
        with open(self.path + Total.__universe) as f:
            for line in f:
                # run the test set given our newly compiled file
                command = "{0}./{1} {2}".format(self.path, Total.__gcc_out, line)
                Benchmark.run_command(command, stdin=subprocess.PIPE, shell=True)

                # Create the .gcov file from the gcno and gcda data
                command = "{0} {1}{2}.c".format(Total.__gcov, self.path, self.name)
                from_command = Benchmark.run_command(command)
                res = from_command[0].strip().split()
                # parse the branch and the line coverage
                current_line_coverage = float(res[3].split(':')[1].split('%')[0])
                current_branch_coverage = float(res[7].split(':')[1].split('%')[0])

                # decide whether or not to add to the coverages
                if current_line_coverage > line_coverage:
                    line_coverage = current_line_coverage
                    self.results["statements"].append(x)
                if current_branch_coverage > branch_coverage:
                    branch_coverage = current_branch_coverage
                    self.results["branches"].append(x)
        print "{0} Statement Coverage: {1}".format(self.tag, line_coverage)
        print "{0} Branch Coverage: {1}".format(self.tag, branch_coverage)
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
