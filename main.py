from benchmarks.Benchmark import Benchmark
from prioritizations.Total import Total
from prioritizations.Random import Random
from prioritizations.Additional import Additional
import sys

tag = "[main]\t"

run_random = True
run_total = True
run_additional = True
run_limit = 5

def main():
    benchmarks = []
    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[2], line, run_limit))
            break
    # print or run all benchmarks from here
    for (x, benchmark) in enumerate(benchmarks):
        if run_random:
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
        if run_total:
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
        if run_additional:
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
        # benchmark.run_mutation_tests(random, total, additional)
        # benchmark.run_mutation_tests(None, None, None)
        break
        ###
        # print benchmark
        ###
    print tag, "Ensure you remove the \"limit\" variable before turning this in!!!!!"

if __name__ == "__main__":
    print tag, "Run Random? {0}".format(run_random)
    print tag, "Run Total? {0}".format(run_total)
    print tag, "Run Additional? {0}".format(run_additional)
    main()
