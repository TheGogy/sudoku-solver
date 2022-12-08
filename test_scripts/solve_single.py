import numpy as np
from time import process_time, perf_counter
from sudoku import sudoku_solver

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
    print(sudoku)

    # - - - - - - - - - - - - - - - - - - - #
    # This code is written like this because if it was cleaner it has an impact on performance
    if use_process_time:
        start_time = process_time()
        sudoku_solver(sudoku)
        end_time = process_time()
    else:
        start_time = perf_counter()
        sudoku_solver(sudoku)
        end_time = perf_counter()
    # - - - - - - - - - - - - - - - - - - - #
    time_taken = (end_time - start_time) * 1000

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print(sudoku)

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
