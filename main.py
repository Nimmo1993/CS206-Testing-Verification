from benchmarks.Benchmark import Benchmark
from prioritizations.Total import Total
from prioritizations.Random import Random
from prioritizations.Additional import Additional
import sys

tag = "[main]\t"

def main():
    benchmarks = []
    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[2], line))
            break
    # print or run all benchmarks from here
    for (x, benchmark) in enumerate(benchmarks):
        #"""
        random = Random(benchmark.results)
        print tag, "=================="
        print "{0}Random: branches: {1}\t statements: {2}".format(tag, len(random.results['branches']),
                                                               len(random.results['statements']))
        print random.results
        for b in random.results['branches']:
            print tag, b
            pass
        print "------"
        for s in random.results['statements']:
            print tag, s
            pass
        #"""
        """
        total = Total(benchmark.results)
        print tag, "=================="
        print tag, "{0}Total: branches: {1}\t statements: {2}".format(tag, len(total.results['branches']),
                                                                 len(total.results['statements']))
        #print total.results['branches']
        for b in total.results['branches']:
            print tag, b
            pass
        print "------"
        for s in total.results['statements']:
            print tag, s
            pass
        """
        """
        additional = Additional(benchmark.results)
        print tag, "=================="
        print "{0}Additional: branches: {1}\t statements: {2}".format(tag, len(additional.results['branches']),
                                                                      len(additional.results['statements']))
        for b in additional.results['branches']:
            print b
            pass
        print "------"
        for s in additional.results['statements']:
            print s
            pass
        """
        # benchmark.run_mutation_tests(random, total, additional)
        # benchmark.run_mutation_tests(None, None, None)
        break
        ###
        # print benchmark
        ###

if __name__ == "__main__":
    main()
