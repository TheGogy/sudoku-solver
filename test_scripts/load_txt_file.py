import numpy as np
import sys

def load_txt_file(file) -> np.ndarray:
    '''
    Loads a sudoku from a .txt file.

    @args file (String) : The path to the file to load from
    @returns loaded_file (np.ndarray) : a NumPy array of the sudoku
    '''
    try:
        loaded_file =  np.loadtxt(file)
        if not (loaded_file.shape == (9, 9)):
            print("Error: Input sudoku must be a 9x9 grid.")
            sys.exit(2)
        else:
            return loaded_file

    except FileNotFoundError:
        print(f'Error: File "{file}" not found.')
        sys.exit(2)
    except ValueError:
        print("Error: Input sudoku must be a 9x9 grid.")
        sys.exit(2)