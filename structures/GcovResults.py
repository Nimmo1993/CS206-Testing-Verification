from StatementCoverage import StatementCoverage
from BranchCoverage import BranchCoverage


class GcovResults(object):

    """
    Parent class responsible for calculating the available coverages based on the input
    This will take the statement and branch coverage from gcov and compute the coverages

    """

    def __init__(self):
        self.statement_coverage = StatementCoverage()
        self.branch_coverage = BranchCoverage()
