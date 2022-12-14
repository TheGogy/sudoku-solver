import numpy as np
from time import process_time, perf_counter
from test_scripts.utils import print_sudoku
from test_scripts.tests import test_sudoku

def solve_single(sudoku: np.ndarray,
                 save_to_file : str or None,
                 use_process_time: bool) -> np.ndarray or None:
    '''
    Passes a sudoku into the sudoku solver and prints information about it.

    @args
        sudoku (np.ndarray) : The sudoku to pass to solver
        save_to_file (str or None) : The filename to save to (or None to not save it)
        use_process_time (bool) : Whether to use time.process_time() instead of perf_counter()

    '''
    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print_sudoku(sudoku)

    your_solution, time_taken =test_sudoku(sudoku, use_process_time)

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print_sudoku(your_solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #
          """)

    if save_to_file:
        save_file_name = f"{save_to_file}_solutions.npy"
        np.save(save_file_name, sudoku)
        print(f"Saved to file: {save_file_name}")
