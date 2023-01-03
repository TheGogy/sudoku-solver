import numpy as np
from time import perf_counter

from test_scripts.utils import print_sudoku
from test_scripts.tests import test_sudoku


def basic_tests(use_process_time: bool) -> None:
    '''
    Basic test function (provided by University of Bath).
    Tests against each set of puzzles stored in /data/
    and compares answers against the solutions (also stored in /data/).

    @args:
        use_process_time (bool) : Whether or not to use time.process_time() instead of time.perf_counter()
    '''

    difficulties = ['very_easy', 'easy', 'medium', 'hard']
#                  ['very_easy', 'easy', 'medium', 'hard']

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
            print_sudoku(sudoku)

            your_solution, time_taken = test_sudoku(sudoku, use_process_time)

            difficulty_total_time += time_taken
            total_time_tuple = (f'{difficulty} {i}', time_taken)
            total_time_list.append(total_time_tuple)

            if time_taken > hardest_time:
                hardest_time = time_taken
                hardest_sudoku = sudokus[i]
                hardest_number = (difficulty, i)
                hardest_solution = your_solution

            print(f"This is your solution for {difficulty} sudoku number", i)
            print_sudoku(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
                total_correct += 1
            else:
                print("No, the correct solution is:")
                print_sudoku(solutions[i])
                exit(f"Failed {difficulty} sudoku number {i} ")

            print("This sudoku took", str(time_taken), "ms to solve.\n")
            print('- '*30, end='\n\n')


        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")

        difficulty_total_time_tuple = (difficulty, difficulty_total_time)
        difficulty_total_time_list.append(difficulty_total_time_tuple)

        total_time += difficulty_total_time

    difficulty_total_time_list.sort(key=lambda x: x[1])
    total_time_list.sort(key=lambda y: y[1])

    tpd_printable = ''
    for i in difficulty_total_time_list:
        tpd_printable += '{:15s} - {:2.5f}  (avg: {:2.5f})\n'.format(i[0], round(i[1], 5), round(i[1] / 15, 5))

    tpd_printable += '\n- - - - - - - - -\n\n'

    for i in total_time_list:
        tpd_printable += '{:15s} - {:2.5f}\n'.format(i[0], round(i[1], 5))


    script_end_time = perf_counter()

    print(f'''
# - - - - - - - - [ Hardest Sudoku ] - - - - - - - - #
THIS IS "{hardest_number[0]}" SUDOKU NUMBER {hardest_number[1]}''')
    print_sudoku(hardest_sudoku)
    print(f'''
# - - - - - - - - - - [ solution ] - - - - - - - - - #''')
    print_sudoku(hardest_solution)
    print(f'''
TIME TAKEN               {hardest_time}ms
# - - - - - - - - - - [ Times per difficulty ] - - - - - - - - - #
{tpd_printable}
# - - - - - - - - - - - - - - - - - - - - - - - - - #

    Solved {total_correct} sudokus in {round(script_end_time - script_start_time, 3)} seconds.


    TOTAL SOLVING TIME       {total_time} ms
    AVERAGE TIME             {total_time / (len(difficulties) * 15)} ms
    TOTAL CORRECT            {total_correct}/{len(difficulties) * 15}

    Calculated using time.{"process_time" if use_process_time else "perf_counter"}()

# - - - - - - - - - - - - - - - - - - - - - - - - - #
''')