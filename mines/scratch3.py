import lab
import doctest

# def new_game_nd()


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


def get_value(array, coords):
    if not coords:
        return array
    else:
        return get_value(array[coords[0]], coords[1:])


# board = [[[3, '.'], [3, 3], [1, 1], [0, 0]],
#          [['.', 3], [3, '.'], [1, 1], [0, 0]]]
# coords = [1, 2, 1]
# print(get_coords(board, coords))

def set_value(array, coords, value):
    if len(coords) == 1:
        array[coords[0]] = value
    else:
        set_value(array[coords[0]], coords[1:], value)


# board = [[[3, '.'], [3, 3], [1, 1], [0, 0]],
#          [['.', 3], [3, '.'], [1, 1], [0, 0]]]
# coords = [1, 2, 1]
# set_value(board, coords, "boop")
# print(board)

def create_value_array(dimensions, value):
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


# arrayy = create_value_array([3, 4], 7)
# set_value(arrayy, (0, 0), 2)
# print(arrayy)

def get_state(game):
    if len(game["dimensions"]) == 1:
        for index in range(game["dimensions"][0]):
            if game["board"][index] == "." and not game["hidden"][index]:
                return "defeat"
            elif game["board"][index] != "." and game["hidden"][index]:
                return "ongoing"
        return "victory"

    else:
        state_list = []
        for index in range(game["dimensions"][0]):
            new_game = {'dimensions': game["dimensions"][1:], 'state': 'ongoing',
                        'board': game["board"][0], 'hidden': game["hidden"][0]}
            state_list.append(get_state(new_game))
        if "defeat" in state_list:
            return "defeat"
        elif "ongoing" in state_list:
            return "ongoing"
        else:
            return "victory"


# game = {'dimensions': (2, 2, 2), 'state': 'ongoing', 'board':
#         [[['.', 3], [2, 3]], ['.', 3], [2, 3]], 'hidden': [[[True, True], [True, True]], [[True, True], [True, True]]]}
# print(get_state(game))


def get_neighbors(coords, dimensions, curr_list=False):
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

# print(get_neighbors([1, 1, 1], [3, 3, 3]))


def get_possible_coords(dimensions, curr_list=False):
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


# print(get_possible_coords([10, 10, 10, 10, 10]))


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
        set_value(board, bomb_coords, '.')
    print(hidden)
    print(board)

    for coords in get_possible_coords(dimensions):
        if get_value(board, coords) == 0:
            neighbor_bombs = 0
            for neighbor in get_neighbors(coords, dimensions):
                if get_value(board, neighbor) == '.':
                    neighbor_bombs += 1
            set_value(board, coords, neighbor_bombs)
    return {
        "dimensions": (dimensions),
        "board": board,
        "hidden": hidden,
        "state": "ongoing",
    }


# g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
# lab.dump(g)


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
            revealed += dig_nd(game, neighbor)

    victory_check = True
    for coords in get_possible_coords(game["dimensions"]):
        if get_value(game["board"], coords) == "." and not get_value(game["hidden"], coords):
            game["state"] = "defeat"
            return revealed
        elif get_value(game["board"], coords) != "." and get_value(game["hidden"], coords):
            victory_check = False
    if victory_check:
        game["state"] = "victory"

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
        elif get_value(game["board"], coords) != 0 or (not xray and get_value(game["hidden"], coords)):
            set_value(render, coords, str(
                get_value(game["board"], coords)))
    return render
    # else:
    #     for coords in get_possible_coords(game["dimensions"]):
    #         if get_value(game["board"], coords) != 0:
    #             set_value(render, coords, str(get_value(game["board"], coords)))
    #     return render

    # row_num = game['dimensions'][0]
    # col_num = game['dimensions'][1]
    # loc_render = []
    # if xray:
    #     for row in range(row_num):
    #         loc_render.append([])
    #         for col in range(col_num):
    #             if game['board'][row][col] == 0:
    #                 loc_render[row].append(' ')
    #             else:
    #                 loc_render[row].append(str(game['board'][row][col]))
    #     return loc_render
    # for row in range(row_num):
    #     loc_render.append([])
    #     for col in range(col_num):
    #         if game["hidden"][row][col]:
    #             loc_render[row].append("_")
    #         elif game['board'][row][col] == 0:
    #             loc_render[row].append(' ')
    #         else:
    #             loc_render[row].append(str(game["board"][row][col]))
    # return loc_render


# _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
# doctest.run_docstring_examples(
#     render_nd,
#     globals(),
#     optionflags=_doctest_flags,
#     verbose=False
# )
g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
dump(g)
