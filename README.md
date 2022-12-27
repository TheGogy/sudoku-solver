# <a name="intro"></a>**Sudoku Solver using Exact Cover and Algorithm X**

## <a name="links"></a>Links
- [Intro](#intro)
- [Usage](#usage)
- [Exact Cover](#exact_cover)
- [My Implementation](#my_implementation)
- [My Observations](#observations)
- [Improvements and Optimisations](#improvements)
- [More Sudokus](#more_sudokus)
- [References](#references)

- - -
- [Test package](/test_scripts/README.md/#title)

# <a name="intro"></a>Intro
This is my solution to the problem proposed by CW1 of the AI module. It is an agent that, on my i5-11400h processor, can solve a sudoku in an average of 0.75 milliseconds. I have chosen to use Donald Knuth's Algorithm X for this, as the removal of rows and columns from matrix A is an efficient method for constraint propagation.

# <a name="usage"></a>How to use the solver

## <a name="usage_solver"></a>Solver - `sudoku.py`
To use the solver, pass a `numpy.ndarray((9x9)<sudoku>)` to [`sudoku.py`](#sudoku.py). The test script included ([`test_sudoku.py`](#test_sudoku.py)) contains examples of how to do this and examples of input are stored in numpy arrays in [`/data/`](#/data/).

```py
import numpy as np
from sudoku import sudoku_solver

initial_state = np.ndarray((9,9), <your sudoku here>)
solution = sudoku_solver(initial_state)

...
```

The solver will return the solved sudoku in the form  `numpy.ndarray((9x9)<solution)`. If the sudoku has multiple possible solutions, the solver will return the first one it finds.

## <a name="usage_test_script"></a>Test script - [`test_sudoku.py`](#test_sudoku.py)
I have included a test script [`test_sudoku.py`](#test_sudoku.py), that implements the test package [`test_scripts.py`](#/test_scripts/) (see below) with the sudoku solver.

 Usage is as follows:
 ```
Usage:
    test_sudoku.py [ -q , -p , -o , -h|-n|-m|-f ] <batches | filename>

Tests sudoku solver with various puzzles.

Options:
    -h, --help              Show help.

    -n, --normal            Run test as normal.

    -m, --multiple          Run <batches> tests of normal test.

    -f, --file              Solve a sudoku stored in a file
                            [*.txt, *.npy]

    -o, --output-to-file    Output the solutions to a .npy file
                            (use with -f)

    -p, --use-process-time  Use time.process_time() instead of
                            time.perf_counter()

    -q, --quit-after        Stop solving sudokus after it has solved a certain
                            number. Used with "-f" on .npy and .csv files.
 ```



<br />

# <a name="exact_cover"></a>Exact Cover

Exact cover is the method the sudoku solver uses in order to solve the sudoku.

It is defined as a collection `S` of subsets of a set `X` such that each element in `X` exists in exactly one subset in `S*`. [(Wikipedia)](https://wikipedia.org/wiki/Exact_cover?lang=en)

## <a name="exact_cover_example"></a>Example

Let `S = {A, B, C, D, E, F}` be a collection of subsets of a set `X` such that:

- `A = {1, 4, 7}`
- `B = {1, 4}`
- `C = {4, 5, 7}`
- `D = {3, 5, 6}`
- `E = {2, 3, 6, 7}`
- `F = {2, 7}`

The exact cover of `X` would be `S* = {B, D, F}` as:

- ```B ∪ D ∪ F = X```<br /> **(`S*` covers every element in `X`)**

- ```B ∩ D ∩ F = {}``` <br /> **(every element in `X` is covered by exactly one element in `S*`)**

<br />

## <a name="exact_cover_solve"></a>Algorithm X - how to solve exact cover problems

In order to use Algorithm X, we must first create a matrix A consisting of 0s and 1s, with a goal of selecting a subset of the rows such that the digit 1 appears in each column exactly once.

Algorithm X takes an element e in `A` to cover, and finds a row r that covers it. This row is added to the potential solution, and every row that also covers e is removed from `A` along with every column that r satisfies. It then repeats this process recursively.


The algorithm is presented with the following pseudocode:
```md
If A is empty, the problem is solved; terminate successfully.
Otherwise:
    choose a column, c (deterministically).
    Choose a row, r, such that A[r, c] = 1 (nondeterministically).
    Include r in the partial solution.
    For each column j such that A[r, j] = 1,
        delete column j from matrix A;
        for each row i such that A[i, j] = 1,
            delete row i from matrix A.
    Repeat this algorithm recursively on the reduced matrix A.
```
(Knuth, 2000) - [Page 4](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)

The above problem can be represented with the matrix:


|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| A   | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| B   | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| C   | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| D   | 0 | 0 | 1 | 0 | 1 | 1 | 0 |
| E   | 0 | 1 | 1 | 0 | 0 | 1 | 1 |
| F   | 0 | 1 | 0 | 0 | 0 | 0 | 1 |

Firstly, as matrix `A` is not empty, the algorithm finds the column with the lowest number of 1s.
This is column 1, that has 1s in rows A and B.

|     | 1 |
|:---:|---|
| A   | **1** |
| B   | **1** |
| C   | 0 |
| D   | 0 |
| E   | 0 |
| F   | 0 |

The algorithm firstly selects row A (but remembers row B is a possible solution).

Row A has 1s in columns 1, 4 and 7. (This is the first `for` loop)

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| A   | **1** | 0 | 0 | **1** | 0 | 0 |**1** |

Column 1 has 1s in rows A, B. Column 4 has rows in A, B, C and column 7 has 1s in rows A, C, E and F.
Therefore the only row that does *not* have a 1 in the same column as row A is row D (this is the second `for` loop.).

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| A   | **1** | 0 | 0 | **1** | 0 | 0 | **1** |
| B   | **1** | 0 | 0 | **1** | 0 | 0 | **0** |
| C   | **0** | 0 | 0 | **1** | 1 | 0 | **1** |
| D   | **0** | 0 | 1 | **0** | 1 | 1 | **0** |
| E   | **0** | 1 | 1 | **0** | 0 | 1 | **1** |
| F   | **0** | 1 | 0 | **0** | 0 | 0 | **1** |

Therefore, row `D` is selected and the algorithm repeats.

As the matrix is not empty, the algorithm finds the column with the lowest number of `1`s.
This is column `2`.

|     | 2 | 3 | 5 | 6 |
|:---:|---|---|---|---|
| D   | **0** | 1 | 1 | 1 |

As column `2` does not contain any `1`s, this branch of the algorithm terminates unsuccessfully and the algorithm moves onto the next branch, which in this case would be row B.

Continuing the algorithm, we will eventually end up with:

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| B   | **1** | 0 | 0 | **1** | 0 | 0 | 0 |
| D   | 0 | 0 | **1** | 0 | **1** | **1** | 0 |
| F   | 0 | **1** | 0 | 0 | 0 | 0 |**1** |

meaning that `S* = {B, D, F}` is the exact cover.

If there are no remaining unsearched branches and no solution has been found, there is no exact cover.

For a step by step version of this process, please see the [Wikipedia article](https://wikipedia.org/wiki/Knuth%27s_Algorithm_X?lang=en#Example).

<br />


## <a name="exact_cover_solve"></a>How to solve sudoku with this method

Sudoku can be represented as an exact cover problem with a matrix `A` of with dimensions `x` and `y`, where:

- `x` represents the set of values that each cell contains, stored in the form `(row, column, value)`
- `y` represents the set of the constraints that each cell must fulfil. There are 4 constraints as outlined below:

- Every cell must contain a value.
- Every row must contain exactly one of each value.
- Every column must contain exactly one of each value.
- Every box must contain exactly one of each value.

Each value in `x` will satisfy a specific combination of values in `y`. No other value in `x` should satisfy these same constraints - for example, if there was a `6` in row `3`, then there cannot be another `6` in row `3`.

Therefore, as every value in `y` needs to be satisfied by *exactly one* value in `x`:

**This can be represented as an exact cover problem where each column is a value in `x` and each row is a value in `y`.**

# <a name="my_implementation"></a>My implementation

## <a name="translating"></a>Translating sudoku to an exact cover problem

The solver firstly constructs `matrix_A`. The code for this is as follows:
```py
    matrix_A = {j: set() for j in(
        [("cell", i) for i in product (range(9), range(9)    )] +
        [("row",  i) for i in product (range(9), range(1, 10))] +
        [("col",  i) for i in product (range(9), range(1, 10))] +
        [("box",  i) for i in product (range(9), range(1, 10))]
    )}

    constraints = get_constraints()

    # Populate matrix A with constraints
    for i, consts in constraints.items():
        for j in consts:
            matrix_A[j].add(i)
```

`get_constraints()` is a function that returns the constraints dict and caches and returns the constraints dict.
Shown below.
```py
# Cache the constraints dict; this is not updated and can be re-used.
@memoize
def get_constraints() -> dict:
    '''
    Gets the general constraint dict for all sudokus.

    @returns:
        constraints (dict) : Constraints dictionary
    '''
    constraints = {}
    for row, col, cell in product(range(9), range(9), range(1, 10)):
        box = (row // 3) * 3 + (col // 3)
        # Boxes are labelled like this:
        #   0 1 2
        #   3 4 5
        #   6 7 8
        constraints[(row, col, cell)] = [
            # Each cell must have a value
            ("cell", (row, col)),
            # Each row must have each value
            ("row",  (row, cell)),
            # Each column must have each value
            ("col",  (col, cell)),
            # Each box must have each value
            ("box",  (box, cell))
        ]
    return constraints
```

This creates a matrix as follows:

|     | (0,0,1) | (0,0,2) | (0,0,3) | ... |
|:---:|:---:|:---:|:---:|:---:|
| cell (0,0) contains value     | 1 | 0 | 0 | ... |
| cell (0,1) contains value     | 0 | 0 | 0 | ... |
| cell (...) contains value     | ... | ... | ... | ... |
| row  (0)   contains value 1   | 1 | 0 | 0 | ... |
| row  (0)   contains value 2   | 0 | 1 | 0 | ... |
| row  (...) contains value ... | ... | ... | ... | ... |
| col  (0)   contains value 1   | 1 | 0 | 0 | ... |
| col  (0)   contains value 2   | 0 | 1 | 0 | ... |
| col  (...) contains value ... | ... | ... | ... | ... |
| box  (0)   contains value 1   | 1 | 0 | 0 | ... |
| box  (0)   contains value 2   | 0 | 1 | 0 | ... |
| box  (...) contains value ... | ... | ... | ... | ... |


Once the initial matrix has been generated, we can update the constraints to reflect the initial state - to remove the rows and columns that we know are incorrect. If our original sudoku contains the value `(0,5,3)` for example, then we can remove all columns that imply a different value at that location, such as `(0,5,2)`.
If the value of any given cell does not exist, the sudoku is not solvable.

This is completed with the code below:
```py
    # Update constraints to reflect initial state
    for (row, col), cell in ndenumerate(sudoku):
        if cell != 0:
            try:
                select(matrix_A, constraints, (row, col, cell))
            except KeyError:
                # Sudoku is not solvable
                return full((9, 9), fill_value=-1)
```

We can then proceed onto <u> **Algorithm X** </u>.

## <a name="Algorithm X"></a>Algorithm X


```py
def find_solution(matrix_A, constraints, solution=[]) -> list:
    '''
    Recursively attempts to find a solution

    @args
        matrix_A: The search space matrix
        constraints: The constraints dict
        solution: The state to find (or not find) soltion for

    @returns list: The solution
    '''
    if not matrix_A:
        # There are no constraints left to fulfil; sudoku solved.
        yield list(solution)
    else:
        col = choose_col(matrix_A, constraints)
        for row in list(matrix_A[col]):
            solution.append(row)
            cols = select(matrix_A, constraints, row)

            # Keep trying to find solution recursively
            for i in find_solution(matrix_A, constraints, solution): yield i

            # This row does not have a solution, deselect it
            deselect(matrix_A, constraints, row, cols)
            solution.pop()
```
This is the recursive backtracking algorithm that attempts to find the solution to the given sudoku.

If `matrix_A` is empty, we have fulfilled all the constraints and thus solved the sudoku.

Otherwise, find the column with the fewest values in `matrix_A` using the algorithm below:

```py
def choose_col(matrix_A, constraints):
    """
    Returns col with fewest possible values.

    @args
        matrix_A: the search space matrix
        constraints: The constraints dict

    @returns
        col : the column with the fewest possible values
    """

    best_col_val = float("inf")
    best_col = None

    for col in matrix_A:
        cur_col_val = len(matrix_A[col])

        if best_col_val > cur_col_val:

            best_col = col
            best_col_val = cur_col_val

            # Do not waste time if we have already found a column with only
            # one value
            if cur_col_val == 1:
                return best_col

    return best_col
```

This returns the selected column. Append it to the partial solution.

The associated rows and columns are then removed from the matrix:
```py
def select(matrix_A, constraints, row) -> list:
    '''
    removes associated rows, cols from matrix
    @args:
        matrix_A: the search space matrix
        constraints: the constraints dict
        row: The row to be selected

    @returns:
        cols (list): List of removed columns
    '''
    # Keep removed columns so they can be added back into sudoku
    cols = []

    # For each constraint this row satisfies:
    for i in constraints[row]:

        # For all other constraints that also satisfy i:
        for j in matrix_A[i]:

            # For all other constraints that j satisfies:
            for k in constraints[j]:

                # Remove all other constraints except i
                if k != i:
                    matrix_A[k].remove(j)

        cols.append(matrix_A.pop(i))

    return cols
```

And the program recursively tries again.

If the program has exhausted all the possible solutions on a given branch, it will then deselect it and return the removed values back into matrix A:

```py
def deselect(matrix_A, constraints, row, cols) -> None:
    '''
    Restores a branch with a no solutions back into matrix_A

    @args:
        matrix_A: The search space matrix
        constraints: the constraints dict
        cols: Columns to restore into matrix_A
    '''
    for i in reversed(constraints[row]):

        # Get top column from list of removed columns
        matrix_A[i] = cols.pop()

        # For each other value that satisfies constraint:
        for j in matrix_A[i]:

            # For other constraints that value satisfies:
            for k in constraints[j]:

                # Add value back into matrix_A
                matrix_A[k].add(j)
```

## <a name="translating_back"></a>Translating the solved exact cover problem back to a sudoku

When `find_solution` has found and returned a solution, it will be in the form of a list of tuples containing the remaining values to put back into the sudoku.
The solver then fills those values into the original sudoku, avoiding making a copy in order to save processing time.

```py
    # find solution and update initial state with it
    for solution in find_solution(matrix_A, constraints, []):
        for (row, col, val) in solution:
            # Fill original values directly into input sudoku to save time
            sudoku[row][col] = val
        return sudoku
```

If `find_solution` has exhausted all possible branches, then there is no possible solution and hence the solver will return the error grid:
```py
return full((9, 9), fill_value=-1)
```

<br />

# <a name="observations"></a>My Observations

While running some tests on the solver, I noticed some rather weird behaviour, which I will do my best to document here.

## <a name="observations_1_blank_sudoku"></a>When given a blank sudoku, the solver always returns the same value.

When the sudoku solver is given an array of zeros, it will consistently return the same solution, as it is the first solution it reaches.
Why it is this specific solution, I am unsure. I have not found any explanation online, although I think it would be interesting to see if other implementations of Algorithm X reach the same solution when given an empty initial state.

```
+-------+-------+-------+
| 4 7 1 | 3 8 6 | 5 9 2 |
| 9 3 2 | 5 4 7 | 6 1 8 |
| 8 5 6 | 2 1 9 | 7 4 3 |
+-------+-------+-------+
| 2 9 3 | 1 6 8 | 4 5 7 |
| 6 8 7 | 9 5 4 | 3 2 1 |
| 1 4 5 | 7 3 2 | 8 6 9 |
+-------+-------+-------+
| 7 6 9 | 8 2 5 | 1 3 4 |
| 3 2 4 | 6 7 1 | 9 8 5 |
| 5 1 8 | 4 9 3 | 2 7 6 |
+-------+-------+-------+
```

I believe that it has something to do with how the compiler treats data stored in lists and dictionaries, as when the code is run using [pypy3](#https://www.pypy.org/), it produces a different result when given the same test:

```
+-------+-------+-------+
| 1 2 3 | 4 5 6 | 7 8 9 |
| 7 8 9 | 1 2 3 | 4 5 6 |
| 4 5 6 | 7 8 9 | 1 2 3 |
+-------+-------+-------+
| 3 1 2 | 8 4 5 | 9 6 7 |
| 6 9 7 | 3 1 2 | 8 4 5 |
| 8 4 5 | 6 9 7 | 3 1 2 |
+-------+-------+-------+
| 2 3 1 | 5 7 4 | 6 9 8 |
| 9 6 8 | 2 3 1 | 5 7 4 |
| 5 7 4 | 9 6 8 | 2 3 1 |
+-------+-------+-------+
```


<br />

# <a name="improvements"></a>Improvements and optimisations
### <a name="custom_min"></a>Custom min() function

My original method for finding the best possible column to choose used the built in min() function from python, with the line shown below.
```py
col = min(matrix_A, key=lambda i: len(matrix_A[i]))
```
This function was inefficient, as even when it had found a column with only one single branch, it would keep iterating through the columns to find a lower value, although the value cannot be lower than 1.

My solution was to write my own function, as shown below.
```py
def choose_col(matrix_A, constraints):
    """
    Returns col with fewest possible values.

    @args
        matrix_A: the search space matrix
        constraints: The constraints dict

    @returns
        col : the column with the fewest possible values
    """

    best_col_val = float("inf")
    best_col = None

    for col in matrix_A:
        cur_col_val = len(matrix_A[col])

        if best_col_val > cur_col_val:

            best_col = col
            best_col_val = cur_col_val

            # Do not waste time if we have already found a column with only
            # one value
            if cur_col_val == 1:
                return best_col

    return best_col
```
This reduced the average solve time of any given puzzle from about 2ms to about 1.7ms.

<br />

### <a name="cache_constraints"></a>Caching the constraints dict

As the constraints dict is not altered between sudokus, it can be cached so that it does not have to be calculated multiple times.
This is done by making use of the memoize wrapper, shown below:
```py
def memoize(func):
    '''
    Caches the result of a function for later use.

    @args:
        func: the function to cache

    @returns:
        wrapper: The wrapper to cache the output of the function
    '''
    # Cache dictionary
    cache = {}

    def wrapper(*args):
        # If values are not cached, add to cache
        if args not in cache:
            cache[args] = func(*args)

        # Return cached values
        return cache[args]
    return wrapper
```
This reduced the solve time for an average sudoku from 1.7ms to 0.75ms.

### <a name="compare_pointers"></a>Comparing pointers instead of hashes for dictionary

For matrix_A, as there are many key values looked up, it is faster to compare the pointers to the values instead of the hashes of the values themselves.

This can be done with the builtin `sys.intern` function, as shown below:

```py
 matrix_A = {j: set() for j in(
        [intern(("cell {}".format(i))) for i in product (range(9), range(9)    )]
        ...
 )}
```
and:

```py
constraints[(row, col, cell)] = [
            # Each cell must have a value
            ("cell ({}, {})".format(row, col)),
            ...
]
```

This reduced the average solve time from 0.75ms to 0.7ms.


<br />

# <a name="more_sudokus"></a>More Sudokus

These are a few resources I used to test the solver. I used the 1 million sudoku dataset in order to get an average solve time.

1 million sudoku games: https://www.kaggle.com/datasets/bryanpark/sudoku

9 million sudoku games: https://www.kaggle.com/datasets/rohanrao/sudoku

You can also find a weekly "Unsolvable" sudoku posted [here](https://www.sudokuwiki.org/Weekly_Sudoku.aspx?puz=28).

# <a name="references"></a>References
Knuth, D. 2000. Dancing Links. https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf [accessed Dec 2022]

Wikipedia, 2022. Dancing Links. https://wikipedia.org/wiki/Dancing_Links?lang=en [accessed Dec 2022]

Wikipedia, 2022. Exact cover. https://wikipedia.org/wiki/Exact_cover?lang=en [accessed Dec 2022]

Wikipedia, 2022. Knuth's Algorithm X. https://wikiless.org/wiki/Knuth%27s_Algorithm_X?lang=en [accessed Dec 2022]

Gillespie, P. (n.d). Text to Ascii Art Generator (TAAG): https://patorjk.com/software/taag/#p=display&f=Big [accessed Dec 2022]

Inkala, A. 2012. Arto Inkala's Monster sudoku: https://www.sudokuwiki.org/Arto_Inkala_Sudoku [accessed Dec 2022]

Inkala, A. 2006. Escargot: https://www.sudokuwiki.org/Escargot [accessed Dec 2022]

pyutils, 2022. line_profiler https://github.com/pyutils/line_profiler [accessed Dec 2022]

Park, K. 2014. 1 million Sudoku games: https://www.kaggle.com/datasets/bryanpark/sudoku [accessed Dec 2022]

Rohanrao, 2019. 9 million Sudoku Puzzles and Solutions: https://www.kaggle.com/datasets/rohanrao/sudoku [accessed Dec 2022]

Sudoku Wiki. (n.d.). Weekly Unsolvable puzzle: https://www.sudokuwiki.org/Weekly_Sudoku.asp?puz=28 [accessed Dec 2022]

Blender, 2013. How to import all modules in dir: https://stackoverflow.com/questions/16852811/python-how-to-import-from-all-modules-in-dir [accessed Dec 2022]