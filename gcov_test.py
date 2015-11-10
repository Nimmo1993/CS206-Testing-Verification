import re

"""
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov.html
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov-branch.html
regex for 123:} = ^[0-9]+:\}
regex for 123: = ^[0-9]+:
"""
methods = []

def run_parser():
    quit_1 = False
    # must be external to the loop in order to add the last function
    method_name = None
    result = []
    executed = 0
    with open("/Users/jason/Desktop/cs206/benchmarks/tcas/tcas.c.gcov") as f:
        for line in f:
            split = line.split()
            # Junk or garbage input from gcov
            if split[0] == "-:" or split[0] == "$$$$$:":
                continue

            # print split

            # this is the edge case of a first time method
            if split[0] == "function" and method_name is None:
                method_name = split[1]
                executed = int(split[8].strip(':%'))
                continue

            # this means we have hit a new function!
            if split[0] == "function" and method_name is not None:
                methods.append({'name': method_name, 'lines': result, '% executed': executed})
                # change the method name!
                method_name = split[1]
                # change the execution count!
                executed = int(split[8].strip(':%'))
                # reset the results
                result = []
                continue

            # we don't care about branches here...
            if split[0] == "branch":
                continue

            # Special case, this means the code wasn't executed!
            if split[0] == "#####:":
                result.append({'line_number': int(split[1].strip(':%}')), 'times_executed': 0})
                continue

            # Do the important parsing here!
            line_number = int(split[1].strip(':-block}'))
            execution_times = int(split[0].strip(':'))
            if execution_times != "-":
                result.append({'line_number': line_number, 'times_executed': execution_times})

        # add the last result to the list of dicts!
        methods.append({'name': method_name, 'lines': result, '% executed': executed})

if __name__ == "__main__":
    # main()
    run_parser()
    for x in methods:
        print "{0} was executed {1}%".format(x['name'], x['% executed'])
        for line in x['lines']:
            print line
        print "======"
        # for line, execution in enumerate(method):
            # print "Line: {0} was executed: {1}".format(line, execution)
