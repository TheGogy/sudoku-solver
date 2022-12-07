import numpy as np
from time import process_time, perf_counter_ns
from sudoku import sudoku_solver

def basic_tests(use_perf_counter: bool) -> None:
    '''
    Basic test function (was already provided).
    Tests against each set of puzzles stored in /data/
    and compares answers against the solutions (also stored in /data/).
    '''

    difficulties = ['very_easy', 'easy', 'medium', 'hard']
#    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    total_time = 0
    total_correct = 0

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")
        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            # profiler = cProfile.Profile()
            # profiler.enable()

            # - - - - - - - - - - - - - - - - - - - #
            # This code is written like this because if it was cleaner it has an impact on performance
            if use_perf_counter:
                start_time = perf_counter_ns()
                your_solution = sudoku_solver(sudoku)
                end_time = perf_counter_ns()
                time_taken = (end_time-start_time) / 1000000000
            else:
                start_time = process_time()
                your_solution = sudoku_solver(sudoku)
                end_time = process_time()
                time_taken = end_time - start_time
            # - - - - - - - - - - - - - - - - - - - #

            # profiler.disable()
            # stats = pstats.Stats(profiler)
            # stats.print_stats()

            total_time += time_taken

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
                total_correct += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])

            print("This sudoku took", time_taken, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break
    print(f'''
# - - - - - - - - - - - - - - - - - - - - - - - - - #

    TOTAL TIME        {total_time}
    AVERAGE TIME      {total_time / (len(difficulties) * 15)}
    TOTAL CORRECT     {total_correct}/{len(difficulties) * 15}

# - - - - - - - - - - - - - - - - - - - - - - - - - #
          ''')