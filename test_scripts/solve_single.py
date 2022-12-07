import numpy as np
from time import process_time, perf_counter
from sudoku import sudoku_solver

def solve_single(sudoku: np.ndarray,
                 save_to_file : str or None,
                 use_process_time: bool) -> np.ndarray or None:
    '''
    Passes a sudoku into the sudoku solver and prints information about it

    @args sudoku (np.ndarray) : The sudoku to pass to solver
    '''

    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print(sudoku)

    # - - - - - - - - - - - - - - - - - - - #
    # This code is written like this because if it was cleaner it has an impact on performance
    if use_process_time:
        start_time = process_time() * 1000
        solution = sudoku_solver(sudoku)
        end_time = process_time() * 1000
    else:
        start_time = perf_counter() * 1000
        solution = sudoku_solver(sudoku)
        end_time = perf_counter() * 1000
    # - - - - - - - - - - - - - - - - - - - #
    time_taken = end_time - start_time

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print(solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #

          """)

    if save_to_file:
        save_file_name = f"{save_to_file}_solutions.npy"
        np.save(save_file_name, solutions)
        print(f"Saved to file: {save_file_name}")
