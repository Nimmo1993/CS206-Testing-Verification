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
cost is O(n2) for programs containing n branches

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
all statements to “not covered” and reapplying additional
statement coverage on the remaining test cases.
For a test suite and program containing m test cases and
n statements, respectively, the cost of additional statement
coverage prioritization is Oðm2 nÞ, a factor of m more than
total statement coverage prioritization

The additional statement (addtl-st) prioritization technique
selects, in turn, the next test case that covers the maximum
number of statements not yet covered in the previous
round. When no remaining test case can improve the statement
coverage, the technique will reset all the statements to
“not covered” and reapply addtl-st on the remaining test
cases. When more than one test case covers the same number
of statements not yet covered, it just selects one of them
randomly. The additional function (addtl-fn) and additional
branch (addtl-br) test case prioritization technique are the
same as addtl-st, except that it uses function and branch
coverage information instead of statement coverage information[11][12]
[13].

"""

class Additional(Prioritization):

    """
    Iteratively selects a test case which yields the greatest branch coverage,
    then adjusts the coverage information on subsequent test cases, do this until
    all branches are covered
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        pass
