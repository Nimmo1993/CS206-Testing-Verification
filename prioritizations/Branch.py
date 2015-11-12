from .Prioritization import Prioritization


class Branch(Prioritization, object):

    """
    For every test case add the test cases which add to the
    aggregate coverage based on the statement or branches
    provided, if test A is a subset of test B do not add
    else add the test case
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)

        self.build_statement_coverage_set()
        self.build_branch_coverage_set()
        pass


    """
    Is this ugly? yes
    does this greatly simplify the detection of branch coverage? absolutely
    There are a few flaws that need to be ironed out from this particular logic.
    test cases can be added multiple times
    """
    def build_statement_coverage_set(self):
        length = len(self.tests)
        for x in range(0, len(self.tests)):
            y = x+1
            if y < length:
                statements_covered_x = set(self.tests[x].get('meta').get('statements').get('covered'))
                branches_covered_x = set(self.tests[x].get('meta').get('branches').get('covered'))
                statements_covered_y = set(self.tests[y].get('meta').get('statements').get('covered'))
                branches_covered_y = set(self.tests[y].get('meta').get('branches').get('covered'))

                branches_covered_set = list(branches_covered_x - branches_covered_y)
                statements_covered_set = list(statements_covered_x - statements_covered_y)
                # Statements covered
                if len(statements_covered_set) > 0:
                    for i in statements_covered_set:
                        if i in statements_covered_x:
                            self.results.append(self.tests[x])
                        elif i in statements_covered_y:
                            self.results.append(self.tests[y])
                # Branches covered
                if len(branches_covered_set) > 0:
                    for i in branches_covered_set:
                        if i in branches_covered_x:
                            self.results.append(self.tests[x])
                        elif i in statements_covered_y:
                            self.results.append(self.tests[y])
                    pass
        pass

    def build_branch_coverage_set(self):
        for x in range(0, len(self.tests)):
            print x
        pass
