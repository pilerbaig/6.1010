import sys
import typing
import doctest

sys.setrecursionlimit(10_000)


# NO ADDITIONAL IMPORTS
def new_formula_creator(formula, var_and_val):
    """creates a new formula"""
    var, val = var_and_val
    new_formula = [
        [
            (sub_var, sub_val)
            for sub_var, sub_val in clauses
            if (sub_var, sub_val) != (var, not val)
        ]
        for clauses in formula
        if (var, val) not in set(clauses)
    ]
    return new_formula


def get_unit_clauses(formula):
    """finds unit clauses"""
    ans = {}
    for clause in formula:
        if len(clause) == 1:
            var, val = clause[0][0], clause[0][1]
            ans[var] = val
    return ans


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    # base case
    if len(formula) == 0:
        return {}
    # checks if that solution doesn't work
    if [] in formula:
        return None
    # ans becomes a dictionary mapping the variable
    # and value for all unit clauses
    ans = get_unit_clauses(formula)
    # if there are not unit clauses it just takes the
    # first value in the formula
    if len(ans) == 0:
        var, val = formula[0][0]
        ans = {var: val}
    else:
        var, val = list(ans.items())[0]
    # creates new formula trying out the var and val
    new_formula = new_formula_creator(formula, (var, val))
    # if the formula is an empty list, it adds to the dictionary
    # to be returned and returns the dictionary
    if not new_formula:
        return ans
    # if not tries to recursively solve by setting more values
    rec1 = satisfying_assignment(new_formula)
    if rec1 is not None:
        rec1[var] = val
        return rec1
    # if this returns None, it tries the opposite value
    val = not val
    # creates new formula with that opposite value
    new_formula = new_formula_creator(formula, (var, val))
    if not new_formula:
        return {var: val}
    # does same thing
    rec2 = satisfying_assignment(new_formula)
    if rec2 is not None:
        rec2[var] = val
        return rec2
    # returns None if no solution
    return None


def quad_finder(n):
    """finds the quadrants"""
    quad = int(n ** (1 / 2))
    ans = [[[] for k in range(quad)] for i in range(quad)]
    for row in range(n):
        for col in range(n):
            # quad = int(n**(1/2))
            rem_row = row // quad
            rem_col = col // quad
            ans[rem_row][rem_col].append((row, col))
    answer = []
    for a_list in ans:
        for sub_lists in a_list:
            answer.append(sub_lists)
    return answer


# print(quad_finder(4))


def pair_creator(combs):
    """creates some pairs"""
    ans = []
    for thing in combs:
        for sub_thing in [n for n in combs if n != thing]:
            ans.append([sub_thing, thing])
    return ans


def num_finder_and_at_leaster(sudoku_board, dim, formula):
    """finds all the numbers that are already on the
    board and adds them as unit clauses, then adds literals
    that make sure there's a number in every spot"""
    # dim = len(sudoku_board)
    for_board = range(dim)
    # formula = []
    for r in for_board:
        for c in for_board:
            if sudoku_board[r][c] != 0:
                formula.append([((r, c, sudoku_board[r][c]), True)])
            else:
                formula.append([((r, c, number), True) for number in range(1, dim + 1)])
    # return formula


def col_excluser(sudoku_board, dim, formula):
    """makes sure theres not a duplicate in a column"""
    # dim = len(sudoku_board)
    # formula = []
    for num in range(1, dim + 1):
        for big_col in range(dim):
            col_list = [((row, big_col, num), False) for row in range(dim)]
            for combos in pair_creator(col_list):
                formula.append(combos)
    # return formula


def row_excluser(sudoku_board, dim, formula):
    """makes sure there's not a duplicate in a row"""
    # dim = len(sudoku_board)
    # formula = []
    for num in range(1, dim + 1):
        for big_row in range(dim):
            row_list = [((big_row, col, num), False) for col in range(dim)]
            for combos in pair_creator(row_list):
                formula.append(combos)
    # return formula


def quad_excluser(sudoku_board, dim, formula):
    """makes sure there's not a duplicate in a block"""
    # dim = len(sudoku_board)
    # formula = []
    for num in range(1, dim + 1):
        for quad in quad_finder(dim):
            quad = [(loc + (num,), False) for loc in quad]
            for combos in pair_creator(quad):
                formula.append(combos)
    # return formula


# print(pair_creator([1,2,3,4]))

def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    # creates formula
    formula = []
    dim = len(sudoku_board)
    # adds literals to it using helper functions
    num_finder_and_at_leaster(sudoku_board, dim, formula)
    col_excluser(sudoku_board, dim, formula)
    row_excluser(sudoku_board, dim, formula)
    quad_excluser(sudoku_board, dim, formula)
    return formula


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    # if there's no solution returns None
    if assignments is None:
        return None
    # if the value in the dictionary is True, it adds to answer,
    # which is a list of list representing a board
    answer = [[0 for k in range(n)] for i in range(n)]
    for row, col, num in assignments:
        if assignments[(row, col, num)] is True:
            answer[row][col] = num
    return answer


if __name__ == "__main__":
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)
    grid = [
        [0, 0, 0, 2],
        [0, 0, 0, 1],
        [4, 0, 0, 0],
        [2, 0, 0, 0],
    ]
    form = []
    row_excluser(grid, 4, form)
    print(form)
    # print(quad_finder(9))