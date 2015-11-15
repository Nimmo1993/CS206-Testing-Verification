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
        self.results = {'statements': [], 'branches': []}

        self.build_branch_coverage_set()
        self.build_statement_coverage_set()
        pass

    """
    percent is monotonic.  Thus, we only add to our results when our coverage is
    greater than the percent.  If it's not we can safely ignore it!
    """
    def build_statement_coverage_set(self):
        percent = 0.0
        for index in self.tests:
            index_total_coverage = float(len(index.get('meta').get('statements').get('covered')) + \
                        len(index.get('meta').get('statements').get('not')))
            index_coverage = float(len(index.get('meta').get('statements').get('covered')))

            coverage = float(index_coverage / index_total_coverage)

            # force this to be monotonic!
            if coverage > percent:
                percent = coverage
                self.results.get('statements').append({'id': index.get('meta').get('id'),
                                                       'statements': index.get('statements')})
    """
    This is the same as build_statement_coverage_set,
    but separate for ease of use and flexibility
    """
    def build_branch_coverage_set(self):
        percent = 0.0
        for index in self.tests:
            index_total_coverage = float(len(index.get('meta').get('branches').get('covered')) + \
                        len(index.get('meta').get('branches').get('not')))
            index_coverage = float(len(index.get('meta').get('branches').get('covered')))

            coverage = float(index_coverage / index_total_coverage)

            # force this to be monotonic!
            if coverage > percent:
                percent = coverage
                self.results.get('branches').append({'id': index.get('meta').get('id'),
                                                    'branches': index.get('branches')})
