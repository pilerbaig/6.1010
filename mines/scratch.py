import lab


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
    num_rows, num_cols = game["dimensions"]

    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    if game["board"][row][col] == ".":
        game["hidden"][row][col] = False
        game["state"] = "defeat"
        return 1

    if game["hidden"][row][col]:
        game["hidden"][row][col] = False
        revealed = 1
    else:
        return 0

    if game["board"][row][col] == 0:

        for neighbor_row in range(row - 1, row + 2):
            for neighbor_col in range(col - 1, col + 2):
                if 0 <= neighbor_row < num_rows and 0 <= neighbor_col < num_cols and game["board"][neighbor_row][neighbor_col] != "." and game["hidden"][neighbor_row][neighbor_col]:
                    revealed += dig_2d(game, neighbor_row, neighbor_col)

    victory_check = True
    for check_row in range(num_rows):
        for check_col in range(num_cols):
            if game["board"][check_row][check_col] == "." and not game["hidden"][check_row][check_col]:
                game["state"] = "defeat"
                return 0
            elif game["hidden"][check_row][check_col] and game["board"][check_row][check_col] != ".":
                victory_check = False
    if victory_check:
        game["state"] = "victory"
        return 0

    return revealed


game = {'dimensions': (2, 4),
        'board': [['.', 3, 1, 0],
                  ['.', '.', 1, 0]],
        'hidden': [[True, False, True, True],
                   [True, True, True, True]],
        'state': 'ongoing'}
print(dig_2d(game, 0, 3))
lab.dump(game)
