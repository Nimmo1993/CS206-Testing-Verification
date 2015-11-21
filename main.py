from benchmarks.Benchmark import *
from benchmarks.Difference import *
from prioritizations.Total import Total
from prioritizations.Random import Random
from prioritizations.Additional import Additional
import sys
import csv

tag = "[main]\t"

run_random = {'run': True, 'display': False}
run_total = {'run': True, 'display': False}
run_additional = {'run': True, 'display': False}
__single = "single/"
__union = "union/"
run_limit = 5


def main():
    benchmarks = []

    if not os.path.isdir(sys.argv[3]):
        print "{0}{1} didn't exist, creating {1} now.".format(tag, sys.argv[3])
        os.mkdir(sys.argv[3])

    if not os.path.isdir(sys.argv[3] + "/" + __single):
        print "{0}{1}/{2} didn't exist, creating {1} now.".format(tag, sys.argv[3], __single)
        os.mkdir(sys.argv[3] + "/" + __single)

    if not os.path.isdir(sys.argv[3] + "/" + __union):
        print "{0}{1}/{2} didn't exist, creating {1} now.".format(tag, sys.argv[3], __union)
        os.mkdir(sys.argv[3] + "/" + __union)

    # read all input and create benchmarks for us
    with open(sys.argv[1]) as f:
        for line in f:
            benchmarks.append(Benchmark(sys.argv[2], line, run_limit))
            break
    # print or run all benchmarks from here
    for (x, benchmark) in enumerate(benchmarks):
        if run_random['run']:
            random = Random(benchmark.results)
            #random.build_single()
            random.build_union()
        if run_total['run']:
            total = Total(benchmark.results)
            #total.build_single()
            total.build_union()
        if run_additional['run']:
            additional = Additional(benchmark.results)
            additional.build_single()
            print "++++++++++++++++++"
            additional.build_union()

        if run_random['run'] and run_random['display']:
            print tag, "=================="
            print "{0}Random: branches: {1}\t statements: {2}".format(tag, len(random.results['branches']),
                                                                   len(random.results['statements']))
            print tag, random.results
            for b in random.results['branches']:
                print tag, b
                pass
            print tag, "------"
            for s in random.results['statements']:
                print tag, s
                pass
        if run_total['run'] and run_total['display']:
            print tag, "=================="
            print "{0}Total: branches: {1}\t statements: {2}".format(tag, len(total.results['branches']),
                                                                     len(total.results['statements']))
            #print total.results['branches']
            for b in total.results['branches']:
                print tag, b
                pass
            print tag, "------"
            for s in total.results['statements']:
                print tag, s
                pass
        if run_additional['run'] and run_additional['display']:
            print tag, "=================="
            print "{0}Additional: branches: {1}\t statements: {2}".format(tag, len(additional.results['branches']),
                                                                          len(additional.results['statements']))
            for b in additional.results['branches']:
                print tag, b
                pass
            print tag, "------"
            for s in additional.results['statements']:
                print tag, s
                pass

        # run the mutations
        benchmark.run_mutation_tests(random, total, additional)

        # build the diff results for both the single and the union
        #diff_single = Difference(mutant=benchmark.mutant_results, rand=random.results,
        #                  total=total.results, add=additional.results)
        #diff_union = Difference(mutant=benchmark.mutant_results, rand=random.union_results,
        #                        total=total.union_results, add=additional.union_results)

        #diff_single.write_results(sys.argv[3] + __single + benchmark.name)
        #diff_single.write_raw_results(sys.argv[3] + __single + benchmark.name)

        #diff_uniont.write_results(sys.argv[3] + __union + benchmark.name)
        #diff_union.write_raw_results(sys.argv[3] + __union + benchmark.name)
        break
        ###
        # print benchmark
        ###
    if run_limit != -1:
        for x in range(0,10):
            print tag, "Ensure you remove the \"limit\" variable before turning this in!!!!!"

if __name__ == "__main__":
    print tag, "Run Random? {0}".format(run_random)
    print tag, "Run Total? {0}".format(run_total)
    print tag, "Run Additional? {0}".format(run_additional)
    main()
