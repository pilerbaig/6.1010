"""
6.1010 Spring '23 Lab 4: Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}
direction_strings = direction_vector.keys()


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    # create at empty set for each object and store them in a dictionary
    #   along with the width and height
    object_locations = {"player": set(), "computer": set(),
                        "target": set(), "wall": set(), "width": 0, "height": 0}
    # iterate through the rows and columns
    for row, row_list in enumerate(level_description):
        for col, cell in enumerate(row_list):
            # add the location for each object
            for object_type in cell:
                object_locations[object_type].add((row, col))
    object_locations["player"] = object_locations["player"].pop()
    # get the width and length
    object_locations["width"] = len(level_description[0])
    object_locations["height"] = len(level_description)
    # return the representation
    return object_locations


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    # check if the computers and targets are in the same
    #   location, and there are targets
    return game["computer"] == game["target"] and game["target"] != set()


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    # copy the sets of object locations
    wall_set = game["wall"].copy()
    computer_set = game["computer"].copy()
    target_set = game["target"].copy()
    player_location = game["player"]
    # get the direction tuple
    direction_tuple = direction_vector[direction]
    # check the next and location after in the direction
    one_step = object_step(player_location, direction_tuple)
    two_step = object_step(one_step, direction_tuple)
    # if the next step is a wall or out of bounds
    if one_step in wall_set or not in_grid(game, one_step):
        # the player does not move
        pass
    # if the next is a computer
    elif one_step in computer_set:
        # if the one next to the computer is a computer, wall or out of bounds
        if two_step in computer_set or two_step in \
                wall_set or not in_grid(game, two_step):
            # player doesn't move
            pass
        else:
            # player moves one step
            player_location = one_step
            # computer in next spot moves one over
            computer_set.remove(one_step)
            computer_set.add(two_step)
    else:
        # player moves one step
        player_location = one_step
    # make a new game state with the created sets and return it
    new_game_state = {"player": player_location, "computer": computer_set,
                      "target": target_set, "wall": wall_set,
                      "width": game["width"], "height": game["height"]}
    return new_game_state


def object_step(location, direction):
    new_location = (tuple(sum(step) for step in zip(location, direction)))
    return new_location


def in_grid(game, location):
    """
    Given a game representation (of the form returned from new_game) and a location,
    check if the location is in the game board and return the boolean.
    """
    # get the row and column of location
    row = location[0]
    col = location[1]
    # check if the row and column are in the range and return
    row_check = 0 <= row < game["height"]
    col_check = 0 <= col < game["width"]
    return row_check and col_check


def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    # create an empty game board
    game_board = []
    # iterate through the rows and columns, creating the empty board
    for row in range(game["height"]):
        game_board.append([])
        for col in range(game["width"]):
            game_board[row].append([])
            # check if each location comtains each object and add to the dumped game
            for object_type in ("computer", "target", "wall"):
                if (row, col) in game[object_type]:
                    game_board[row][col].append(object_type)
            if (row, col) == game["player"]:
                game_board[row][col].append("player")
    # return the game board
    return game_board


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    # check if the initial game is won and return no moves if it is
    if victory_check(game):
        return []
    # create the agenda, including the current game and list of moves
    possible_plays = [(game, [])]
    # create an empty set of checked states
    checked_states = set()
    # while the agenda is not empty
    while possible_plays:
        # get the board and move list from the agenda
        (current_board, current_list) = possible_plays.pop(0)
        # create the current state, represented as frozen sets of
        #   player and computer locations (only changeable objects)
        current_state = (current_board["player"],
                         frozenset(current_board["computer"]))
        # if the current state has not been checked
        if current_state not in checked_states:
            # for each possible direction (neighbors)
            for direction in direction_strings:
                # get the next board
                next_board = step_game(current_board, direction)
                # get the next move list
                next_list = current_list + [direction]
                # if the board wins
                if victory_check(next_board):
                    return next_list
                # add the next game and list to the agenda
                possible_plays.append((next_board, next_list))
                # add the current state to the checked states
                checked_states.add(current_state)
    # return None if there is no solution
    return None


if __name__ == "__main__":
    level = [
        [["wall"],  ["wall"],  ["wall"],      [
            "wall"],             ["wall"], ["wall"]],
        [["wall"],  [],        [],
            [],                   [],       ["wall"]],
        [["wall"],  [],        ["computer", "target"],            [
            "player"], [],       ["wall"]],
        [["wall"],  ["wall"],  ["wall"],      [
            "wall"],             ["wall"], ["wall"]]
    ]
    game_1 = new_game(level)
    print(dump_game(game_1))
    # print(solve_puzzle(game_1))
