from itertools import product
from sys import intern
from functools import reduce
from numpy import (
    count_nonzero,
    ndarray,
    ndenumerate,
    full,
    arange,
    where,
    setdiff1d,
    union1d,
    copy as npcopy
)

#   _____                           _
#  |  __ \                         | |
#  | |  | | ___  ___ ___  _ __ __ _| |_ ___  _ __ ___
#  | |  | |/ _ \/ __/ _ \| '__/ _` | __/ _ \| '__/ __|
#  | |__| |  __/ (_| (_) | | | (_| | || (_) | |  \__ \
#  |_____/ \___|\___\___/|_|  \__,_|\__\___/|_|  |___/


def memoize(func):
    '''
    Caches the result of a function for later use.

    @args:
        func: the function to cache

    @returns:
        wrapper: The wrapper to cache the output of the function
    '''
    # Cache dictionary
    cache = {}

    def wrapper(*args):
        # If values are not cached, add to cache
        if args not in cache:
            cache[args] = func(*args)

        # Return cached values
        return cache[args]
    return wrapper

#                      _        __   __
#                /\   | |       \ \ / /
#    ______     /  \  | | __ _   \ V /   ______
#   |______|   / /\ \ | |/ _` |   > <   |______|
#             / ____ \| | (_| |  / . \
#            /_/    \_\_|\__, | /_/ \_\
#                         __/ |
#                        |___/


def select(matrix_a, constraints, row) -> list:
    '''
    removes associated rows, cols from matrix
    @args:
        matrix_a: the search space matrix
        constraints: the constraints dict
        row: The row to be selected

    @returns:
        cols (list): List of removed columns
    '''
    # Keep removed columns so they can be added back into sudoku
    cols = []

    # For each constraint this row satisfies:
    for i in constraints[row]:

        # For all other constraints that also satisfy i:
        for j in matrix_a[i]:

            # For all other constraints that j satisfies:
            for k in constraints[j]:

                # Remove all other constraints except i
                if k != i:
                    matrix_a[k].remove(j)

        cols.append(matrix_a.pop(i))

    return cols


def deselect(matrix_a, constraints, row, cols) -> None:
    '''
    Restores a branch with a no solutions back into matrix_a

    @args:
        matrix_a: The search space matrix
        constraints: the constraints dict
        cols: Columns to restore into matrix_a
    '''
    for i in reversed(constraints[row]):

        # Get top column from list of removed columns
        matrix_a[i] = cols.pop()

        # For each other value that satisfies constraint:
        for j in matrix_a[i]:

            # For other constraints that value satisfies:
            for k in constraints[j]:

                # Add value back into matrix_a
                matrix_a[k].add(j)


def find_solution(matrix_a, constraints, solution):
    '''
    Recursively attempts to find a solution to a given exact cover problem

    @args:
        matrix_a: The search space matrix
        constraints: the constraints dict
        solution: The state to find (or not find) soltion for

    @returns:
        list: The solution
    '''
    if not matrix_a: yield solution
    else:
        col = choose_col(matrix_a)
        for row in list(matrix_a[col]):
            solution.append(row)
            cols = select(matrix_a, constraints, row)

            # Keep trying to find solution recursively
            for i in find_solution(matrix_a, constraints, solution): yield i

            # This branch does not have a solution, deselect it
            deselect(matrix_a, constraints, row, cols)

            # Remove value from this possible solution
            solution.pop()


def choose_col(matrix_a) -> str:
    """
    Returns col with fewest possible values.
    @args
        matrix_a: the search space matrix
        constraints: The constraints dict

    @returns
        col : the column with the fewest possible values
    """

    best_col_val = 325

    for col in matrix_a:
        cur_col_val = len(matrix_a[col])

        if best_col_val > cur_col_val:

            best_col = col
            best_col_val = cur_col_val

            # Do not waste time if we have already found a column with only
            # one value
            if cur_col_val == 1:
                return best_col

    return best_col


# Cache the constraints dict; this is not updated and can be re-used.

@memoize
def get_constraints() -> dict:
    '''
    Gets the general constraint dict for all sudokus.

    @returns:
        constraints (dict) : Constraints dictionary
    '''
    constraints = {}
    for row, col, cell in product(range(9), range(9), range(1, 10)):
        box = (row // 3) * 3 + (col // 3)
        # Boxes are labelled like this:
        #   0 1 2
        #   3 4 5
        #   6 7 8
        constraints[(row, col, cell)] = [
            # Each cell must have a value
            intern((f"cell ({row}, {col})")),
            # Each row must have each value
            intern((f"row ({row}, {cell})")),
            # Each column must have each value
            intern((f"col ({col}, {cell})")),
            # Each box must have each value
            intern((f"box ({box}, {cell})"))
        ]
    return constraints


@memoize
def get_mat_a():
    return {j: set() for j in(
        [intern((f"cell {i}")) for i in product (range(9), range(9)    )] +
        [intern((f"row {i}" )) for i in product (range(9), range(1, 10))] +
        [intern((f"col {i}" )) for i in product (range(9), range(1, 10))] +
        [intern((f"box {i}" )) for i in product (range(9), range(1, 10))]
    )}


def solve_alg_x(sudoku) -> ndarray or None:
    '''
    Solves the given sudoku using Donald Knuth's Algorithm X.

    @args sudoku (ndarray) : the sudoku to solve
    @returns (generator obj) : Solved sudoku if sudoku has solution,
                               else (9,9) numpy array with values -1
    '''

    matrix_a = get_mat_a().copy()

    constraints = get_constraints()

    # Populate matrix A with constraints
    for i, consts in constraints.items():
        for j in consts:
            matrix_a[j].add(i)

    # Update constraints to reflect initial state
    for (row, col), cell in ndenumerate(sudoku):
        if cell != 0:
            try:
                select(matrix_a, constraints, (row, col, cell))
            except KeyError:
                # Sudoku is not solvable
                return full((9, 9), -1)

    # find solution and update initial state with it
    for solution in find_solution(matrix_a, constraints, []):
        for (row, col, val) in solution:
            # Fill original values directly into input sudoku to save time
            sudoku[row][col] = val
        return sudoku

    return full((9, 9), -1)

#   ____             _    _                  _
#  |  _ \           | |  | |                | |
#  | |_) | __ _  ___| | _| |_ _ __ __ _  ___| | __
#  |  _ < / _` |/ __| |/ / __| '__/ _` |/ __| |/ /
#  | |_) | (_| | (__|   <| |_| | | (_| | (__|   <
#  |____/ \__,_|\___|_|\_\\__|_|  \__,_|\___|_|\_\

def backtrack(sudoku):
    '''
    Solves a sudoku using backtracking.
    If there is no solution, return unsolvable.

    Assumes all initial values are correct;
    solution must be checked to ensure sudoku is correct.

    @args:
        sudoku (ndarray) The sudoku to solve

    @returns:
        solution (ndarray) : The solved sudoku

        solved (bool) : Whether the solver has found a solution.
    '''

    digits = arange(1, 10)
    x, y = where(sudoku == 0)
    if x.size == 0:
        # Sudoku has been filled
        return True, sudoku

    cur_x, cur_y = x[0], y[0]

    row = sudoku[cur_x, :]  # list of values in current row
    col = sudoku[:, cur_y]  # list of values in current col
    i, j = (cur_x//3)*3, (cur_y//3)*3  # coords of top left of box
    box = sudoku[i:i+3, j:j+3].ravel()  # List of values in current box

    # Get all values that cannot be in this cell
    used_vals = reduce(union1d, (row, col, box))
    candidates = setdiff1d(digits, used_vals)

    sudoku_copy = npcopy(sudoku)

    # Backtrack for each branch
    for val in candidates:
        sudoku_copy[cur_x, cur_y] = val
        recurse = backtrack(sudoku_copy)

        if recurse[0]:
            return recurse

    return False, None


def check_solved(sudoku) -> ndarray((9,9)):
    '''
    Checks if a given sudoku solution is valid.

    @args:
        sudoku (ndarray) : Sudoku to check

    @returns:
        The input sudoku if solution is valid, else unsolvable
    '''

    for i in range(9):
        x = (i//3)*3
        y = (i%3)*3

        if (
            # Check each row has all digits
            len(set(sudoku[i, :])) !=9 or \
            # Check each col has all digits
            len(set(sudoku[:, i])) !=9 or \
            # Check each box has all digits
            len(set(sudoku[x:x+3, y:y+3].ravel())) !=9
        ):
            return full((9, 9), -1)
    return sudoku

#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|


def sudoku_solver(initial_state) -> ndarray((9,9)):
    '''
    Solves a sudoku using either a backtracking algorithm or Algorithm X,
    depending on which one is faster for the given sudoku.

    @args:
        initial_state (ndarray) : The unsolved sudoku

    @returns:
        solution (ndarray) : The solved sudoku
    '''

    # Decide which algorithm to use
    if count_nonzero(initial_state) > 39:

        # Optimised for easier sudokus
        solvable, sol = backtrack(initial_state)
        if solvable:
            return check_solved(sol)
        else:
            return full((9,9), -1)

    # Optimised for harder sudokus
    return solve_alg_x(initial_state)