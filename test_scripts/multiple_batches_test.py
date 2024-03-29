import numpy as np
from time import process_time, perf_counter
from test_scripts.utils import print_sudoku
from test_scripts.tests import test_sudoku

def multiple_batches(num_of_batches: int, use_process_time: bool) -> None:
    '''
    Runs the basic test <num_of_batches> times.
    Calculates fastest batch, slowest batch, fastest single puzzle solve, etc.
    Prints out results.

    @args num_of_batches (int) : The number of batches to test
    '''
    script_start_time = process_time()
    total_time = 0
    count = 0
    fastest_batch_time = 10000
    slowest_batch_time = 0
    fastest_time  = 10000
    slowest_time  = 0
    try:
        for i in range(num_of_batches):
            print(f"RUNNING BATCH    {i}/{num_of_batches}", end="\r")

            difficulties = ['very_easy', 'easy', 'medium', 'hard']
            batch_time = 0
            fastest_time_from_batch = 10000
            slowest_time_from_batch = 0
            for difficulty in difficulties:
                sudokus = np.load(f"data/{difficulty}_puzzle.npy")
                for i in range(len(sudokus)):
                    sudoku = sudokus[i].copy()

                    your_solution, time_taken = test_sudoku(sudoku, use_process_time)

                    batch_time += time_taken

                    if time_taken < fastest_time_from_batch:
                        fastest_time_from_batch = time_taken

                    if time_taken > slowest_time_from_batch:
                        slowest_time_from_batch = time_taken

                    count += 1

            total_time += batch_time
            # - - - - - - - - - - - - - - - - - - - #
            if batch_time < fastest_batch_time:
                fastest_batch_time = batch_time

            if batch_time > slowest_batch_time:
                slowest_batch_time = batch_time

            # - - - - - - - - - - - - - - - - - - - #
            if batch_time < fastest_time:
                fastest_time = fastest_time_from_batch

            if batch_time > slowest_time:
                slowest_time = slowest_time_from_batch

    except KeyboardInterrupt: pass

    average_batch_time = total_time / (count/60)
    average_single_time = total_time / (count)
    script_end_time = process_time()

    print(f'''
# - - - - - - - - - - - - - - - - - - - - - - - - - #

    Solved {count} sudokus in {round(script_end_time - script_start_time, 3)} seconds.

    TOTAL SOLVING TIME      {total_time / 1000} s

    FASTEST BATCH TIME      {fastest_batch_time} ms
    SLOWEST BATCH TIME      {slowest_batch_time} ms
    AVERAGE BATCH TIME      {average_batch_time} ms

    FASTEST SINGLE TIME     {fastest_time} ms
    SLOWEST SINGLE TIME     {slowest_time} ms
    AVERAGE SINGLE TIME     {average_single_time} ms

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - - - #
          ''')