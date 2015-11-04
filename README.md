# cs206-Testing-Verification
Testing software suite for Testing and Verification

## Dependencies
1. This was built using python 2.7.10
2. This program relies upon the [**gcovr**](http://gcovr.com/guide.html).  As per gcovr's documentation the easiest way to install it is: [_pip install gcovr_](http://gcovr.com/guide.html#installation)

## Using this program
Running this program is very simple.  It takes 2 arguments:

1. /path/to/curated/input.txt (the provided is sufficient for the curse)
2. /path/to/the/benchmark

## How this program works
Essentially this program flows accordingly:

1. Build a benchmark for each benchmark defined in the "input.txt" file
2. Compile the program once with the following flags: _gcc -fprofile-arcs -ftest-coverage -fPIC input.c -o out_
3. For every test input in _universe.txt_ we run the program and evaluate the [file].gcda and [file].gcno in order to evaluate coverage
4. We then will sort the lists of coverage by the appropriate implementations
5. We will then begin testing the mutations given our reduced test set
6. Generate the results and profit!