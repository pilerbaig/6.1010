"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a',None) is True or x.get('b',None) is False or x.get('c',None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """

    assignments = {}
    formula, assignments = remove_unit_clauses(formula)
    if not formula:
        return assignments
    if formula is None:
        return None
    if [] in formula:
        return None
    var_set = variable_set(formula)
    var = var_set.pop()
    for value in (True, False):
        updated_formula = update_formula(formula, (var, value))
        recursive_result = satisfying_assignment(updated_formula)
        if recursive_result is not None:
            return {var: value} | recursive_result | assignments
    return None


def remove_unit_clauses(formula):
    """
    Find unit clauses in the formula and remove them,
    continue to remove them until there are none left
    """
    assignments = {}
    while True:
        changed = False
        for clause in formula:
            if len(clause) == 1:
                changed = True
                formula = update_formula(formula, clause[0])
                assignments = assignments | {clause[0][0]: clause[0][1]}
                break
        if not changed:
            return formula, assignments


def update_formula(formula, assignment):
    """
    Update a CNF formula based on the assignment passed in.
    >>> formula = [[('a', True), ('b', True), ('c', False)],[('c', True), ('d', True)]]
    >>> assignment = ('c', True)
    >>> update_formula(formula, assignment)
    [[('a', True), ('b', True)]]
    """
    new_formula = []
    opposite_assignment = (assignment[0], not assignment[1])
    for clause in formula:
        if assignment not in clause:
            if opposite_assignment in clause:
                new_clause = [
                    literal for literal in clause if literal != opposite_assignment]
                new_formula.append(new_clause)
            else:
                new_formula.append(clause)
    return new_formula


def variable_set(formula):
    """
    From a formula, get a set of all the variables involved.
    >>> formula = [[('a', True), ('b', True), ('c', False)],[('c', True), ('d', True)]]
    >>> var_set = variable_set(formula)
    >>> var_set == {'a', 'b', 'c', 'd'}
    True
    """
    var_set = set()
    for clause in formula:
        for literal in clause:
            var_set.add(literal[0])
    return var_set


def filled_squares(sudoku_board):
    """
    Rule that states that each pre-filled square must
    contain the given number.
    """
    sub_formula = []
    dim = len(sudoku_board)
    for row in range(dim):
        for col in range(dim):
            if sudoku_board[row][col]:
                sub_formula.append([((row, col, sudoku_board[row][col]), True)])
    return sub_formula

def row_rule(sudoku_board):
    """
    Rule that states that there must be one of each number
    in each row of the board.
    """
    sub_formula = []
    dim = len(sudoku_board)

    for row in range(dim):
        for num in range(1, dim + 1):
            num_clause = []
            for col in range(dim):
                cols = list(range(dim))
                pairs = get_pairs(cols)
                num_clause.append(((row, col, num), True))
                pair_check = []
                for pair in pairs:
                    pair_check.append(
                        [((row, pair[0], num), False), ((row, pair[1], num), False)]
                    )
            sub_formula.append(num_clause)
            sub_formula.extend(pair_check)
    return sub_formula


def col_rule(sudoku_board):
    """
    Rule that states that there must be one of each number
    in each column of the board
    """
    sub_formula = []
    dim = len(sudoku_board)
    for col in range(dim):
        for num in range(1, dim + 1):
            num_clause = []
            for row in range(dim):
                rows = list(range(dim))
                pairs = get_pairs(rows)
                num_clause.append(((row, col, num), True))
                pair_check = []
                for pair in pairs:
                    pair_check.append(
                        [((pair[0], col, num), False), ((pair[1], col, num), False)]
                    )
            sub_formula.append(num_clause)
            sub_formula.extend(pair_check)
    return sub_formula

def subgrid_rule(sudoku_board):
    """
    Rule that states that there must be one of each number
    in each subgrid of dimension sqrt(n) in the board.
    """
    sub_formula = []
    dim = len(sudoku_board)
    sqrt_dim = int(dim ** (1 / 2))
    for sub_row in range(sqrt_dim):
        for sub_col in range(sqrt_dim):
            # subgrid_entries = []
            for num in range(1, dim + 1):
                num_clause = []
                coord_list = []
                for row in range(sub_row * sqrt_dim, sub_row * sqrt_dim + sqrt_dim):
                    for col in range(sub_col * sqrt_dim, sub_col * sqrt_dim + sqrt_dim):
                        num_clause.append(((row, col, num), True))
                        # subgrid_entries.append(((row, col, num), False))
                        # pairs = get_pairs(subgrid_entries)
                        coord_list.append((row, col))
                        # pairs = get_pairs(coord_list)
                        # pair_check = []
                        # for pair in pairs:
                        #     pair_check.append([((pair[0], col, num), False), 
                        #   ((pair[1], col, num), False)])

                sub_formula.append(num_clause)
                # sub_formula.extend(pair_check)
    return sub_formula


def all_squares(sudoku_board):
    """
    Rule that states that there must be a number from 1-9
    in each square of the board.
    """
    sub_formula = []
    dim = len(sudoku_board)
    nums = list(range(1, dim + 1))
    pairs = get_pairs(nums)
    for row in range(dim):
        for col in range(dim):
            square_entries = []
            for pair in pairs:
                square_entries.append(
                    [((row, col, pair[0]), False), ((row, col, pair[1]), False)]
                )
            sub_formula.extend(square_entries)
    return sub_formula


def get_pairs(entry_list):
    """
    From a list of entries, returns a list of all possible pairs
    (without duplicates).
    """
    pairs_list = []
    for entry in entry_list:
        for entry2 in entry_list:
            if entry2 != entry and [entry2, entry] not in pairs_list:
                pairs_list.append([entry, entry2])
    return pairs_list


def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    formula = []
    formula.extend(all_squares(sudoku_board))
    formula.extend(filled_squares(sudoku_board))
    formula.extend(row_rule(sudoku_board))
    formula.extend(col_rule(sudoku_board))
    formula.extend(subgrid_rule(sudoku_board))
    return formula


def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    board = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append([])
        board.append(row)
    print(board)

    if assignments is None:
        return None

    for key, val in assignments.items():
        if val:
            board[key[0]][key[1]] = key[2]
    return board


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    # form = [
    #     [("a", True), ("a", False)],
    #     [("b", True), ("a", True)],
    #     [("b", True)],
    #     [("b", False), ("b", False), ("a", False)],
    #     [("c", True), ("d", True)],
    #     [("c", True), ("d", True)],
    # ]
    # updateda = update_formula((form),('a', True))
    # print(form)
    # print(updateda)
    # print(update_formula((updateda),('b', True)))
    # print(satisfying_assignment(form))
    # new_formula, assignments = simplify_formula(form)
    # print(assignments)
    # print(new_formula)
    # print(remove_unit_clauses(form))
    # # print(filled_squares(grid))
    # print(subgrid_rule(grid))
    # print(filled_squares(grid))
    # sat = sudoku_board_to_sat_formula(grid)
    # sattt = satisfying_assignment(sat)
    # print(assignments_to_sudoku_board(sattt, 4))
