"""
6.1010 Spring '23 Lab 7: Mines
"""

#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    # num_rows, num_cols = game["dimensions"]

    # if game["state"] == "defeat" or game["state"] == "victory":
    #     game["state"] = game["state"]  # keep the state the same
    #     return 0

    # if game["board"][row][col] == ".":
    #     game["hidden"][row][col] = False
    #     game["state"] = "defeat"
    #     return 1

    # if game["hidden"][row][col]:
    #     game["hidden"][row][col] = False
    #     revealed = 1
    # else:
    #     return 0

    # if game["board"][row][col] == 0:

    #     for neighbor_row in range(row - 1, row + 2):
    #         for neighbor_col in range(col - 1, col + 2):
    #             if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols and game["board"][neighbor_row][neighbor_col] != "." and game["hidden"][neighbor_row][neighbor_col]:
    #                 revealed += dig_2d(game, neighbor_row, neighbor_col)

    # victory_check = True
    # for check_row in range(num_rows):
    #     for check_col in range(num_cols):
    #         if game["board"][check_row][check_col] == "." and not game["hidden"][check_row][check_col]:
    #             game["state"] = "defeat"
    #             return 0
    #         elif game["hidden"][check_row][check_col] and game["board"][check_row][check_col] != ".":
    #             victory_check = False
    # if victory_check:
    #     game["state"] = "victory"
    #     return revealed

    # return revealed
    return dig_nd(game, (row, col))


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    row_num = game["dimensions"][0]
    rendered_locs = render_2d_locations(game, xray)
    joined_rows = []
    for row in range(row_num):
        joined_rows.append("".join(rendered_locs[row]))
    rendered_board = "\n".join(joined_rows)
    return rendered_board


# N-D IMPLEMENTATION


def get_value(array, coords):
    """
    Given an array and a list or tuple of coordinates, return
    the value of the array at those coordinates.
    >>> board = [[[3, '.'], [3, 3], [1, 1], [0, 0]],[['.', 3], [3, '.'], [1, 1], [0, 0]]]
    >>> coords = [1, 2, 1]
    >>> get_value(board, coords)
    1
    """
    if not coords:
        return array
    else:
        return get_value(array[coords[0]], coords[1:])


def set_value(array, coords, value):
    """
    Given an array, a list or tuple of coordinates, and a value,
    set the value of the array at those coordinates to the given value.
    >>> board = [[[3, '.'], [3, 3], [1, 1], [0, 0]],[['.', 3], [3, '.'], [1, 1], [0, 0]]]
    >>> coords = [1, 2, 1]
    >>> set_value(board, coords, 7)
    >>> board
        [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 7], [0, 0]]]
    """
    if len(coords) == 1:
        array[coords[0]] = value
    else:
        set_value(array[coords[0]], coords[1:], value)


def create_value_array(dimensions, value):
    """
    Given a list or tuple of dimensions and a value, return an array
    of the given dimensions where each value is the given value.
    >>> create_value_array((2, 2, 3), 2)
    [[[2, 2, 2], [2, 2, 2]], [[2, 2, 2], [2, 2, 2]]]
    """
    if len(dimensions) == 1:
        new_array = []
        for _ in range(dimensions[0]):
            new_array.append(value)
        return new_array
    else:
        new_array = []
        for _ in range(dimensions[0]):
            new_array.append(create_value_array(dimensions[1:], value))
        return new_array


def get_state(game):
    """
    Given a game, return the state of the game (victory, defeat, or ongoing)
    >>> game = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> get_state(game)
    'ongoing'
    """
    victory_check = "victory"
    for coords in get_possible_coords(game["dimensions"]):
        if get_value(game["board"], coords) == "." and not get_value(
            game["hidden"], coords
        ):
            return "defeat"
        elif get_value(game["board"], coords) != "." and get_value(
            game["hidden"], coords
        ):
            victory_check = "ongoing"
    return victory_check


def get_neighbors(coords, dimensions, curr_list=False):
    """
    Given a list or tuple of coordinates and the dimensions of a board,
    return the coordinates of the neighbors.
    >>> get_neighbors([1, 0, 2], [3, 3, 3])
    [[0, 0, 1], [0, 0, 2], [0, 1, 1], [0, 1, 2], [1, 0, 1], [1, 0, 2], [1, 1, 1], [1, 1, 2], [2, 0, 1], [2, 0, 2], [2, 1, 1], [2, 1, 2]]
    """
    if not curr_list:
        curr_list = []
        for neighbor_coord in range(coords[0] - 1, coords[0] + 2):
            if 0 <= neighbor_coord < dimensions[0]:
                curr_list.append([neighbor_coord])
        return get_neighbors(coords[1:], dimensions[1:], curr_list)
    if not coords:
        return curr_list
    else:
        for _ in range(len(curr_list)):
            prev_part = curr_list.pop(0)
            for neighbor_coord in range(coords[0] - 1, coords[0] + 2):
                if 0 <= neighbor_coord < dimensions[0]:
                    curr_list.append(prev_part + [neighbor_coord])
        return get_neighbors(coords[1:], dimensions[1:], curr_list)


def get_possible_coords(dimensions, curr_list=False):
    """
    Given a list or tuple of dimensions of a board,
    return the coordinates of all board entries.
    >>> get_possible_coords((2, 1, 2))
    [[0, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 1]]
    """
    if not curr_list:
        curr_list = []
        for coord in range(dimensions[0]):
            curr_list.append([coord])
        return get_possible_coords(dimensions[1:], curr_list)
    if not dimensions:
        return curr_list
    else:
        for _ in range(len(curr_list)):
            prev_part = curr_list.pop(0)
            for coord in range(dimensions[0]):
                curr_list.append(prev_part + [coord])
        return get_possible_coords(dimensions[1:], curr_list)


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    hidden = create_value_array(dimensions, True)
    board = create_value_array(dimensions, 0)
    for bomb_coords in bombs:
        set_value(board, bomb_coords, ".")

    for bomb_coords in bombs:
        for neighbor in get_neighbors(bomb_coords, dimensions):
            if get_value(board, neighbor) != ".":
                set_value(board, neighbor, get_value(board, neighbor) + 1)
    return {
        "dimensions": (dimensions),
        "board": board,
        "hidden": hidden,
        "state": "ongoing",
    }


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """

    def dig_nd_helper(game, coordinates):
        coord_value = get_value(game["board"], coordinates)
        coord_hidden = get_value(game["hidden"], coordinates)

        if game["state"] == "defeat" or game["state"] == "victory":
            game["state"] = game["state"]  # keep the state the same
            return 0

        if coord_value == ".":
            set_value(game["hidden"], coordinates, False)
            game["state"] = "defeat"
            return 1

        if coord_hidden:
            set_value(game["hidden"], coordinates, False)
            revealed = 1
        else:
            return 0

        if coord_value == 0:
            for neighbor in get_neighbors(coordinates, game["dimensions"]):
                revealed += dig_nd_helper(game, neighbor)

        return revealed

    revealed = dig_nd_helper(game, coordinates)

    state = get_state(game)
    game["state"] = state

    return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    render = create_value_array(game["dimensions"], " ")
    for coords in get_possible_coords(game["dimensions"]):
        if not xray and get_value(game["hidden"], coords):
            set_value(render, coords, "_")
        elif get_value(game["board"], coords) != 0 or (
            not xray and get_value(game["hidden"], coords)
        ):
            set_value(render, coords, str(get_value(game["board"], coords)))
    return render


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    doctest.run_docstring_examples(
        set_value, globals(), optionflags=_doctest_flags, verbose=False
    )
