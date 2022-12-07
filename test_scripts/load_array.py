import numpy as np
import sys

def load_array(filename: str) -> np.ndarray:
    try:
        loaded_file = np.load(filename) if filename.endswith(".npy") else np.loadtxt(filename)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(2)
    except ValueError:
        print(f"Error: {filename} is of incorrect format.")
        sys.exit(2)

    # Account for 3D arrays containing multiple sudokus
    if loaded_file.shape == (9,9) or loaded_file[0].shape == (9,9):
        return loaded_file

    else:
        print(f"Error: {filename} is of incorrect format.")
        sys.exit(2)

