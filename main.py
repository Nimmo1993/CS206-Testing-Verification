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

        """
        for test in benchmark.results:
            branch = benchmark.results[test]['branches']
            state = benchmark.results[test]['statements']
            bc = float(branch['covered_count']) / (float(branch['covered_count']) + float(branch['not_count']))
            sc = float(state['covered_count']) / (float(state['covered_count']) + float(state['not_count']))

            print "Branch: id: {0}\nCovered: {1}\t Not: {2}\n Calculated Coverage: {3}".format(branch['id'], branch['covered_count'], branch['not_count'], bc)
            print "Statement: id: {0}\nCovered: {1}\t Not: {2}\n Calculated Coverage: {3}".format(state['id'], state['covered_count'], state['not_count'], sc)
            print "========================="
        """

        """
        random = Random(benchmark.results)
        print "{0}Random: branches: {1}\t statements: {2}".format(tag, len(random.results['branches']),
                                                               len(random.results['statements']))

        total = Total(benchmark.results, benchmark.path, benchmark.name)
        print "{0}Total: branches: {0}\t statements: {1}".format(tag, len(total.results['branches']),
                                                              len(total.results['statements']))
        """
        additional = Additional(benchmark.results)
        print "{0}Additional: branches: {1}\t statements: {2}".format(tag, len(additional.results['branches']),
                                                                      len(additional.results['statements']))
        # benchmark.run_mutation_tests(random, total, additional)
        # benchmark.run_mutation_tests(None, None, None)
        break
        ###
        # print benchmark
        ###

if __name__ == "__main__":
    main()
