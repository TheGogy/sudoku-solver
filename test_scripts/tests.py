from numpy import ndarray
from time import process_time, perf_counter
from sudoku import sudoku_solver


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