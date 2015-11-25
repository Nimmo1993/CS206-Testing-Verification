# cs206-Testing-Verification
Testing software suite for Testing and Verification

## Dependencies
1. This was built using python 2.7.10

## Using this program
Running this program is very simple.  It takes 3 arguments:

1. /path/to/curated/input.txt (the provided is sufficient for the course)
2. /path/to/the/benchmark/
3. /path/to/the/results/

e.g.:
```
python main.py /path/to/curated/input.txt /path/to/benchmarks/ /path/to/the/results
```

## How this program works
Essentially this program flows accordingly:

1. Build a benchmark for each benchmark defined in the "input.txt" file
2. Compile the program once with the following flags: *gcc -ansi -Wno-implicit-int Wno-return-type --coverage -fprofile-arcs -ftest-coverage -fPIC input.c -o out input.c*
3. For every test input in *universe.txt*  we run the program and evaluate the [file].gcda and [file].gcno in order to obtain coverage
4. Sort the lists of coverage by the appropriate prioritization methods
5. Begin testing the mutations given our reduced test suite
6. Tabulate the results and get 100%

## A sample input.txt file is provided:

 tcas~gcc -g -o tcas tcas.c~tcas [int] [int] [int] [int] [int] [int] [int] [int] [int] [int] [int]~null~universe.txt
 
 schedule~gcc -g -o schedule schedule.c~schedule 5 1 1 < input/dat027~input~universe.txt
 
 totinfo~gcc -g -o totinfo totinfo.c -lm~totinfo < universe/jkAdl.mat~universe~universe.txt
 
 printtokens2~gcc -g -o printtokens2 printtokens2.c~printtokens2 < inputs/newtst122.tst~inputs~universe.txt
 
 schedule2~gcc -g -o schedule2 schedule2.c~schedule2 5 1 1 < input/dat027~input~universe.txt
 
 printtokens~gcc -g -o printtokens printtokens.c~printtokens < inputs/newtst122.tst~inputs~universe.txt
 
 replace~gcc -g -o replace replace.c -lm~replace '@|' 'E)m' < input/ruin.1373~input, moni, temp-test~universe.txt
 
 ------------------
 
 You could copy and paste the above into a file and the program will work from there.
 
## Errata:
As with any piece of software, there are bugs.  If only there was a way to automatically detect these…oh wait!  In any event, all these issues are minor in nature and create a miniscule headache for the user.

### Core Dump issue
I have discovered a core dump problem while running replace.  I have tested this on 3 different Linux distributions (Debian-based, Redhat-based, and FreeBSD-based) and the core dump occurs on all three.  More specifically, this problem arose for me with *mutant 27* and the test *‘%A[0-9]?@\*\*[a-c][^0-9]$’ ‘@%&a’ < temp-test/672.inp.292.11*.  In order to get replace to compile I had to add the *–ansi* flag to gcc.  This is because the compiler, on 3 different OSes, was complaining about redefining *getline()*.  When I compiled with –ansi this error would disappear.  This allowed me to run the program successfully.  However, my hypothesis is derived from a warning that is given when I compile replace.c: “incompatible implicit declaration of built-in function ‘abort’ abort()”.  When I gdb the core, it really gives me nothing more than “Program was terminated with signal SIGABRT, Aborted”.  In any event, the gcov/gcda files are never created and I have to accommodate that in my program.  I accommodate this problem in the program itself.

### Union results writing
I have looked into this problem for quite some time and cannot discern the root cause.  The problem is that when running multiple tests, the union results will not write to disk correctly.  However, when one runs the program with one single test case the union results will be written to disk.  This is such a minor inconvenience that it is worth noting, but I wanted to report it so that you knew I was aware of this problem.
