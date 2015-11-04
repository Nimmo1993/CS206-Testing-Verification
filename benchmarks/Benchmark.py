from testcases.Random import Random
from testcases.Branch import Branch
from testcases.Additional import Additional
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
    baseline: what the coverages look like from a no input test

    """

    """
    This will give us the branch and statement coverage of runs
    we will need to formulate our run as follows:
        gcc -fprofile-arcs -ftest-coverage -fPIC input.c -o out
        we then run the program with test data.  This creates 2 files: [exec].gcda and [exec].gcno
        from there we can run gcov and see exactly what happens
        gcov -a -b -c -o gcov_out --object-file executable './executable arg1 arg2 argN'"
    """
    __gcc_out = "out"
    __gcov_out = "gcov_out"
    __gcc = "gcc -fprofile-arcs -ftest-coverage -fPIC -o {0}".format(__gcc_out)
    __gcov_obj_file = "--object-file executable"
    __gcov = "gcov -a -b -c -o {0} {1}".format(__gcov_out, __gcov_obj_file)

    def __init__(self, path, line):
        b = line.split('~')
        self.name = b[0]
        self.compile = b[1]
        self.example = b[2]
        self.dir = b[3]
        self.test_cases = b[4]
        self.path = path + self.name + "/"
        self.mutations = []
        for subdirs, dirs, files in os.walk(self.path):
            to_check = subdirs.split('/')[-1]
            if len(to_check) > 0:
                if to_check[0] == 'v':
                    self.mutations.append(subdirs)
        self.baseline = self.build_base_line()

    def build_base_line(self):
        command = "{0} {1}.c".format(Benchmark.__gcc, self.name)
        print command
        comman = "this part isn't working yet..."
        #command = "{0} ./{1}".format(Benchmark.__gcov, Benchmark.__gcc_out)
        print command
        return None

    def run_gcov(self):
        pass

    def get_mutations_as_string(self):
        string = ""
        for x in self.mutations:
            string = string + "\t" + x
        return string

    @staticmethod
    def run_command(command):
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print out
        print err

    def __str__(self):
        string = "Name: " + self.name + "\nCompilation: " + self.compile + "\nExample: "
        string = string + self.example + "\nDir: " + self.dir + "\nTest cases: " + self.test_cases
        string = string + "Mutations: " + self.get_mutations_as_string()
        return string + "\n=======================\n"
