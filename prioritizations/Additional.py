from .Prioritization import Prioritization


class Additional(Prioritization):

    """
    Iteratively selects a test case which yields the greatest branch coverage,
    then adjusts the coverage information on subsequent test cases, do this until
    all branches are covered
    """

    def __init__(self, tests):
        Prioritization.__init__(self, tests)
        pass
