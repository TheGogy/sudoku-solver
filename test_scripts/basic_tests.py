import numpy as np
from time import process_time, perf_counter
from sudoku import sudoku_solver
import cProfile, pstats


def basic_tests(use_process_time: bool) -> None:
    '''
    Basic test function (was already provided).
    Tests against each set of puzzles stored in /data/
    and compares answers against the solutions (also stored in /data/).
    '''

    difficulties = ['very_easy', 'easy', 'medium', 'hard']
#    difficulties = ['very_easy', 'easy', 'medium', 'hard']

    total_time = 0
    total_correct = 0
    hardest_time = 0
    difficulty_total_time_list = []
    total_time_list = []

    script_start_time = perf_counter()
    for difficulty in difficulties:
        difficulty_total_time = 0
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
            if use_process_time:
                start_time = process_time()
                your_solution = sudoku_solver(sudoku)
                end_time = process_time()
            else:
                start_time = perf_counter()
                your_solution = sudoku_solver(sudoku)
                end_time = perf_counter()
            # - - - - - - - - - - - - - - - - - - - #

            # profiler.disable()
            # stats = pstats.Stats(profiler)
            # stats.print_stats()
            # input()

            time_taken = end_time - start_time
            total_time += time_taken
            difficulty_total_time += time_taken
            total_time_tuple = (f'{difficulty} {i}', time_taken * 1000)
            total_time_list.append(total_time_tuple)

            if time_taken > hardest_time:
                hardest_time = time_taken
                hardest_sudoku = sudokus[i]
                hardest_number = (difficulty, i)
                hardest_solution = your_solution

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

            print("This sudoku took", str(time_taken * 1000), "ms to solve.\n")


        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break

        difficulty_total_time_tuple = (difficulty, difficulty_total_time * 1000)
        difficulty_total_time_list.append(difficulty_total_time_tuple)

    difficulty_total_time_list.sort(key=lambda x: x[1])
    total_time_list.sort(key=lambda y: y[1])

    tpd_printable = ''
    for i in difficulty_total_time_list:
        tpd_printable += '{:15s} - {:2.5f}\n'.format(i[0], round(i[1], 5))

    tpd_printable += '\n- - - - - - - - -\n\n'

    for i in total_time_list:
        tpd_printable += '{:15s} - {:2.5f}\n'.format(i[0], round(i[1], 5))


    script_end_time = perf_counter()

    print(f'''
# - - - - - - - - [ Hardest Sudoku ] - - - - - - - - #
THIS IS "{hardest_number[0]}" SUDOKU NUMBER {hardest_number[1]}
{hardest_sudoku}
# - - - - - - - - - - [ solution ] - - - - - - - - - #
{hardest_solution}
TIME TAKEN               {hardest_time * 1000}ms
# - - - - - - - - - - [ Times per difficulty ] - - - - - - - - - #
{tpd_printable}
# - - - - - - - - - - - - - - - - - - - - - - - - - #

    Solved {total_correct} sudokus in {round(script_end_time - script_start_time, 3)} seconds.


    TOTAL SOLVING TIME       {total_time} s
    AVERAGE TIME             {total_time * 1000 / (len(difficulties) * 15)} ms
    TOTAL CORRECT            {total_correct}/{len(difficulties) * 15}

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - - - #
          ''')