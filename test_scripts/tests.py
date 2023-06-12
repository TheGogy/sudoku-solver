from numpy import ndarray, full
from time import process_time, perf_counter
from copy import deepcopy

from signal import signal, alarm, SIGALRM

from sudoku import sudoku_solver
from test_scripts.utils import *

TIMEOUT_THRESHOLD = 20

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    print(u'\033[41m \033[01m \033[30mSolver timed out \033[0m')
    raise TimeoutException

def test_sudoku(sudoku: ndarray, use_process_time: bool):

    signal(SIGALRM, timeout_handler)
    alarm(TIMEOUT_THRESHOLD)
    if use_process_time:
        timer = process_time
    else:
        timer = perf_counter

    try:
        start_time = timer()
        your_solution = sudoku_solver(sudoku)
        end_time = timer()


    except TimeoutException:
        return full((9,9), fill_value=0), TIMEOUT_THRESHOLD * 1000
    # - - - - - - - - - - - - - - - - - - - #

    return your_solution, (end_time-start_time) * 1000

def test_sudoku_verbose(sudoku: ndarray, save_to_file: str or None, use_process_time: bool):
    sudoku_copy = deepcopy(sudoku)

    signal(SIGALRM, timeout_handler)
    alarm(TIMEOUT_THRESHOLD)

    try:
        solution, time_taken = test_sudoku(sudoku, use_process_time)

    except TimeoutException:
        solution = full((9,9), fill_value=0)
        time_taken = TIMEOUT_THRESHOLD

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


