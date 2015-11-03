from testcases.TestCase import TestCase


class Branch(TestCase):

    """
    Prioritizes test cases by the total number of branches covered
    """

    def __init__(self):
        super(TestCase, self).__init__()
