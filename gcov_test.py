import re

"""
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov.html
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov-branch.html
regex for 123:} = ^[0-9]+:\}
regex for 123: = ^[0-9]+:
"""
results = {}


def run_parser():
    line_number = 0
    still_branch = False
    branches = []
    with open("/Users/jason/Desktop/cs206/benchmarks/tcas/tcas.c.gcov") as f:
        for line in f:
            split = line.split()
            print split
            # Junk or garbage input from gcov
            if split[0] == "-:" or split[0] == "$$$$$:" or split[0] == "#####:" or split[0] == "function":
                continue

            if split[0] != "branch":
                if still_branch:
                    results[line_number] = branches
                    branches = []
                    still_branch = False
                line_number = int(split[1].strip(":}"))
            else:
                branches.append(True if int(split[3]) > 0 else False)
                still_branch = True
    return results

if __name__ == "__main__":
    # main()
    run_parser()
    # print coverage
    print results
