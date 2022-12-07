# <a name="intro"></a>Sudoku Solver using Exact Cover
This is my solution to the problem proposed by CW1 of the AI module. It is an agent that, on my - relatively modern as of 2022 - laptop, can solve a "hard" sudoku in an average of 3.85 milliseconds and a "very easy" sudoku in an average of 1.28 milliseconds. I have chosen to use Donald Knuth's Algorithm X for this, as the removal of rows and columns from matrix A is an efficient method for constraint propagation.


## <a name="links"></a>Links
- [Intro](#intro)
- [Usage](#usage)
- [Exact Cover](#exact_cover)
- [My implementation](#my_implementation)
- [Edge Cases and drawbacks](#edge_cases)
- [Future Improvement](#future_improvement)
- [Solving the "hardest sudoku ever"](#hardest_sudoku)
- [My observations](#observations)
- [References](#references)

# <a name="usage"></a>How to use the solver
To use the solver, pass a `numpy.ndarray((9x9)<sudoku>)` to `sudoku.py`. The test script included (`test_sudoku.py`) contains examples of how to do this and examples of input are stored in numpy arrays in `/data`.

```py
import numpy as np
from sudoku import sudoku_solver

initial_state = np.ndarray((9,9), <your sudoku here>)
solution = sudoku_solver(initial_state)

...
```

The solver will return the solved sudoku in the form  `numpy.ndarray((9x9)<solution)`. If the sudoku has multiple possible solutions, the solver will return the first one it finds.

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

Algorithm X takes an element `e` in `A` to cover, and finds a row `r` that covers it. This row is added to the potential solution, and every row that also covers `e` is removed from `A` along with every column that `r` satisfies. It then repeats this process recursively


The algorithm is presented with the following pseudocode:
```md
If A is empty, the problem is solved; terminate successfully.
Otherwise:
    choose a column, c (deterministically).
    Choose a row, r, such that A[r, c] = 1 (nondeterministically).
    Include r in the partial solution.
    For each j such that A[r, j] = 1,
        delete column j from matrix A;
        for each i such that A[i, j] = 1,
            delete row i from matrix A.
    Repeat this algorithm recursively on the reduced matrix A.
```
(Knuth, 2000) - [Page 4](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf)

<br />

# <a name="observations"></a>My Observations

While running some tests on the solver, I noticed some rather weird behaviour, which I will do my best to document here.

<br />

## <a name="observations_1_blank_sudoku"></a>When given a blank sudoku, the solver always returns the same value.

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

## <a name="observations_2_v_easy_not_easiest"></a>The solver reduces average time significantly by solving more puzzles
When running tests on varying difficulties, I found that if I ran the test script on the solver with both "easy" and "medium", this would reduce the average solve time by about 20% compared to solving either "easy" or "medium" individually.

This can be reproduced by:

in `test_scripts/basic_tests.py`, change line 12 to:
```py
...
    '''
    and compares answers against the solutions (also stored in /data/).
    '''

    difficulties = ['easy', 'medium']   # <---- Change line to this
#    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    total_time = 0
    total_correct = 0
...
```
and by calling the test script with this line:
```
python test_sudoku.py -p -n
```
The average time, as calculated by `time.perf_counter()`:
```
difficulties = ['easy', 'medium']
AVERAGE TIME             0.001978670533268693
```
although when the line is set to `difficulties = ['very_easy']`the output changes to:
```
difficulties = ['very_easy']
AVERAGE TIME             0.0025217442666568483
```
Thinking this might be because the solver is fast at finding "medium" puzzles, I set the line to `difficulties = ['medium']` and got an output similar to "very_easy":

```
difficulties = ['medium']
AVERAGE TIME             0.0025053513994256114
```
And again for "easy" difficulty:
```
difficulties = ['easy']
AVERAGE TIME             0.0024232690000644654
```
And finally, running both "very_easy" and "easy" difficulties at once we get an output similar to running both "medium" and "easy" at once:
```
difficulties = ['very_easy', 'easy']
AVERAGE TIME             0.0019366133001919176
```
But the fastest average solve time is when the solver solves the "very_easy", "easy" and "medium" puzzles at once, which gives this result:
```
difficulties = ['very_easy', 'easy', 'medium']
AVERAGE TIME             0.0017157262444320237
```

As we can see from the tests, it appears that it can solve easy puzzles fastest, followed by medium, very easy and finally hard. But when it tests both "easy" and "medium", or "very_easy" and "easy" at once, there is a consistent decrease in the average time of about 0.5ms. But when running "very_easy", "easy" and "medium" difficulties at once, the compute time was even faster still, with an average decrease of about 0.75ms.

I assume this is because the scheduler simply allocates more time to completing the task instead of

<br />

# <a name="references"></a>References
1 million sudoku dataset: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download

Ascii art to clearly show sections of code: https://patorjk.com/software/taag/#p=display&f=Big

Unsolveable #28, the "hardest sudoku ever created", according to [Sudoku Wiki](https://www.sudokuwiki.org/Arto_Inkala_Sudoku) (found when looking for more sudokus like Arto Inkala's): https://www.sudokuwiki.org/Weekly_Sudoku.asp?puz=28