# <a name="title"></a>Test package - `/test_scripts/`
This is a collection of scripts I have used to test the sudoku solver. As there were quite a few of them, I bundled them into a package to stop `test_sudoku.py` from getting too long.

I have also included some test data that can be used with these scripts.
These can be found in [`/data/`](../data).

As well as the data provided by the University of Bath, I have also included a `/custom/` directory containing a few puzzles I have encountered that my solver has found particularly challenging.
You can also find a weekly "Unsolvable" sudoku posted [here](#https://www.sudokuwiki.org/Weekly_Sudoku.aspx?puz=28).

## <a name="links"></a>Links
- [basic_tests](#basic_tests)
- [load_array](#load_array)
- [load_txt_file](#load_txt_file)
- [multiple_batches](#multiple_batches)
- [solve_multiple](#solve_multiple)
- [solve_single](#solve_single)


## <a name="basic_tests"></a>**basic_tests**
This is based on the sudoku testing program from Uni of Bath. It tests against each set of puzzles stored in `/data/` and compares answers against the solutions (also stored in `/data/`).

It takes the argument `use_process_time`. If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.

Usage:
```py
import test_scripts

test_scripts.basic_tests(use_process_time=...)
```

## <a name="all_zeros_test"></a>**all_zeros_test**
Tests the solver by giving it a blank sudoku, i.e. a `(9,9)` NumPy array of `0`s.

It takes the argument `use_process_time`. If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.

Usage:
```py
import test_scripts

test_scripts.all_zeros_test(use_process_time=...)
```

## <a name="already_solved_test"></a>**already_solved_test**
Tests the solver by giving it a solved sudoku. The solver should output the

It takes the argument `use_process_time`. If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.

Usage:
```py
import test_scripts

test_scripts.all_zeros_test(use_process_time=...)
```

## <a name="load_array"></a>**load_array**
Loads an array from a `.npy` or a `.csv` file. If the file does not exist, or appears to be of incorrect format to be a sudoku, raise an error.

Usage:
```py
import test_scripts

test_scripts.load_array(filename=...)
```

## <a name="load_txt_file"></a>**load_txt_file**
Loads an array from a `.txt` file. If the file does not exist, or appears to be of incorrect format to be a sudoku, raise an error.

Usage:
```py
import test_scripts

test_scripts.load_txt_file(filename=...)
```

## <a name="multiple_batches"></a>**multiple_batches**
Runs a test similar to `basic_tests` a set number of times. This is also a lot less verbose than `basic_test` in that it does not print the sudokus or solutions. It also assumes that the sudoku solver is correct for each solve.

It takes two arguments:
- `use_process_time` - If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.

- `num_of_batches` - The number of batches to process (each batch = 1 run of `basic_tests`, 60 sudokus)

Usage:
```py
import test_scripts

test_scripts.multiple_batches(num_of_batches=..., use_process_time=...)
```

## <a name="solve_multiple"></a>**solve_multiple**
Solves multiple sudokus stored in a 3d array and prints the results.

It takes 4 arguments:
- `sudoku_array` - the 3d array of sudokus to solve
- `save_to_file` - whether or not to save results to a file. If you are not interested in the sudoku solutions and only want to know the processing time, then set this to `False`.  Setting it to `True` will make the function return an array of the solutions, but it will significantly increase processing time.
- `use_process_time` - If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.
- `quit_after` - The number of sudokus to stop processing after.

Usage:
```py
import test_scripts

test_scripts.solve_multiple(sudoku_array=...,
                            save_to_file_=...,
                            use_process_time=...,
                            quit_after=...)
```

## <a name="solve_single"></a>**solve_single**
Solves a single sudoku and prints the results.

It takes 3 arguments:
- `sudoku` - the sudoku to solve
- `save_to_file` - whether or not to save results to a file. If you are not interested in the sudoku solutions and only want to know the processing time, then set this to `False`.  Setting it to `True` will make the function return an array of the solutions, but it will significantly increase processing time.
- `use_process_time` - If this is `True`, `time.process_time()` will be used to measure how long the sudoku solver takes. Otherwise it will use `time.perf_counter`.

Usage:
```py
import test_scripts

test_scripts.solve_multiple(sudoku_array=...,
                            save_to_file_=...,
                            use_process_time=...)