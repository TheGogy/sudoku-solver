from numpy import ndarray
from time import process_time, perf_counter
from copy import deepcopy

from sudoku import sudoku_solver
from test_scripts.utils import *



def test_sudoku(sudoku: ndarray, use_process_time: bool):
    # - - - - - - - - - - - - - - - - - - - #
    # This code is written like this because if it was cleaner it has an impact on performance
    if use_process_time:
        start_time = process_time()
        your_solution = sudoku_solver(sudoku)
        end_time = process_time()
    else:
        start_time = perf_counter()
        your_solution = sudoku_solver(sudoku)
        end_time = perf_counter()
    # - - - - - - - - - - - - - - - - - - - #

    return your_solution, (end_time-start_time) * 1000

def test_sudoku_verbose(sudoku: ndarray, save_to_file: str or None, use_process_time: bool):
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
    if save_to_file:
        save_sudoku(your_solution, save_to_file)


