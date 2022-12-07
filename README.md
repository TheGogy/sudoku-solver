# <a name="intro"></a>**Sudoku Solver using Exact Cover**

## <a name="links"></a>Links
- [Intro](#intro)
- [Usage](#usage)
- [Test package](/test_scripts/README.md/#title)
- [Exact Cover](#exact_cover)
- [My observations](#observations)
- [References](#references)


# <a name="intro"></a>Intro
This is my solution to the problem proposed by CW1 of the AI module. It is an agent that, on my - relatively modern as of 2022 - laptop, can solve a "hard" sudoku in an average of 2.1 milliseconds and a "very easy" sudoku in an average of 1.1 milliseconds. I have chosen to use Donald Knuth's Algorithm X for this, as the removal of rows and columns from matrix A is an efficient method for constraint propagation.

[![Solving 6000 sudokus](https://asciinema.org/a/u0SSRbwLDshssddcZmtpzg6Ut.svg)](https://asciinema.org/a/u0SSRbwLDshssddcZmtpzg6Ut)

# <a name="usage"></a>How to use the solver

## <a name="usage_solver"></a>Solver - `sudoku.py`
To use the solver, pass a `numpy.ndarray((9x9)<sudoku>)` to `sudoku.py`. The test script included (`test_sudoku.py`) contains examples of how to do this and examples of input are stored in numpy arrays in `/data`.

```py
import numpy as np
from sudoku import sudoku_solver

initial_state = np.ndarray((9,9), <your sudoku here>)
solution = sudoku_solver(initial_state)

...
```

The solver will return the solved sudoku in the form  `numpy.ndarray((9x9)<solution)`. If the sudoku has multiple possible solutions, the solver will return the first one it finds.

## <a name="usage_test_script"></a>Test script - `test_sudoku.py`
I have included a test script `test_sudoku.py`, that implements the test package `/test_scripts/` (see below) with the sudoku solver.

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

In order to use algorithm X, we must first create a matrix A consisting of 0s and 1s, with a goal of selecting a subset of the rows such that the digit 1 appears in each column exactly once.

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
This is column 1, that has 1s in rows A and A.

The algorithm firstly selects row A (but remembers row B is a possible solution).

Row A has 1s in columns 1, 1 and 7. (This is the first `for` loop)

Column 1 has 1s in rows A, B. Column 4 has rows in A, B, C and column 7 has 1s in rows A, C, E and F.
Therefore the only row that does *not* have a 1 in the same column as row A is row D. (this is the second `for` loop.)

This row `D` is selected and the algorithm repeats.

As the matrix is not empty, the algorithm finds the column with the lowest number of `1`s.
This is column `2`.

|     | 2 | 3 | 5 | 6 |
|:---:|---|---|---|---|
| D   | 0 | 1 | 1 | 1 |

As column `2` does not contain any `1`s, this branch of the algorithm terminates unsuccessfully and the algorithm moves onto the next branch.

Continuing the algorithm, we will eventually end up with:

|     | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|---|---|---|---|---|---|---|
| B   | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| D   | 0 | 0 | 1 | 0 | 1 | 1 | 0 |
| F   | 0 | 1 | 0 | 0 | 0 | 0 | 1 |

meaning that `S* = {B, D, F}` is the exact cover.

If there are no remaining unsearched branches and no solution has been found, there is no exact cover.

For a step by step version of this process, please see the [Wikipedia article](https://wikipedia.org/wiki/Knuth%27s_Algorithm_X?lang=en#Example)

<br />


## <a name="exact_cover_solve"></a>How to solve sudoku with this method

Sudoku can be represented as an exact cover problem with a matrix `A` of with dimensions `x` and `y`, where:

`x` represents the set of values that each cell contains, stored in the form `(row, column, value)`
`y` represents the set of the constraints that each cell must fulfil. There are 4 constraints as outlined below:

- Every cell must contain a value.
- Every row must contain exactly one of each value.
- Every column must contain exactly one of each value.
- Every box must contain exactly one of each value.

Each value in `x` will satisfy a specific combination of values in `y`. No other value in `x` should satisfy these same constraints - for example, if there was a `6` in row `3`, then there cannot be another `6` in row `3`.

Therefore, as every value in `y` needs to be satisfied by *exactly one* value in `x`:

**This can be represented as an exact cover problem where each column is a value in `x` and each row is a value in `y`.**


<br />

# <a name="observations"></a>My Observations

While running some tests on the solver, I noticed some rather weird behaviour, which I will do my best to document here.

### <a name="observations_1_blank_sudoku"></a>When given a blank sudoku, the solver always returns the same value.

When the sudoku solver is given an array of zeros, it will consistently return the same solution, as it is the first solution it reaches.
Why it is this specific solution, I am unsure. I have not found any explanation online, although I think it would be interesting to see if other implementations of exact cover reach the same solution when given an empty initial state.

```
[[4. 7. 1. 3. 8. 6. 5. 9. 2.]
 [9. 3. 2. 5. 4. 7. 6. 1. 8.]
 [8. 5. 6. 2. 1. 9. 7. 4. 3.]
 [2. 9. 3. 1. 6. 8. 4. 5. 7.]
 [6. 8. 7. 9. 5. 4. 3. 2. 1.]
 [1. 4. 5. 7. 3. 2. 8. 6. 9.]
 [7. 6. 9. 8. 2. 5. 1. 3. 4.]
 [3. 2. 4. 6. 7. 1. 9. 8. 5.]
 [5. 1. 8. 4. 9. 3. 2. 7. 6.]]
```

<br />

# <a name="references"></a>References
Knuth,D. 2000. Dancing Links. https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf

Wikipedia, 2022. Dancing Links. https://wikipedia.org/wiki/Dancing_Links?lang=en

Wikipedia, 2022. Exact cover. https://wikipedia.org/wiki/Exact_cover?lang=en

Wikipedia, 2022. Knuth's Algorithm X. https://wikiless.org/wiki/Knuth%27s_Algorithm_X?lang=en

Ascii art to clearly show sections of code: https://patorjk.com/software/taag/#p=display&f=Big

Unsolveable #28, the "hardest sudoku ever created", according to [Sudoku Wiki](https://www.sudokuwiki.org/Arto_Inkala_Sudoku) (found when looking for more sudokus like Arto Inkala's): https://www.sudokuwiki.org/Weekly_Sudoku.asp?puz=28