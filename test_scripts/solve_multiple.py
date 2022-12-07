import numpy as np
from time import process_time, perf_counter_ns
from sudoku import sudoku_solver

def solve_multiple(sudoku_array: np.ndarray,
                   save_to_file: bool,
                   use_perf_counter: bool,
                   quit_after: int) -> np.ndarray or None:
    '''
    Solves multiple sudokus and prints the results.

    @args sudoku_array (np.ndarray) : A 3D array of the sudokus to solve
    '''
    total_time = 0
    count = 0
    total_count = len(sudoku_array) if quit_after == -1 else quit_after
    fastest = 10000
    slowest = 0
    solutions = np.ndarray
    try:
        for sudoku in sudoku_array:
            print(f"SOLVING SUDOKU    {count}/{total_count}", end="\r")
            count += 1
            if count == quit_after: break
            # - - - - - - - - - - - - - - - - - - - #
            # This code is written like this because if it was cleaner it has an impact on performance
            if use_perf_counter:
                start_time = perf_counter_ns()
                solution = sudoku_solver(sudoku)
                end_time = perf_counter_ns()
                time_taken = (end_time-start_time) / 1000000000
            else:
                start_time = process_time()
                solution = sudoku_solver(sudoku)
                end_time = process_time()
                time_taken = end_time - start_time

            # - - - - - - - - - - - - - - - - - - - #
            total_time += time_taken
            if time_taken < fastest:
                fastest = time_taken
            if time_taken > slowest:
                slowest = time_taken

            if save_to_file:
                solutions = np.append(solutions, solution)

    except KeyboardInterrupt:
        pass
    print( f'''
    # - - - - - - - - - - - - - - - - - - - - - - - #

        TOTAL TIME                {total_time}
        SUDOKUS SOLVED            {count}

        FASTEST TIME              {fastest}
        SLOWEST TIME              {slowest}
        AVERAGE TIME              {total_time / count}

    # - - - - - - - - - - - - - - - - - - - - - - - #
            ''')
    if save_to_file:
        save_file_name = f"{save_to_file}_solutions.npy"
        np.save(save_file_name, solutions)
        print(f"Saved to file: {save_file_name}")