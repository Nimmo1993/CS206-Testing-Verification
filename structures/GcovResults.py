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

    def add_statement(self, statement):
        self.statement_coverage.statements.append(statement)

    def add_branch(self, branch):
        self.branch_coverage.branches.append(branch)

    """
    Parses the statement coverage from a gcov input file
    """
    @staticmethod
    def parse_statements(file_loc):
        functions = []
        with open(file_loc) as f:
            for line in f:
                split = line.split(" ")
                if split[0] == "function":
                    functions.append({'name': split[1], 'returned': int(split[5].replace("%", "")),
                                      'blocks_executed': int(split[8].replace("%", "").strip())})
        return functions

    """
    Parses the branch coverage from a gcov input file
    """
    @staticmethod
    def parse_branches(file_loc):
        # this maps the methods->branch
        branches = []
        # this holds the branches in the particular function
        branch = []
        # allows us to keep track of which method we are actually visiting
        prev_function = ""
        curr_function = ""
        with open(file_loc) as f:
            for line in f:
                split = line.split(" ")
                # We must maintain the function name for each branch
                if split[0] == "function":
                    curr_function = split[1]
                    # add the branches to the blo
                    branches.append({'name':prev_function, 'branches': branch})
                    # update the previous function name!
                    prev_function = curr_function
                    # reset our branch variable
                    branch = []
                if split[0] == "branch":
                    branch.append({'id': int(split[2]), 'executed': int(split[4].replace("%", "").strip())})

        return branches
