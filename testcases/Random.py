import random
import TestSuite

class Random(object):
    """
    Random test case prioritization
    """

    def __init__(self, tests):
        self.tests = tests
        self.coverage = 0
        self.branch_coverage_set = {}
        self.statement_coverage_set = {}
        self.results = []

        for x in self.tests[0]['branches']:
            self.branch_coverage_set[int(x)] = []
            for index in self.tests[0]['branches'].get(x):
                self.branch_coverage_set[int(x)].append(False)

        for x in self.tests[0]['statements']:
            self.statement_coverage_set[int(x)] = []
            self.statement_coverage_set[int(x)].append(False)

        # randomly shuffle the test cases
        random.shuffle(self.tests)
        self.build_branch_coverage_set()
        self.build_statement_coverage_set()

    """
    1) check each element in the input against the coverage set
    2) if we change one element in the coverage set we must take the test
    3) continue to do this until you have maximum coverage
    """
    def build_statement_coverage_set(self):
        #print self.statement_coverage_set
        x = 0
        for index in self.tests:
            save_test = False
            for key in index['statements']:
                if index['statements'].get(key) != self.statement_coverage_set.get(key)[0] \
                        and index['statements'].get(key) is True:
                    print "{0}:{1}\t{2}:{3}".format(key, index['statements'].get(key), key, self.statement_coverage_set.get(key)[0])
                    self.statement_coverage_set.get(key)[0] = index['statements'].get(key)
                    save_test = True
            # See if we need to save the test
            if save_test:
                print "adding: ", index
                self.results.append(index)
                save_test = False
            # See if we are done with test coverage
            if TestSuite.TestSuite.is_statement_coverage_complete(self.statement_coverage_set) is True:
                break
        print "-----------"
        print self.statement_coverage_set

    pass

    def build_branch_coverage_set(self):
        while TestSuite.TestSuite.is_branch_coverage_complete(self.branch_coverage_set):
            break
    pass
