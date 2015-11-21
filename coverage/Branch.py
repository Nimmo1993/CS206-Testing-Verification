from .Coverage import Coverage


class Branch(Coverage):

    def __init__(self, coverage, line, branches, covered=False):
        Coverage.__init__(coverage, line, covered)
        self.branches = branches
