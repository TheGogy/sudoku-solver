import numpy as np
import sys

def load_txt_file(filename: str) -> np.ndarray:
    '''
    Loads a sudoku from a .txt file.

    @args file (String) : The path to the file to load from
    @returns loaded_file (np.ndarray) : a NumPy array of the sudoku
    '''
    try:
        # Load file as int8 so it can be printed more easily
        loaded_file =  np.loadtxt(filename, dtype=np.int8)

        # Check if input file is incorrect shape
        if not (loaded_file.shape == (9, 9)):
            print("Error: Input sudoku must be a 9x9 grid.")
            sys.exit(2)
        else:
            return loaded_file

    except FileNotFoundError:
        print(f'Error: File "{filename}" not found.')
        sys.exit(2)
    except ValueError:
        print(f"Error: {filename} is of incorrect format.")
        sys.exit(2)