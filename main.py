from benchmarks.Benchmark import Benchmark
import sys


def main():
    benchmarks = []
    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[2], line))
    # print or run all benchmarks from here
    for (x, benchmark) in enumerate(benchmarks):
        pass
        ###
        # print benchmark
        ###

if __name__ == "__main__":
    main()
