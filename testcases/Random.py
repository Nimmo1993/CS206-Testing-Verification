from testcases.TestCase import TestCase
import random


class Random(TestCase):
    """
    Random test case prioritization
    """

    def __init__(self, test_objects):
        super(TestCase, self).__init__()
        self.tests = random.shuffle(test_objects)
