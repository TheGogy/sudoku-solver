import numpy as np
import sys

def load_array(filename: str) -> np.ndarray:
    try:
        loaded_file = np.load(filename) if filename.endswith(".npy") else np.loadtxt(filename)
    except FileNotFoundError:
        sys.exit(f"Error: {filename} not found.")
    except ValueError:
        sys.exit(f"Error: {filename} is of incorrect format.")

    # Account for 3D arrays containing multiple sudokus
    if loaded_file.shape == (9,9) or loaded_file[0].shape == (9,9):
        return loaded_file

    else:
        sys.exit(f"Error: {filename} is of incorrect format.")

