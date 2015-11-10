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

    @staticmethod
    def parse_gcov(path):
        results = {}
        line_number = 0
        still_branch = False
        branches = []
        with open("/Users/jason/Desktop/cs206/benchmarks/tcas/tcas.c.gcov") as f:
            for line in f:
                split = line.split()
                print split
                # Junk or garbage input from gcov
                if split[0] == "-:" or split[0] == "$$$$$:" or split[0] == "#####:" or split[0] == "function":
                    continue

                # We care about branches and line numbers, hence this block!
                if split[0] != "branch":
                    if still_branch:
                        results[line_number] = branches
                        branches = []
                        still_branch = False
                    line_number = int(split[1].strip(":}"))
                else:
                    branches.append(True if int(split[3]) > 0 else False)
                    still_branch = True
        return results
