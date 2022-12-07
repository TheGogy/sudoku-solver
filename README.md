# <a name="intro"></a>Sudoku Solver using Exact Cover
This is my solution to the problem proposed by CW1 of the AI module. It is an agent that, on my - relatively modern as of 2022 - laptop, can solve a "hard" sudoku in an average of 3.85 milliseconds and a "very easy" sudoku in an average of 1.28 milliseconds. I have chosen to use Donald Knuth's Algorithm X for this, as the removal of rows and columns from matrix A is an efficient method for constraint propagation.


## <a name="links"></a>Links
- [Intro](#intro)
- [Usage](#usage)
- [Exact Cover](#exact_cover)
- [My implementation](#my_implementation)
- [Edge Cases](#edge_cases)
- [Future Improvement](#future_improvement)
- [Solving the "hardest sudoku ever"](#hardest_sudoku)
- [My observations](#observations)
- [References](#references)

# <a name="usage"></a>How to use the solver
To use the solver, pass a `numpy.ndarray((9x9)<sudoku>)` to `sudoku.py`. The test script included contains examples of how to do this and examples of input are stored in numpy arrays in `/data`.

```py
import numpy as np
from sudoku import sudoku_solver

initial_state = np.ndarray((9,9), <your sudoku here>)
solution = sudoku_solver(initial_state)

...
```
# <a name="usage"></a>Exact Cover

# <a name="observations"></a>My Observations

While running some tests on the solver, I noticed some rather weird behaviour, which I will do my best to document here.

## <a name="observations_1_v_easy_not_easiest"></a>The solver reduces average time significantly by solving more puzzles
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


# <a name="references"></a>References
1 million sudoku dataset: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download

Ascii art to clearly show sections of code: https://patorjk.com/software/taag/#p=display&f=Big

Unsolveable #28, the "hardest sudoku ever created", according to [Sudoku Wiki](https://www.sudokuwiki.org/Arto_Inkala_Sudoku) (found when looking for more sudokus like Arto Inkala's): https://www.sudokuwiki.org/Weekly_Sudoku.asp?puz=28