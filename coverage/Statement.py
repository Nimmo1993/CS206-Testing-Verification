from Coverage import Coverage


class Statement(Coverage):

    def __init__(self, coverage, line, covered=False):
        Coverage.__init__(coverage, line, covered)
