import numpy as np
from time import process_time, perf_counter
from sudoku import sudoku_solver

def multiple_batches_test(num: int, use_perf_counter: bool) -> None:
    '''
    Runs the basic test <num> times.
    Calculates fastest batch, slowest batch, fastest single puzzle solve, etc.
    Prints out results.

    @args num (int) : The number of batches to test
    '''
    script_start_time = process_time()
    total_time = 0
    count = 0
    fastest_batch_time = 10000
    slowest_batch_time = 0
    fastest_time  = 10000
    slowest_time  = 0
    try:
        for i in range(num):
            print(f"RUNNING BATCH    {i}/{num}", end="\r")

            difficulties = ['very_easy', 'easy', 'medium', 'hard']
            batch_time = 0
            fastest_time_from_batch = 10000
            slowest_time_from_batch = 0
            for difficulty in difficulties:
                sudokus = np.load(f"data/{difficulty}_puzzle.npy")
                for i in range(len(sudokus)):
                    sudoku = sudokus[i].copy()
                    # - - - - - - - - - - - - - - - - - - - #
                    # This code is written like this because if
                    # it was cleaner it seems to have an impact on performance
                    if use_perf_counter:
                        start_time = perf_counter()
                        solution = sudoku_solver(sudoku)
                        end_time = perf_counter()
                    else:
                        start_time = process_time()
                        solution = sudoku_solver(sudoku)
                        end_time = process_time()
                    # - - - - - - - - - - - - - - - - - - - #

                    # The code below is a little ugly.
                    # It keeps track of the fastest and slowest
                    # individual solves and batch solves.
                    time_taken = end_time - start_time
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

    TOTAL SOLVING TIME      {total_time}

    FASTEST BATCH TIME      {fastest_batch_time}
    SLOWEST BATCH TIME      {slowest_batch_time}
    AVERAGE BATCH TIME      {average_batch_time}

    FASTEST SINGLE TIME     {fastest_time}
    SLOWEST SINGLE TIME     {slowest_time}
    AVERAGE SINGLE TIME     {average_single_time}

    Calculated using time.{"perf_counter" if use_perf_counter else "process_time"}()

# - - - - - - - - - - - - - - - - - - - - - - - - - #
          ''')