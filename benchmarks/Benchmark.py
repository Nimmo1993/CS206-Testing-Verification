from structures.GcovResults import GcovResults
import os
import subprocess


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
        then run: gcov -abci input.c
        and repeat
        from there we can run gcov and see exactly what happens
        gcov -a -b -c -o gcov_out --object-file executable './executable arg1 arg2 argN'"
    """
    __gcc_out = "out"
    __gcov_out = "gcov_out"
    __gcc = "gcc -fprofile-arcs -ftest-coverage -fPIC -o {0}".format(__gcc_out)
    __gcov_obj_file = "--object-file executable"
    __gcov = "gcov -abc"
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
        with open(self.path + Benchmark.__universe) as f:
            for line in f:
                # run the test set given our newly compiled file
                command = "{0}./{1} {2}".format(self.path, Benchmark.__gcc_out, line)
                Benchmark.run_command(command)

                # Create the .gcov file from the gcno and gcda data
                command = "{0} {1}{2}.c".format(Benchmark.__gcov, self.path, self.name)
                Benchmark.run_command(command)

                # Pass the path to the newly created gcov file in order to parse what we need
                statements = GcovResults.parse_statements("{0}{1}.c.gcov".format(self.path, self.name))
                branches = GcovResults.parse_branches("{0}{1}.c.gcov".format(self.path, self.name))
                self.results.append(GcovResults(statements, branches))

                # Todo: run this command when we are done parsing stuff!
                command = "rm {0}.gcno {1}.gcda".format(self.name, self.name)
                #Benchmark.run_command(command)
                break
                #pass

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
        print command
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out, err

    def __str__(self):
        string = "Name: " + self.name + "\nCompilation: " + self.compile + "\nExample: "
        string = string + self.example + "\nDir: " + self.dir + "\nTest cases: " + self.test_cases
        string = string + "Mutations: " + self.get_mutations_as_string()
        return string + "\n=======================\n"
