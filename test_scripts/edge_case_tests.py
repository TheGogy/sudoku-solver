import numpy as np
from test_scripts.utils import print_sudoku
from test_scripts.tests import test_sudoku

def all_zeros_test(use_process_time: bool) -> None:
    sudoku = np.full((9, 9), fill_value=0)
    solve_test(sudoku, use_process_time)


def already_solved_test(use_process_time: bool) -> None:
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
    solve_test(sudoku, use_process_time)


def solve_test(sudoku: np.ndarray, use_process_time: bool) -> None:

    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print_sudoku(sudoku)

    your_solution, time_taken = test_sudoku(sudoku, use_process_time)

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print_sudoku(your_solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #
          """)

