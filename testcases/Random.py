import random


class Random(object):
    """
    Random test case prioritization
    """

    def __init__(self, tests):
        self.tests = tests
        self.selected_cases = random.sample(self.tests, random.randint(10-15))
        pass
