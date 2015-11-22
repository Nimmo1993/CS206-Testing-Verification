# cs206-Testing-Verification
Testing software suite for Testing and Verification

## Dependencies
1. This was built using python 2.7.10

## Using this program
Running this program is very simple.  It takes 2 arguments:

1. /path/to/curated/input.txt (the provided is sufficient for the course)
2. /path/to/the/benchmark/
3. /path/to/the/results/

## How this program works
Essentially this program flows accordingly:

1. Build a benchmark for each benchmark defined in the "input.txt" file
2. Compile the program once with the following flags: _gcc -fprofile-arcs -ftest-coverage -fPIC input.c -o out input.c_
3. For every test input in _universe.txt_ we run the program and evaluate the [file].gcda and [file].gcno in order to evaluate coverage
4. We then will sort the lists of coverage by the appropriate implementations
5. We will then begin testing the mutations given our reduced test set
6. Generate the results and profit!

## A sample input.txt file is provided:

 tcas~gcc -g -o tcas tcas.c~tcas [int] [int] [int] [int] [int] [int] [int] [int] [int] [int] [int]~null~universe.txt
 
 schedule~gcc -g -o schedule schedule.c~schedule 5 1 1 < input/dat027~input~universe.txt
 
 totinfo~gcc -g -o totinfo totinfo.c -lm~totinfo < universe/jkAdl.mat~universe~universe.txt
 
 printtokens2~gcc -g -o printtokens2 printtokens2.c~printtokens2 < inputs/newtst122.tst~inputs~universe.txt
 
 schedule2~gcc -g -o schedule2 schedule2.c~schedule2 5 1 1 < input/dat027~input~universe.txt
 
 printtokens~gcc -g -o printtokens printtokens.c~printtokens < inputs/newtst122.tst~inputs~universe.txt
 
 replace~gcc -g -o replace replace.c -lm~replace '@|' 'E)m' < input/ruin.1373~input, moni, temp-test~universe.txt