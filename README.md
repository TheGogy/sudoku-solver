# <a name="title"></a>**Sudoku Solver using Exact Satisfactability and Algorithm X**

- [Usage](#usage)
- [Test package](/test_scripts/README.md/#title)

For more information on how to use this solver, please refer to [my blog post](https://gogy.dev/projects/sudoku-solver).

# <a name="usage"></a>How to use the solver

## <a name="usage_solver"></a>Solver - `sudoku.py`
To use the solver, pass a `numpy.ndarray((9x9)<sudoku>)` to [`sudoku.py`](/sudoku.py). The test script included ([`test_sudoku.py`](/test_sudoku.py)) contains examples of how to do this and examples of input are stored in numpy arrays in [`/data/`](/data/).

```py
import numpy as np
from sudoku import sudoku_solver

initial_state = np.ndarray((9,9), <your sudoku here>)
solution = sudoku_solver(initial_state)

...
```

The solver will return the solved sudoku in the form  `numpy.ndarray((9x9)<solution)`. If the sudoku has multiple possible solutions, the solver will return the first one it finds.

## <a name="usage_test_script"></a>Test script - [`test_sudoku.py`](/test_sudoku.py)
I have included a test script [`test_sudoku.py`](/test_sudoku.py), that implements the test package [`test_scripts.py`](/test_scripts/) (see below) with the sudoku solver.

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


