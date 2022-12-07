import numpy as np

def load_array(filename: str) -> np.ndarray:
    try:
        loaded_file = np.load(filename) if filename.endswith(".npy") else np.loadtxt(filename)
    except FileNotFoundError:
        print(f'Error: File "{filename}" not found.')
        sys.exit(2)

    return loaded_file
