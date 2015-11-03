from testcases.TestCase import TestCase


class Additional(TestCase):

    """
    Iteratively selects a test case which yields the greatest branch coverage,
    then adjusts the coverage information on subsequent test cases, do this until
    all branches are covered
    """

    def __init__(self):
        super(TestCase, self).__init__()
