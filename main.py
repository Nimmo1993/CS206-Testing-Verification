from benchmarks.Benchmark import Benchmark
from testcases.TestSuite import TestSuite
import sys


def main():
    benchmarks = []
    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[2], line))
            break
    # print or run all benchmarks from here
    for (x, benchmark) in enumerate(benchmarks):
        test_suite = TestSuite(benchmark.results)
        break
        ###
        # print benchmark
        ###

if __name__ == "__main__":
    main()
