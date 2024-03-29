import numpy as np
from test_scripts.tests import test_sudoku
from test_scripts.utils import print_sudoku
from copy import deepcopy

def all_zeros_test(use_process_time: bool) -> None:
    '''
    Tests the sudoku solver against a sudoku with no elements.
    @args:
        use_process_time (bool) : Whether or not to use time.process_time() instead of time.perf_counter()
    '''
    sudoku = np.full((9, 9), fill_value=0)
    sudoku_copy = deepcopy(sudoku)

    solution, time_taken = test_sudoku(sudoku, use_process_time)

    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print_sudoku(sudoku_copy)

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print_sudoku(solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #
""")


def already_solved_test(use_process_time: bool) -> None:
    '''
    Tests the sudoku solver against a sudoku that has already been solved.

    @args:
        use_process_time (bool) : Whether or not to use time.process_time() instead of time.perf_counter()
    '''

    sudoku = np.array([
        [5, 8, 2,    6, 4, 3,    9, 1, 7,],
        [3, 1, 9,    8, 7, 5,    4, 6, 2,],
        [6, 7, 4,    9, 2, 1,    3, 8, 5,],

        [1, 6, 5,    2, 3, 4,    8, 7, 9,],
        [8, 2, 3,    7, 9, 6,    5, 4, 1,],
        [4, 9, 7,    1, 5, 8,    6, 2, 3,],

        [7, 3, 6,    5, 8, 2,    1, 9, 4,],
        [2, 5, 1,    4, 6, 9,    7, 3, 8,],
        [9, 4, 8,    3, 1, 7,    2, 5, 6,]
    ])
    sudoku_copy = deepcopy(sudoku)

    solution, time_taken = test_sudoku(sudoku, use_process_time)

    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print_sudoku(sudoku_copy)

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print_sudoku(solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #
""")

    passed = u'\033[32m \u2713' if np.array_equal(sudoku_copy, solution) else u'\033[31m \u2717'
    print(f"Test passed: {passed}")
