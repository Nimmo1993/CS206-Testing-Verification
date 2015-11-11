import re
import ast
import json
from testcases.TestSuite import TestSuite

"""
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov.html
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov-branch.html
regex for 123:} = ^[0-9]+:\}
regex for 123: = ^[0-9]+:
"""
statements = {}
branches = {}


def parse_gcov():
    line_number = 0
    still_branch = False
    branch = []
    with open("/Users/jason/Desktop/cs206/benchmarks/tcas/tcas.c.gcov") as f:
        for line in f:
            split = line.split()
            # Junk or garbage input from gcov
            if split[0] == "-:" or split[0] == "$$$$$:" or split[0] == "function" or "-block" in split[1]:
                continue

            if split[0] != "branch":
                if still_branch:
                    branches[line_number] = branch
                    branch = []
                    still_branch = False
                line_number = int(split[1].strip(":}"))
                statements[line_number] = True if split[0].strip(":") != "#####" else False
            else:
                branch.append(True if int(split[3]) > 0 else False)
                still_branch = True
    return branches

def test_test_suite():
    tests = []
    with open("/Users/jason/Desktop/cs206/tcas.results") as f:
        for line in f:
            tests = json.loads(line)
    test = TestSuite(tests)


if __name__ == "__main__":
    # main()
    test_test_suite()

"""
Statement ground truth:
    {128: True, 132: False, 133: True, 134: True, 135: True, 136: True, 138: True, 139: True, 141: True, 148: True, 150: True, 151: True, 152: True, 153: True, 154: True, 155: True, 157: True, 158: True, 159: True, 160: True, 161: True, 162: True, 163: True, 164: True, 165: True, 166: True, 167: True, 168: True, 169: True, 171: True, 172: True, 173: False, 50: True, 51: True, 52: True, 53: True, 54: True, 58: True, 63: True, 72: True, 73: True, 75: True, 76: True, 79: True, 81: True, 90: True, 91: True, 93: True, 94: True, 97: True, 99: True, 104: True, 109: True, 118: True, 119: True, 120: True, 122: True, 124: True, 126: True, 127: True}
    {128: True, 132: False, 133: True, 134: True, 135: True, 136: True, 138: True, 139: True, 141: True, 148: True, 150: True, 151: True, 152: True, 153: True, 154: True, 155: True, 157: True, 158: True, 159: True, 160: True, 161: True, 162: True, 163: True, 164: True, 165: True, 166: True, 167: True, 168: True, 169: True, 171: True, 172: True, 173: False, 50: True, 51: True, 52: True, 53: True, 54: True, 58: True, 63: True, 72: True, 73: True, 75: True, 76: True, 79: True, 81: True, 90: True, 91: True, 93: True, 94: True, 97: True, 99: True, 104: True, 109: True, 118: True, 119: True, 120: True, 122: True, 124: True, 126: True, 127: True}
Branch ground truth:
    {128: [True, True, False, True], 97: [True, True, True, False], 133: [True, True], 135: [True, True], 73: [True, True], 75: [True, True, True, False], 79: [True, True, True, False], 148: [True, True], 118: [True, True, True, True], 120: [True, True], 127: [True, True], 91: [True, True], 124: [True, True, True, True, True, True, True, True], 93: [True, True, True, False], 126: [True, True], 63: [True, True]}
"""