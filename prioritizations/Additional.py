from .Prioritization import Prioritization


"""
T5: Additional branch coverage prioritization. Total
branch coverage prioritization schedules test cases in the order
of total coverage achieved. However, having executed a
test case and covered certain branches, more may be gained
in subsequent test cases by covering branches that have not
yet been covered. Additional branch coverage prioritization
iteratively selects a test case that yields the greatest branch
coverage, then adjusts the coverage information on subsequent
test cases to indicate their coverage of branches not
yet covered, and then repeats this process, until all branches
covered by at least one test case have been covered.
Having scheduled test cases in this fashion, we may be
left with additional test cases that cannot add additional
branch coverage. We could order these next using any prioritization
technique; in this work we order the remaining
test cases using total branch coverage prioritization.
Because additional branch coverage prioritization requires
recalculation of coverage information for each unprioritized
test case following selection of each test case, its
cost is O(n^2) for programs containing n branches

T4: Additional statement coverage prioritization. Additional
statement coverage prioritization is like total coverage
prioritization, but it relies on feedback about coverage
attained so far in testing to focus on statements not yet
covered. To do this, the technique greedily selects a test case
that yields the greatest statement coverage, then adjusts the
coverage data about subsequent test cases to indicate their
coverage of statements not yet covered, and then iterates
until all statements covered by at least one test case have
been covered. When all statements have been covered, the
remaining test cases are covered (recursively) by resetting
all statements to \"not covered\" and reapplying additional
statement coverage on the remaining test cases.
For a test suite and program containing m test cases and
n statements, respectively, the cost of additional statement
coverage prioritization is O(m^2 n), a factor of m more than
total statement coverage prioritization

The additional statement (addtl-st) prioritization technique
selects, in turn, the next test case that covers the maximum
number of statements not yet covered in the previous
round. When no remaining test case can improve the statement
coverage, the technique will reset all the statements to
\"not covered\" and reapply addtl-st on the remaining test
cases. When more than one test case covers the same number
of statements not yet covered, it just selects one of them
randomly. The additional function (addtl-fn) and additional
branch (addtl-br) test case prioritization technique are the
same as addtl-st, except that it uses function and branch
coverage information instead of statement coverage information[11][12]
[13].

Sort the cases by coverage, pull one, resort based on additional coverage left
take the not covered top one, intersect with all other sets, then resort remainder, pull form top, repeat

add test, then sort the list based on what you haven't seen, add again, then resort the list

So for additional you sort by total coverage first, then for every other test you sort by relative coverage from the last added coverage?
Coverage being literal true/false values for each statement/branch.
"""


class Additional(Prioritization):

    """
    Iteratively selects a test case which yields the greatest branch coverage,
    then adjusts the coverage information on subsequent test cases, do this until
    all branches are covered
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)

        for test in self.tests:
            self.statement_coverage_tests.append(self.tests[test].get('statements'))
            self.branch_coverage_tests.append(self.tests[test].get('branches'))

        # sort the branch and statement by their coverage count
        self.statement_coverage_tests = sorted(self.statement_coverage_tests,
                                               key=lambda x: x['covered_count'], reverse=True)
        self.branch_coverage_tests = sorted(self.branch_coverage_tests, key=lambda x: x['covered_count'], reverse=True)

        # We automatically take the first element as it maintains the highest coverage
        self.results['statements'].append(self.statement_coverage_tests[0])
        self.results['branches'].append(self.branch_coverage_tests[0])

        del self.statement_coverage_tests[0]
        del self.branch_coverage_tests[0]

        self.build_coverage()
        pass

    """
    Sort the lists, add the top element from the list to result, remove it from the test set
    compare all elements remaining to the last element on the results
    add whichever elements are different to a new list.
    repeat
    """
    def build_coverage(self):

        temp_statements = []
        temp_branches = []

        """
        Run for statements
        """
        for test in self.statement_coverage_tests:
            # see if we can pare anything from the list before we begin...
            if Prioritization.same_coverage(test['not'], self.results['statements'][-1]['not']) is False:
                temp_statements.append(test)

        print "pre Length of temp_statements: ", len(temp_statements)

        count = 0
        while len(temp_statements) > 0 and count < 4:
            print "Length of temp_statements: ", len(temp_statements)
            temp_statements = sorted(temp_statements, key=lambda covered: covered['covered_count'], reverse=True)
            for x in range(0, len(temp_statements)):
                print x
                if Prioritization.same_coverage(temp_statements[x]['not'],
                                                self.statement_coverage_tests[-1]['not']) is True:
                    del temp_statements[x]
                    print "len:",len(temp_statements)
            count += 1
            pass

        return
        """
        Run for branches
        """
        for test in self.branch_coverage_tests:
            # always compare against the last element added, because that covers the next least
            if not Prioritization.same_coverage(test['not'], self.results['branches'][-1]['not']):
                temp_branches.append(test)

        count = 0
        while len(temp_branches) > 0 and count < 4:
            # we must sort the list at each iteration according to the algorithm
            temp_branches = sorted(temp_branches, key=lambda x: x['covered_count'], reverse=True)
            for x in range(0, len(temp_branches)):
                # compare against the last element added to results for differences
                if Prioritization.same_coverage(temp_branches[x]['not'], self.branch_coverage_tests[-1]['not']) is True:
                    del temp_branches[x]
                else:
                    temp_branches.append(temp_branches[x])
            count += 1
            pass
