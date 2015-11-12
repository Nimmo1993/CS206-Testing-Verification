from structures.GcovResults import GcovResults
import os
import subprocess
import json
from functools import partial
from operator import is_not


class Benchmark(object):

    """
    Defines the benchmark for each input that is required.  These benchmarks have 3 TestCases
    which will help us prioritize the test cases in order to achieve maximum coverage with
    the smallest amount of tests

    It is assumed that each object here has a complimenting ".c" of the name.  Such that
    tcas will have a tcas.c in the same root directory of tcas

    from there we will take each benchmark and run the gcov on it.  This will give us a baseline.

    name: name of program to run
    path: root path + name
    compile: example compilation
    dir: dir for inputs (may contain multiple dirs)
    example: example of running the program
    test_cases: file which contains test cases for us
    mutations: list of mutations to test against, a list of paths which contain
        all available mutations for the benchmark
    results: where to store the coverage results
    """

    """
    This will give us the branch and statement coverage of runs
    we will need to formulate our run as follows:
        gcc -fprofile-arcs -ftest-coverage -fPIC input.c -o out
        This creates 2 files: [exec].gcda and [exec].gcno
        we then execute: ./out [args]
        then run: gcov -abc input.c
        rm input.c.gcov
        and repeat
        from there we can run gcov and see exactly what happens
        gcov -a -b -c -o gcov_out --object-file executable './executable arg1 arg2 argN'"
    """
    __gcc_out = "out"
    __gcov_out = "gcov_out"
    __gcc = "gcc -fprofile-arcs -ftest-coverage -fPIC -o {0}".format(__gcc_out)
    __gcov_obj_file = "--object-file executable"
    __gcov = "gcov -bc"
    __universe = "universe.txt"

    def __init__(self, path, line):
        b = line.split('~')
        self.name = b[0]
        self.compile = b[1]
        self.example = b[2]
        self.dir = b[3]
        self.test_cases = b[4]
        self.path = path + self.name + "/"
        self.mutations = []

        # Compile the file with the necessary gcov flags
        Benchmark.run_command("{0} {1}.c".format(Benchmark.__gcc, self.name))

        # get all the mutations present in the directory
        for subdirs, dirs, files in os.walk(self.path):
            to_check = subdirs.split('/')[-1]
            if len(to_check) > 0:
                if to_check[0] == 'v':
                    self.mutations.append(subdirs)

        # this is where we will store the results for our tests
        self.results = []
        # run the tests on our non-mutated program
        self.run_tests()

    """
    Run the tests available to the program
    """
    def run_tests(self):
        x = 0
        with open(self.path + Benchmark.__universe) as f:
            for line in f:
                # run the test set given our newly compiled file
                command = "{0}./{1} {2}".format(self.path, Benchmark.__gcc_out, line)
                Benchmark.run_command(command)

                # Create the .gcov file from the gcno and gcda data
                command = "{0} {1}{2}.c".format(Benchmark.__gcov, self.path, self.name)
                Benchmark.run_command(command)

                # parse the gcov results
                self.parse_gcov("{0}{1}.c.gcov".format(self.path, self.name))

                command = "rm {0}{1}.gcno {2}{3}.gcda".format(self.path, self.name, self.path, self.name)
                Benchmark.run_command(command)
                x += 1
                if x > 99:
                    break
                else:
                    continue
        print "Benchmark: size of results: ", len(self.results)
        # with open("/Users/jason/Desktop/cs206/tcas.results", 'a') as f:
            # f.write(json.dumps(self.results))

    """
    Parse the gcov output for the branch information
    """
    def parse_gcov(self, path):
        line_number = 0
        still_branch = False
        branch = []
        statements = {}
        branches = {}
        with open(path) as f:
            for line in f:
                split = line.split()
                # Junk or garbage input from gcov
                if split[0] == "-:" or split[0] == "$$$$$:" or split[0] == "function" or "-block" in split[1]:
                    continue

                # If we don't have a branch, parse it as a regular line
                # and add the previous branches to the list
                if split[0] != "branch":
                    # we have a branch and we need to save it, then progress our line number
                    if still_branch:
                        branches[line_number] = branch
                        branch = []
                        still_branch = False
                    # Get the line number and add it to the statements
                    line_number = int(split[1].strip(":}"))
                    statements[line_number] = True if split[0].strip(":") != "#####" else False
                else:
                    branch.append(True if int(split[3]) > 0 else False)
                    still_branch = True
        self.results.append({'statements': statements, 'branches': branches})

    """
    Retrieve each mutation from the program folder
    This will return a path for all mutations needed
    testing
    """
    def get_mutations_as_string(self):
        string = ""
        for x in self.mutations:
            string = string + "\t" + x
        return string

    """
    wrapper to run a command and capture the output
    """
    @staticmethod
    def run_command(command):
        # print(command)
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out, err

    def __str__(self):
        string = "Name: " + self.name + "\nCompilation: " + self.compile + "\nExample: "
        string = string + self.example + "\nDir: " + self.dir + "\nTest cases: " + self.test_cases
        string = string + "Mutations: " + self.get_mutations_as_string()
        return string + "\n=======================\n"
