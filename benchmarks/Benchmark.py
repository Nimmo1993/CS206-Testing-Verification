from testcases.Random import Random
from testcases.Branch import Branch
from testcases.Additional import Additional


class Benchmark(object):

    """
    Defines the benchmark for each input that is required.  These benchmarks have 3 TestCases
    which will help us prioritize the test cases in order to achieve maximum coverage with
    the smallest amount of tests

    name: name of program to run
    path: root path + name
    compile: example compilation
    dir: dir for inputs (may contain multiple dirs)
    example: example of running the program
    test_cases: file which contains test cases for us
    mutations: list of mutations to test against
    
    """

    def __init__(self, path, line):
        b = line.split('~')
        self.name = b[0]
        self.compile = b[1]
        self.example = b[2]
        self.dir = b[3]
        self.test_cases = b[4]
        self.path = path + self.name
        self.mutations = None

        self.random = Random()
        self.branch = Branch()
        self.additional = Additional()

    def run_benchmark(self):
        print "running " + self.name

    def __str__(self):
        return "Name: " + self.name + "\nCompilation: " + self.compile + "\nExample: " \
              + self.example + "\nDir: " + self.dir + "\nTest cases: " + self.test_cases
