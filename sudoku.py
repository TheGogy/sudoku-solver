from itertools import product
from numpy import ndarray, add, ndenumerate, full, array, size

#                      _        __   __
#                /\   | |       \ \ / /
#    ______     /  \  | | __ _   \ V /   ______
#   |______|   / /\ \ | |/ _` |   > <   |______|
#             / ____ \| | (_| |  / . \
#            /_/    \_\_|\__, | /_/ \_\
#                         __/ |
#                        |___/

def select(matrix_A, constraints, row):
    '''
    removes associated rows, cols from matrix
    @args:
        matrix_A: the search space matrix
        constraints: the constraints matrix
        row: The row to be selected
    '''
    cols = []
    for i in constraints[row]:
        for j in matrix_A[i]:
            for k in constraints[j]:
                if k != i:
                    matrix_A[k].remove(j)
        cols.append(matrix_A.pop(i))
    return cols

def deselect(matrix_A, constraints, row, cols) -> None:
    '''
    Restores a branch with a no solutions back into matrix_A

    @args
        matrix_A: The search space matrix
        constraints: the constraints matrix
        row, cols: value to restore to matrix A
    '''
    for i in reversed(constraints[row]):
        matrix_A[i] = cols.pop()
        for j in matrix_A[i]:
            for k in constraints[j]:
                if k != i:
                    matrix_A[k].add(j)

def find_solution(matrix_A, constraints, solution=[]) -> list:
    '''
    Recursively attempts to find a solution

    @args
        matrix_A: The search space matrix
        constraints: The constraints matrix
        solution: The state to find (or not find) soltion for

    @returns list: The solution
    '''
    if not matrix_A:
        # There are no constraints left to fulfil; sudoku solved.
        yield list(solution)
    else:
        col = choose_col(matrix_A, constraints)
        for row in list(matrix_A[col]):
            solution.append(row)
            cols = select(matrix_A, constraints, row)

            # Keep trying to find solution recursively
            for i in find_solution(matrix_A, constraints, solution): yield i

            # This branch does not have a solution, deselect it
            deselect(matrix_A, constraints, row, cols)

            # Remove value from this possible solution
            solution.pop()


def choose_col(matrix_A, constraints):
    """
    Returns col with fewest possible values.

    @args
        matrix_A: the search space matrix
        constraints: The constraints matrix

    @returns
        col : the column with the fewest possible values
    """

    best_col_val = float("inf")
    best_col = None

    for col in matrix_A:
        cur_col_val = len(matrix_A[col])
        if best_col_val > cur_col_val:

            best_col = col
            best_col_val = cur_col_val

            # Do not waste time if we have already found a column with only
            # one value
            if cur_col_val == 1:
                break

    return best_col

#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|


def sudoku_solver(sudoku) -> ndarray or None:
    '''
    Solves the given sudoku using Donald Knuth's Algorithm X.

    @args sudoku (ndarray) : the sudoku to solve
    @returns: solution
    @returns (generator obj) : Solved sudoku if sudoku has solution
    '''

    matrix_A = {j: set() for j in(
        [("cell", i) for i in product (range(9), range(9)    )] +
        [("row",  i) for i in product (range(9), range(1, 10))] +
        [("col",  i) for i in product (range(9), range(1, 10))] +
        [("box",  i) for i in product (range(9), range(1, 10))]
        )}

    constraints = {}
    for row, col, cell in product(range(9), range(9), range(1, 10)):
        box = (row // 3) * 3 + (col // 3)
        # Boxes are labelled like this:
        #   0 1 2
        #   3 4 5
        #   6 7 8
        constraints[(row, col, cell)] = [
            # Each cell must have a value
            ("cell", (row, col)),
            # Each row must have each value
            ("row",  (row, cell)),
            # Each column must have each value
            ("col",  (col, cell)),
            # Each box must have each value
            ("box",  (box, cell))
        ]

    # Populate matrix A with constraints
    for i, consts in constraints.items():
        for j in consts:
            matrix_A[j].add(i)

    # Update constraints to reflect initial state
    for (row, col), cell in ndenumerate(sudoku):
        if cell != 0:
            try:
                select(matrix_A, constraints, (row, col, cell))
            except KeyError:
                # Sudoku is not solvable
                return full((9, 9), fill_value=-1)

    # find solution and update initial state with it
    for solution in find_solution(matrix_A, constraints, []):
        for (row, col, val) in solution:
            sudoku[row][col] = val
        return sudoku

    return full((9, 9), fill_value=-1)
