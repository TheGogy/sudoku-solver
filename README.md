# <a name="intro"></a>Sudoku Solver using Exact Cover
This is my solution to the problem proposed by CW1 of the AI module. It is an agent that, on my - relatively modern as of 2022 - laptop, can solve a hard sudoku in an average of about 7 milliseconds and an easy sudoku in about 3 milliseconds. I have chosen to use Donald Knuth's Algorithm X for this, as the removal of rows and columns from matrix A is an efficient method for constraint propagation.


## <a name="links"></a>Links
- [Intro](#intro)
- [Usage](#usage)
- [Exact Cover](#exact_cover)
- [My implementation](#my_implementation)
- [Edge Cases](#edge_cases)
- [Future Improvement](#future_improvement)
- [Solving the "hardest sudoku ever"](#hardest_sudoku)
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

# <a name="references"></a>References
1 million sudoku dataset: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download

Ascii art to clearly show sections of code: https://patorjk.com/software/taag/#p=display&f=Big

Unsolveable #28, the "hardest sudoku ever created", according to https://www.sudokuwiki.org/Arto_Inkala_Sudoku (found when looking for more sudokus like Arto Inkala's): https://www.sudokuwiki.org/Weekly_Sudoku.asp?puz=28