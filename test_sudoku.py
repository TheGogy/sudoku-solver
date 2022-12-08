import sys, getopt
from test_scripts import *

help = '''
Usage:
    test_sudoku.py [ -q , -p , -o , -h|-n|-m|-f|-e ] <batches | filename | edge case>

Tests sudoku solver with various puzzles.

Options:
    -h, --help              Show help.

    -n, --normal            Run test as normal.

    -m, --multiple          Run <batches> tests of normal test.

    -f, --file              Solve a sudoku stored in a file
                            [*.txt, *.npy]

    -o, --output-to-file    Output the solutions to a .npy file
                            (use with -f)

    -p, --use-process-time  Use time.process_time() instead of
                            time.perf_counter()

    -q, --quit-after        Stop solving sudokus after it has solved a certain
                            number. Used with "-f" on .npy and .csv files.

    -e, --edge-case         Run specified edge case [allzero, presolved]

'''

#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|

def main(argv) -> None:
    output_file=''
    use_process_time = False
    quit_after = -1
    commands_verbose_list = ["use-perf-counter-ns", "output-to-file",
                             "help", "normal", "multiple=", "file=",
                             "quit-after=", "edge-case="]

    try:
        opts, args = getopt.getopt(argv,"q:pohnm:f:e:", commands_verbose_list)
    except getopt.GetoptError as e:
        print("Error: " + e.msg)
        sys.exit(2)


    for opt, arg in opts:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

        if opt in ["-o", "--output-to-file"]:
            output_file = arg

        if opt in ["-p", "--perf-counter-ns"]:
            use_process_time = True

        if opt in ["-q", "--quit-after"]:
            try:
                quit_after = int(arg)
            except ValueError:
                print("Error: Option -q requires integer")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


        if opt in ["-h", "--help"]:
            print(help)
            sys.exit(0)

        elif opt in ("-n", "--normal"):
            basic_tests(use_process_time)
            sys.exit(0)

        elif opt in ("-m", "--multiple"):
            try:
                multiple_batches(int(arg), use_process_time)
                sys.exit(0)

            except ValueError:
                print("Error: Option -m requires integer")
                sys.exit(2)

        elif opt in ("-f", "--file"):
            if arg.endswith(".txt"):
                solve_single(load_txt_file(arg), output_file, use_process_time)
                sys.exit(0)

            elif arg.endswith(".npy") or arg.endswith(".csv"):
                sudoku_array = load_array(filename=arg)
                dimensions = sudoku_array.ndim
                if dimensions == 2:
                    solve_single(
                        sudoku=sudoku_array,
                        output_file=output_file,
                        use_process_time=use_process_time)
                elif dimensions == 3:
                    solve_multiple(sudoku_array, output_file, use_process_time, quit_after)
                sys.exit(0)

            else:
                print("Error: File type not supported. (please use .npy / .txt / .csv)")

                sys.exit(0)

        elif opt in ("-e", "--edge-case"):
            if arg == "allzero":
                all_zeros_test(use_process_time)
                sys.exit(0)

            elif arg == "presolved":
                already_solved_test(use_process_time)
                sys.exit(0)
            else:
                print(f'Error: Unknown edge case "{arg}". Known edge cases: allzero, presolved')
                sys.exit(2)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    print(help)
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])