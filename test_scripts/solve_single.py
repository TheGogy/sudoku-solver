import numpy as np
from time import process_time, perf_counter_ns
from sudoku import sudoku_solver

def solve_single(sudoku: np.ndarray,
                 save_to_file: str,
                 use_perf_counter: bool) -> np.ndarray or None:
    '''
    Passes a sudoku into the sudoku solver and prints information about it

    @args sudoku (np.ndarray) : The sudoku to pass to solver
    '''

    print(" - - - - - - - - [ Input Sudoku ] - - - - - - - - ")
    print(sudoku)

    # - - - - - - - - - - - - - - - - - - - #
    # This code is written like this because if it was cleaner it has an impact on performance
    if use_perf_counter:
        start_time = perf_counter_ns() * 1000
        solution = sudoku_solver(sudoku)
        end_time = perf_counter_ns() * 1000
        time_taken = (end_time-start_time) / 1000000000
    else:
        start_time = process_time() * 1000
        solution = sudoku_solver(sudoku)
        end_time = process_time() * 1000
        time_taken = end_time - start_time

    # - - - - - - - - - - - - - - - - - - - #

    print(" - - - - - - - - [ Solved sudoku ] - - - - - - - - ")
    print(solution)

    print(f"""
# - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME                {time_taken} ms

    Calculated using time.{"perf_counter" if use_perf_counter else "process_time"}()

# - - - - - - - - - - - - - - - - - - - - - - - #

          """)

    if save_to_file:
        save_file_name = f"{save_to_file}_solutions.npy"
        np.save(save_file_name, solutions)
        print(f"Saved to file: {save_file_name}")
