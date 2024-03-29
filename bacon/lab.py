"""
6.1010 Spring '23 Lab 3: Bacon Number
"""

#!/usr/bin/env python3

import pickle

# NO ADDITIONAL IMPORTS ALLOWED!


def transform_data(raw_data):
    """
    Takes in the raw data, which is a list of tuples containing three ints:
    the first two are the ids of actors that acted in a movie together,
    and the third is the id of the movie that the actors acted in.
    Returns the data as a tuple containing two dicts:
    the first has actor ids as keys and sets of actors that they acted
    with as values, and the second has movie ids as keys and sets of
    actors that acted in the movie as values.
    """
    # create empty dictionaries to contain the ids and sets
    acted_with = {}
    movie_actors = {}
    # for each movie tuple in the raw data
    for movie in raw_data:
        # assign each actor and movie to a variable
        actor1 = movie[0]
        actor2 = movie[1]
        film = movie[2]
        actors = (actor1, actor2)
        # add each actor to the set pertaining to each
        #   actor, or create a new key and set for them
        if actor1 in acted_with.keys():
            acted_with[actor1] |= set(actors)
        else:
            acted_with[actor1] = set(actors)
        if movie[1] in acted_with.keys():
            acted_with[actor2] |= set(actors)
        else:
            acted_with[actor2] = set(actors)
        # add each actor to the set pertaining to each
        #   movie, or create a new key and set for them
        if film in movie_actors.keys():
            movie_actors[film] |= set(actors)
        else:
            movie_actors[film] = set(actors)
    # return the transformed data as a tuple of dicts
    return (acted_with, movie_actors)


def acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Takes in the transformed data (a tuple of dicts), and two ints of
    the ids of two actors.
    Returns a bool that says if the actors acted together
    """
    # check if actor 1 is in the set of actors actor 2
    #   has acted with and return the result
    return actor_id_1 in transformed_data[0][actor_id_2]


def actors_with_bacon_number(transformed_data, n):
    """
    Takes in the transformed data (a tuple of dicts), and an int n.
    Returns the set of actor ids of actors with the bacon number n.
    """
    # start with the bacon number set of n=0, which is just Kevin Bacon.
    current_bacon = {4724}
    # create an empty set to keep track of actors that
    #   have ben assigned bacon numbers.
    used_actors = set()
    # loop n times to get the actor set of bacon number n
    for _ in range(n):
        # create a copy of the previous bacon number level
        prev_bacon = current_bacon.copy()
        # create an empty set to keep track of the current bacon number level.
        current_bacon = set()
        # add the previous bacon level to the set of used actors.
        used_actors |= prev_bacon
        # for each actor in the previous bacon number level
        for actor in prev_bacon:
            # add all the actors that the actor has acted with
            current_bacon |= transformed_data[0][actor]
        # remove the actors that have already been assigned bacon numbers
        current_bacon = current_bacon.difference(used_actors)
        # if the current bacon level is empty, all higher levels will also be empty
        # so we can return the empty set
        if len(current_bacon) == 0:
            return current_bacon
    # return the desired bacon number level set
    return current_bacon


def bacon_path(transformed_data, actor_id):
    """
    Takes in the transformed data (a tuple of dicts), and an int actor id.
    Returns a list representing the shortest actor path from Kevin Bacon to the actor.
    """
    # call the actor_path function with Kevin Bacon as the starting actor
    #   and the given actor as the ending actor and return the resulting path
    return actor_path(transformed_data, 4724,
                      lambda p: p == actor_id)


def actor_to_actor_path(transformed_data, actor_id_1, actor_id_2):
    """
    Takes in the transformed data (a tuple of dicts), and two int actor ids.
    Returns a list representing the shortest actor path from
    the first to the second actor.
    """
    # call the actor_path function the first actor as the starting actor
    #   and the second actor as the ending actor and return the resulting path
    return actor_path(transformed_data, actor_id_1,
                      lambda p: p == actor_id_2)


def movie_path(transformed_data, actor_id_1, actor_id_2):
    """
    Takes in the transformed data (a tuple of dicts), and two int actor ids.
    Returns a list representing the shortest movie
    path from the first to the second actor.
    """
    # call the actor_path function the first actor as the starting actor
    #   and the second actor as the ending actor and store the resulting path
    actors_path = actor_path(
        transformed_data, actor_id_1, lambda p: p == actor_id_2)
    # create an empty list to store the movie path
    film_path = []
    # iterates once less than the length of the actor
    #   path (since each movie connects 2 actors)
    for i in range(len(actors_path) - 1):
        # add a movie that the current actor and the next actor have acted together in
        film_path.append(get_movie_acted_together(
            transformed_data, actors_path[i], actors_path[i+1]))
    # return the movie path
    return film_path


def get_movie_acted_together(transformed_data, actor_id_1, actor_id_2):
    """
    Takes in the transformed data (a tuple of dicts), and two int actor ids.
    Returns an int id of a movie that the actors have acted together in.
    """
    # for each movie and actor set in the data
    for movie, actors in transformed_data[1].items():
        # return the movie if both actors acted in it
        if actor_id_1 in actors and actor_id_2 in actors:
            return movie


def actor_path(transformed_data, actor_id_1, goal_test_function):
    """
    Takes in the transformed data (a tuple of dicts), an int actor id and a function.
    Returns a list representing the shortest actor path from the first
    to an actor satisfying the function.
    """
    # start with a path of just the starting actor
    possible_paths = [(actor_id_1,)]
    # create a set of actors that have been checked, starting with the staring actor
    checked_actors = {actor_id_1}
    # if this path satisfies the function, return it
    if goal_test_function(possible_paths[0][-1]):
        return list(possible_paths[0])
    # iterate until there are no more paths to explore
    while len(possible_paths) != 0:
        # remove a path from the list of possible paths and store it
        current_path = possible_paths.pop(0)
        # for each actor that the last actor in the path has acted with
        for neighbor in transformed_data[0][current_path[-1]]:
            # if the neighbor has not been checked, add it to the path
            if neighbor not in checked_actors:
                path = current_path + (neighbor,)
                # if the neighbor satisfies the function, return the path
                if goal_test_function(neighbor):
                    return list(path)
                # if not, add the neighbor to the checked set
                #   and add the path to the possible paths
                else:
                    checked_actors.add(neighbor)
                    possible_paths.append(path)


def actors_connecting_films(transformed_data, film1, film2):
    """
    Takes in the transformed data (a tuple of dicts), and two int movie ids.
    Returns a list representing the shortest actor path connecting the movies
    """
    # store the sets of actors that have acted in each movie
    film1_actors = transformed_data[1][film1]
    film2_actors = transformed_data[1][film2]
    # create an empty set to store the possible paths
    path_set = set()
    # for each actor that has acted in the first movie
    for actor1 in film1_actors:
        # get the path to an actor that acted in the second movie
        path = actor_path(transformed_data, actor1,
                          lambda p: p in film2_actors)
        # add the path to the set of possible paths
        path_set.add(tuple(path))
    # return the shortest path in the list
    return min(list(path_set), key=len)


if __name__ == "__main__":
    with open("resources/large.pickle", "rb") as f:
        largedb = pickle.load(f)
    with open("resources/small.pickle", "rb") as f:
        smalldb = pickle.load(f)
    with open("resources/tiny.pickle", "rb") as f:
        tinydb = pickle.load(f)
    with open("resources/names.pickle", "rb") as f:
        names = pickle.load(f)
    with open("resources/movies.pickle", "rb") as f:
        movies = pickle.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    # print(names["Susan Anspach"])
    # for key in names:
    #     if names[key] == 1043379:
    #         print(key)

    # database = transform_data(smalldb)
    # scott_subiono = names["Scott Subiono"]
    # louise_devar = names["Louise Devar"]
    # charles_berling = names["Charles Berling"]
    # dominique_reymond = names["Dominique Reymond"]
    # print(acted_together(database, scott_subiono, louise_devar))
    # print(acted_together(database, charles_berling, dominique_reymond))

    # database = transform_data(largedb)
    # bn6 = actors_with_bacon_number(database, 6)
    # bn6_names = []
    # for actor_id in bn6:
    #     for key in names:
    #         if names[key] == actor_id:
    #             bn6_names.append(key)
    # print(set(bn6_names))

    # database = transform_data(largedb)
    # tiny_ward = names["Tiny Ward"]
    # tiny_ward_path = bacon_path(database, tiny_ward)
    # tiny_ward_path_names = []
    # for actor_id in tiny_ward_path:
    #     for key in names:
    #         if names[key] == actor_id:
    #             tiny_ward_path_names.append(key)
    # print(tiny_ward_path_names)

    # database = transform_data(largedb)
    # bill_corry = names["Bill Corry"]
    # betsy_palmer = names["Betsy Palmer"]
    # corry_to_palmer_path = actor_to_actor_path(
    #     database, bill_corry, betsy_palmer)
    # corry_to_palmer_path_names = []
    # for actor_id in corry_to_palmer_path:
    #     for key in names:
    #         if names[key] == actor_id:
    #             corry_to_palmer_path_names.append(key)
    # print(corry_to_palmer_path_names)

    # database = transform_data(largedb)
    # curtis_hanson = names["Curtis Hanson"]
    # vjeran_tin_turk = names["Vjeran Tin Turk"]
    # film_path = movie_path(database, curtis_hanson, vjeran_tin_turk)
    # film_path_names = []
    # for movie_id in film_path:
    #     for key in movies:
    #         if movies[key] == movie_id:
    #             film_path_names.append(key)
    # print(film_path_names)

    database = transform_data(largedb)
    print(actors_connecting_films(database, 142416, 44521))
