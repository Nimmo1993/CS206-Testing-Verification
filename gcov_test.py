
"""
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov.html
http://www.cs.odu.edu/~cs333/website-latest/Lectures/wbtesting/pages/gcov-branch.html

"""


def main():
    with open("/Users/jason/Desktop/cs206/benchmarks/tcas/tcas.c.gcov") as f:
        for line in f:
            print line

if __name__ == "__main__":
    main()
