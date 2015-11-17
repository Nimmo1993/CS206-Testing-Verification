from benchmarks.Benchmark import Benchmark
from prioritizations.Total import Total
from prioritizations.Random import Random
from prioritizations.Additional import Additional
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
        # random = Random(benchmark.results)
        # print random.results
        # total = Total(benchmark.results, benchmark.path, benchmark.name)
        # print total.results
        additional = Additional(benchmark.results)
        print additional.results

        # benchmark.run_mutation_tests(random, total, additional)
        #benchmark.run_mutation_tests(None, None, None)
        break
        ###
        # print benchmark
        ###

if __name__ == "__main__":
    main()
