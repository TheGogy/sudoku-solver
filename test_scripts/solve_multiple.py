import numpy as np
from time import process_time, perf_counter
from test_scripts.tests import test_sudoku

def solve_multiple(sudoku_array: np.ndarray,
                   save_to_file: str or None,
                   use_process_time: bool,
                   quit_after: int) -> np.ndarray or None:
    '''
    Solves multiple sudokus and prints the results.

    @args
        sudoku_array (np.ndarray) : A 3D array of the sudokus to solve
        save_to_file (bool) : Whether or not to save the variables
                                (Can increase processing time)

        use_process_time (bool) : Whether or not to use time.process_time()
                                  instead of time.perf_counter()

        quit_after (int) : The number of sudokus to stop processing after.
    '''
    total_time = 0
    count = 0
    total_count = len(sudoku_array) if quit_after == -1 else quit_after
    fastest = 10000
    slowest = 0
    solutions = np.ndarray
    script_start_time = perf_counter()
    try:
        for sudoku in sudoku_array:
            print(f"SOLVING SUDOKU    {count}/{total_count}", end="\r")
            count += 1
            if count == quit_after: break

            your_solution, time_taken = test_sudoku(sudoku, use_process_time)

            total_time += time_taken
            if time_taken < fastest:
                fastest = time_taken
            if time_taken > slowest:
                slowest = time_taken

            if save_to_file:
                solutions = np.append(solutions, solution)

    except KeyboardInterrupt:
        pass
    script_end_time = perf_counter()
    print( f'''
# - - - - - - - - - - - - - - - - - - - - - - - #

    Solved {count} sudokus in {round(script_end_time - script_start_time, 3)} seconds.

    TOTAL TIME                {total_time / 1000} s
    SUDOKUS SOLVED            {count}

    FASTEST TIME              {fastest} ms
    SLOWEST TIME              {slowest} ms
    AVERAGE TIME              {total_time / count} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - #
            ''')
    if save_to_file:
        save_file_name = f"{save_to_file}_solutions.npy"
        np.save(save_file_name, solutions)
        print(f"Saved to file: {save_file_name}")