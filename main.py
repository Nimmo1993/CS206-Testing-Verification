from benchmarks.Benchmark import Benchmark
import sys


def main():
    print str(sys.argv)
    benchmarks = []
    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[1], line))
    for (x, benchmark) in enumerate(benchmarks):
        print benchmark

if __name__ == "__main__":
    main()
