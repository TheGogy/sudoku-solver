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
    for row_num, row in enumerate(sudoku):
        print("|", end=" ")
        for col_num, cell in enumerate(row):
            item = str(cell).replace('-1', 'x').replace('0', ' ')
            print(item, end=" ")
            if (col_num + 1) % 3 == 0:
                print("|", end=" ")
        if (row_num + 1) % 3 == 0:
            print(sep, end=" ")
        print()