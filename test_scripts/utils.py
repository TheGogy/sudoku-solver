from numpy import ndarray

def print_sudoku(sudoku: ndarray) -> str:
    '''
    Displays a sudoku in a more easily way.

    @args:
        sudoku (ndarray) : The sudoku to print

    @returns:
        sudoku_str (string) : The easily readable sudoku
    '''
    sep = '\n+-------+-------+-------+'

    print(sep)
    # Iterate through rows
    for row_num, row in enumerate(sudoku):
        print("|", end=" ")

        # Iterate through cols
        for col_num, cell in enumerate(row):

            # Make sure each value is easier to read
            item = str(cell).replace('-1', 'x').replace('0', ' ')

            print(item, end=" ")

            if (col_num + 1) % 3 == 0:
                # reached edge of box
                print("|", end=" ")

        # Print separator after finished printing all cols
        if (row_num + 1) % 3 == 0:
            print(sep, end=" ")

        # go to new line
        print()