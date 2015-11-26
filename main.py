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
__test_suites = "test_suites/"
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

    if not os.path.isdir(sys.argv[3] + "/" + __test_suites):
        print "{0}{1}/{2} didn't exist, creating {1} now.".format(tag, sys.argv[3], __test_suites)
        os.mkdir(sys.argv[3] + "/" + __test_suites)

    start = int(time.time())
    with open(sys.argv[1]) as f:
        for line in f:
            process = int(time.time())
            benchmark = Benchmark(sys.argv[2], line, run_limit)
            benchmark.prepare_and_run()
            if benchmark.run:
                # Do random
                srandom = Random(benchmark.results)
                srandom.build_single()
                urandom = Random(benchmark.results)
                urandom.build_union()
                # Do total
                stotal = Total(benchmark.results)
                stotal.build_single()
                utotal = Total(benchmark.results)
                utotal.build_union()
                # Do Additional
                sadditional = Additional(benchmark.results)
                sadditional.build_single()
                uadditional = Additional(benchmark.results)
                uadditional.build_union()
                # run the mutations
                benchmark.run_mutation_tests_single(srandom, stotal, sadditional)
                benchmark.run_mutation_tests_union(urandom, utotal, uadditional)

                # write our test_suite to disk
                benchmark.write_test_suite_to_disk(sys.argv[3] + __test_suites, "single", srandom.results,
                                                   stotal.results, sadditional.results)
                benchmark.write_test_suite_to_disk(sys.argv[3] + __test_suites, "union", urandom.union_results,
                                                   utotal.union_results, uadditional.union_results)

                # build the diff results for the single
                diff_single = Difference(mutant=benchmark.mutant_results_single, rand=srandom.results,
                                         total=stotal.results, add=sadditional.results)
                diff_single.find_differences_single()
                # write our results to disk!
                diff_single.write_results(sys.argv[3] + __single + benchmark.name)
                diff_single.write_raw_results(sys.argv[3] + __single + benchmark.name)

                # build the diff results for union
                diff_union = Difference(mutant=benchmark.mutant_results_union, rand=urandom.union_results,
                                        total=utotal.union_results, add=uadditional.union_results)
                diff_union.find_differences_union()
                # write our results to disk
                diff_union.write_results(sys.argv[3] + __union + benchmark.name)
                diff_union.write_raw_results(sys.argv[3] + __union + benchmark.name)
            print tag, "Finished processing: {0} in {1} seconds".format(benchmark.name, int(time.time())-process)
            print tag, "======================="
    print "Finished execution in: {0} seconds".format(int(time.time()) - start)

    if run_limit != -1:
        for x in range(0,10):
            pass
            #print tag, "Ensure you remove the \"limit\" variable before turning this in!!!!!"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print tag, "Usage: python main {/path/to/curated/input.txt} {/path/to/the/benchmark/} {/path/to/the/results/}"
    else:
        main()
