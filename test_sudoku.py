import sys, getopt
from test_scripts import *

help = '''
Usage:
    test_sudoku.py [ -q , -p , -o , -h|-n|-m|-f ] <batches | filename>

Tests sudoku solver with various puzzles.

Options:
    -h, --help                  Show help.

    -n, --normal                Run test as normal.

    -m, --multiple              Run <batches> tests of normal test.

    -f, --file                  Solve a sudoku stored in a file
                                [*.txt, *.npy]

    -o, --output-to-file        Output the solutions to a .npy file
                                (use with -f)

    -p, --use-perf-counter-ns   Use time.perf_counter_ns() instead of
                                time.process_time()

    -q, --quit-after            Stop solving sudokus after it has solved a certain
                                number. Used with "-f" on .npy and .csv files.

'''

#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|

def main(argv) -> None:
    output_file=''
    use_perf_counter = False
    quit_after = -1

    try:
        opts, args = getopt.getopt(argv,"q:pohnm:f:", ["use-perf-counter-ns", "output-to-file", "help", "normal", "multiple=", "file=", "quit-after="])
    except getopt.GetoptError as e:
        print("Error: " + e.msg)
        sys.exit(2)
    for opt, arg in opts:
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

        if opt in ["-o", "--output-to-file"]:
            output_file = arg

        if opt in ["-p", "--perf-counter-ns"]:
            use_perf_counter = True

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
            basic_tests(use_perf_counter)
            sys.exit(0)

        elif opt in ("-m", "--multiple"):
            try:
                multiple_batches_test(int(arg), use_perf_counter)
                sys.exit(0)

            except ValueError:
                print("Error: Option -m requires integer")
                sys.exit(2)

        elif opt in ("-f", "--file"):
            if arg.endswith(".txt"):
                solve_single(load_txt_file(arg), output_file, use_perf_counter)
                sys.exit(0)

            elif arg.endswith(".npy") or arg.endswith(".csv"):
                sudoku_array = load_array(filename=arg)
                dimensions = sudoku_array.ndim
                if dimensions == 2:
                    solve_single(
                        sudoku=sudoku_array,
                        output_file=output_file,
                        use_perf_counter=use_perf_counter)
                elif dimensions == 3:
                    solve_multiple(sudoku_array, output_file, use_perf_counter, quit_after)
                sys.exit(0)

            else:
                print("Error: File type not supported. (please use .npy / .txt / .csv)")

                sys.exit(0)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    print(help)
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])