from itertools import product
from numpy import ndarray, add, ndenumerate, full, array

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
    Adds the given row to possible solutions and removes
    associated rows from matrix
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
    Removes a potential solution from the possible solutions
    and restores it into matrix A
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
        col = min(matrix_A, key=lambda d: len(matrix_A[d]))
        for row in list(matrix_A[col]):
            solution.append(row)
            cols = select(matrix_A, constraints, row)

            # Keep trying to find solution recursively
            for i in find_solution(matrix_A, constraints, solution): yield i

            # This row does not have a solution, deselect it
            deselect(matrix_A, constraints, row, cols)
            solution.pop()

#   ______                _
#  |  ____|              | |
#  | |__  __  ____ _  ___| |_    ___ _____   _____ _ __
#  |  __| \ \/ / _` |/ __| __|  / __/ _ \ \ / / _ \ '__|
#  | |____ >  < (_| | (__| |_  | (_| (_) \ V /  __/ |
#  |______/_/\_\__,_|\___|\__|  \___\___/ \_/ \___|_|


def exact_cover_solver(sudoku) -> ndarray or None:
    '''
    Solves the given sudoku using Donald Knuth's Dancing Links method.

    @args sudoku (ndarray) : the sudoku to solve
    @returns: None if sudoku has no solutions
    @returns (generator obj) : Solved sudoku if sudoku has solution
    '''

    matrix_A = (
        [("cell", i) for i in product (range(9), range(9)    )] +
        [("row", i)  for i in product (range(9), range(1, 10))] +
        [("col", i)  for i in product (range(9), range(1, 10))] +
        [("box", i)  for i in product (range(9), range(1, 10))]
        )
    matrix_A = {j: set() for j in matrix_A}

    constraints = dict()
    for row, col, cell in product(range(9), range(9), range(1, 10)):
        box = (row // 3) * 3 + (col // 3)
        # Boxes are labelled like this:
        #   0 1 2
        #   3 4 5
        #   6 7 8
        constraints[(row, col, cell)] = [
            # Each cell must have a value
            ("cell",    (row, col)),
            # Each row must have each value
            ("row",     (row, cell)),
            # Each column must have each value
            ("col",     (col, cell)),
            # Each box must have each value
            ("box",     (box, cell))
        ]

    # Populate matrix A with possible solutions
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
                return  None

    # find solution and pdate initial state with it
    for solution in find_solution(matrix_A, constraints, []):
        for (row, col, val) in solution:
            sudoku[row][col] = val
        yield sudoku

#   __  __       _
#  |  \/  |     (_)
#  | \  / | __ _ _ _ __
#  | |\/| |/ _` | | '_ \
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|


def sudoku_solver(initial_state) -> ndarray:
    '''
    Handles input and output of the solver.

    @args initial_state (ndarray) : 9x9 array containing sudoku to solve
    @returns solved sudoku. If no solutions found, return 9x9 grid of "-1".
    '''
    finalSolution = list(exact_cover_solver(initial_state))
    if not finalSolution:
        return full((9, 9), fill_value=-1)

    # Solution exists, return it
    return array(list(finalSolution))[0]