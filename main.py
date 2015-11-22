from benchmarks.Benchmark import *
from benchmarks.Difference import *
from prioritizations.Total import Total
from prioritizations.Random import Random
from prioritizations.Additional import Additional
import sys
import time

tag = "[main]\t"

run_random = {'run': True, 'display': False}
run_total = {'run': True, 'display': False}
run_additional = {'run': True, 'display': False}
__single = "single/"
__union = "union/"
run_limit = -1


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

    start = int(time.time())
    with open(sys.argv[1]) as f:
        for line in f:
            process = int(time.time())
            benchmark = Benchmark(sys.argv[2], line, run_limit)
            # Do random
            random = Random(benchmark.results)
            random.build_single()
            random.build_union()
            # Do total
            total = Total(benchmark.results)
            total.build_single()
            total.build_union()
            # Do Additional
            additional = Additional(benchmark.results)
            additional.build_single()
            additional.build_union()
            # run the mutations
            benchmark.run_mutation_tests_single(random, total, additional)
            benchmark.run_mutation_tests_union(random, total, additional)
            # build the diff results for both the single
            diff_single = Difference(mutant=benchmark.mutant_results_single, rand=random.results,
                                     total=total.results, add=additional.results)
            diff_single.find_differences_single()
            # write our results to disk!
            diff_single.write_results(sys.argv[3] + __single + benchmark.name)
            diff_single.write_raw_results(sys.argv[3] + __single + benchmark.name)
            # build the diff results for union
            diff_union = Difference(mutant=benchmark.mutant_results_union, rand=random.union_results,
                                    total=total.union_results, add=additional.union_results)
            diff_union.find_differences_union()
            # write our results to disk
            diff_union.write_results(sys.argv[3] + __union + benchmark.name)
            diff_union.write_raw_results(sys.argv[3] + __union + benchmark.name)
            print tag, "Finished processing: {0} in {1} seconds".format(benchmark.name, int(time.time())-process)
            print tag, "======================="
    print "Finished execution in: {0} seconds".format(int(time.time()) - start)

    if run_limit != -1:
        for x in range(0,10):
            print tag, "Ensure you remove the \"limit\" variable before turning this in!!!!!"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print tag, "Usage: python main {/path/to/curated/input.txt} {/path/to/the/benchmark/} {/path/to/the/results/}"
    else:
        main()
