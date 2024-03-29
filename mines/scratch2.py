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
    if game["state"] == "defeat" or game["state"] == "victory":
        game["state"] = game["state"]  # keep the state the same
        return 0

    if game["board"][row][col] == ".":
        game["hidden"][row][col] = False
        game["state"] = "defeat"
        return 1

    bombs = 0
    hidden_squares = 0
    for r in range(game["dimensions"][0]):
        for c in range(game["dimensions"][1]):
            if game["board"][r][c] == ".":
                if game["hidden"][r][c] == False:
                    bombs += 1
            elif game["hidden"][r][c] == True:
                hidden_squares += 1
    if bombs != 0:
        # if bombs is not equal to zero, set the game state to defeat and
        # return 0
        game["state"] = "defeat"
        return 0
    if hidden_squares == 0:
        game["state"] = "victory"
        return 0

    if game["hidden"][row][col] != False:
        game["hidden"][row][col] = False
        revealed = 1
    else:
        return 0

    if game["board"][row][col] == 0:
        num_rows, num_cols = game["dimensions"]
        if 0 <= row - 1 < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row - 1][col - 1] != ".":
                    if game["hidden"][row - 1][col - 1] == True:
                        revealed += dig_2d(game, row - 1, col - 1)
        if 0 <= row < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row][col - 1] != ".":
                    if game["hidden"][row][col - 1] == True:
                        revealed += dig_2d(game, row, col - 1)
        if 0 <= row + 1 < num_rows:
            if 0 <= col - 1 < num_cols:
                if game["board"][row + 1][col - 1] != ".":
                    if game["hidden"][row + 1][col - 1] == True:
                        revealed += dig_2d(game, row + 1, col - 1)
        if 0 <= row - 1 < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row - 1][col] != ".":
                    if game["hidden"][row - 1][col] == True:
                        revealed += dig_2d(game, row - 1, col)
        if 0 <= row < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row][col] != ".":
                    if game["hidden"][row][col] == True:
                        revealed += dig_2d(game, row, col)
        if 0 <= row + 1 < num_rows:
            if 0 <= col < num_cols:
                if game["board"][row + 1][col] != ".":
                    if game["hidden"][row + 1][col] == True:
                        revealed += dig_2d(game, row + 1, col)
        if 0 <= row - 1 < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row - 1][col + 1] != ".":
                    if game["hidden"][row - 1][col + 1] == True:
                        revealed += dig_2d(game, row - 1, col + 1)
        if 0 <= row < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row][col + 1] != ".":
                    if game["hidden"][row][col + 1] == True:
                        revealed += dig_2d(game, row, col + 1)
        if 0 <= row + 1 < num_rows:
            if 0 <= col + 1 < num_cols:
                if game["board"][row + 1][col + 1] != ".":
                    if game["hidden"][row + 1][col + 1] == True:
                        revealed += dig_2d(game, row + 1, col + 1)

    bombs = 0  # set number of bombs to 0
    hidden_squares = 0
    for r in range(game["dimensions"][0]):
        # for each r,
        for c in range(game["dimensions"][1]):
            # for each c,
            if game["board"][r][c] == ".":
                if game["hidden"][r][c] == False:
                    # if the game hidden is False, and the board is '.', add 1 to
                    # bombs
                    bombs += 1
            elif game["hidden"][r][c] == True:
                hidden_squares += 1
    bad_squares = bombs + hidden_squares
    if bad_squares > 0:
        game["state"] = "ongoing"
        return revealed
    else:
        game["state"] = "victory"
        return revealed


game = {'dimensions': (2, 4),
        'board': [['.', 3, 1, 0],
                  ['.', '.', 1, 0]],
        'hidden': [[True, False, True, True],
                   [True, True, True, True]],
        'state': 'ongoing'}
print(dig_2d(game, 0, 3))
lab.dump(game)
