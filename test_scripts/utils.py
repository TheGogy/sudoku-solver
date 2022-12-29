from numpy import (
    ndarray,
    save
)

def print_sudoku(sudoku: ndarray) -> str:
    '''
    Displays a sudoku in an easy to read format.

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


def save_sudoku(sudoku: ndarray, filename: str):
    '''
    Saves a sudoku or array of sudokus to a file.

    @args:
        sudoku (ndarray): The sudoku (or array of sudokus) to save
    '''
    try:
        save_file_name = f"{filename}_solutions.npy"
        np.save(save_file_name, solutions)
        print(f"Saved to file: {save_file_name}")

    except FileExistsError:
        print(f"Could not save: file {save_file_name} already exists.")
