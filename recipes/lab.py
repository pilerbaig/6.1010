"""
6.1010 Spring '23 Lab 4: Recipes
"""

import pickle
import sys

sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!


def make_recipe_book(recipes):
    """
    Given recipes, a list containing compound and atomic food items, make and
    return a dictionary that maps each compound food item name to a list
    of all the ingredient lists associated with that name.
    """
    # create a dictionary to store the recipe book
    recipe_dict = {}
    # for reach compound recipe
    for recipe in recipes:
        if recipe[0] == "compound":
            # add the ingredients of the compound recipe
            #   to the dictionary key of the item
            recipe_dict.setdefault(recipe[1], []).append(recipe[2])
    # return the recipe book
    return recipe_dict


def make_atomic_costs(recipes):
    """
    Given a recipes list, make and return a dictionary mapping each atomic food item
    name to its cost.
    """
    # create a new dictionary to store the atomic items and costs
    cost_dict = {}
    # for each atomic recipe
    for recipe in recipes:
        if recipe[0] == "atomic":
            # map the amount to the atomic item
            cost_dict[recipe[1]] = recipe[2]
    # return the new dictionary
    return cost_dict


def lowest_cost(recipes, food_item, forbidden_list=None):
    """
    Given a recipes list and the name of a food item, return the lowest cost of
    a full recipe for the given food item.
    """
    # create an empty forbidden list if no forbidden list is passed in
    if forbidden_list is None:
        forbidden_list = []
    # create the recipe book and atomic costs dictionaries
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    # remove the forbidden items from the atomic costs and recipe book
    for forbidden_ingredient in forbidden_list:
        if forbidden_ingredient in recipe_book:
            del recipe_book[forbidden_ingredient]
        elif forbidden_ingredient in atomic_costs:
            del atomic_costs[forbidden_ingredient]

    def lowest_cost_helper(food_item):
        """
        Recursive helper function for the lowest_cost function
        """
        # base case: return the cost of the item if it is atomic
        if food_item in atomic_costs:
            return atomic_costs[food_item]
        # if the item is valid
        elif food_item in recipe_book:
            # get the recipe of the item
            food_item_recipe = recipe_book[food_item]
            # create an empty list to store the costs of each possible recipe
            cost_list = []
            # for each potential recipe for the item
            for potential_recipe in food_item_recipe:
                # initialize the cost to 0
                total_cost = 0
                # for each ingredient in the recipe
                for ingredient in potential_recipe:
                    # get the lowest cost for that ingredient
                    ingredient_cost = lowest_cost_helper(ingredient[0])
                    # if None is returned, the item is invalid, so give None cost
                    if ingredient_cost is None or total_cost is None:
                        total_cost = None
                    else:
                        # add the cost of the ingredients to the cost of the recipe
                        total_cost += ingredient[1] * ingredient_cost
                # add the total cost for the potential recipe to the list
                cost_list.append(total_cost)
            # create a cost list without the impossible recipes
            cost_list_no_none = []
            for cost in cost_list:
                if cost is not None:
                    cost_list_no_none.append(cost)
            # if there is no possible cost, return None
            if not cost_list_no_none:
                return None
            # if not, return the minimum cost
            return min(cost_list_no_none)
        # return None if the item is not a possible item
        else:
            return None
    # start the recursion
    return lowest_cost_helper(food_item)


def scale_recipe(flat_recipe, n):
    """
    Given a dictionary of ingredients mapped to quantities needed, returns a
    new dictionary with the quantities scaled by n.
    """
    # create a new dictionary to store the scaled recipe
    new_recipe = {}
    # if the recipe passed in is None, return None
    if flat_recipe is None:
        return None
    # add each ingredient and amount scaled by the scaling
    #   factor to the dictionary
    for ingredient in flat_recipe:
        new_recipe[ingredient] = flat_recipe[ingredient] * n
    # return the new recipe
    return new_recipe


def make_grocery_list(flat_recipes):
    """
    Given a list of flat_recipe dictionaries that map food items to quantities,
    return a new overall 'grocery list' dictionary that maps each ingredient name
    to the sum of its quantities across the given flat recipes.

    For example,
        make_grocery_list([{'milk':1, 'chocolate':1}, {'sugar':1, 'milk':2}])
    should return:
        {'milk':3, 'chocolate': 1, 'sugar': 1}
    """
    # create a new recipe to store the grocery list
    new_recipe = {}
    # for each ingredient in each recipe
    for flat_recipe in flat_recipes:
        for ingredient in flat_recipe:
            # add the amount of the ingredient to the total amount of
            #   that ingredient (start at 0 if not present)
            new_recipe[ingredient] = new_recipe.setdefault(
                ingredient, 0) + flat_recipe[ingredient]
    # return the new recipe
    return new_recipe


def price_grocery_list(grocery_list, atomic_costs):
    """
    Given a dictionary grocery list mapping ingredients to quanitities and a
    dictionary mapping atomic ingredients to their costs, returns the total
    price of all the items in the grocery list
    """
    # initialize the price to 0
    price = 0
    # add the price of each ingredient times the quantity to the cost
    for ingredient in grocery_list:
        price += atomic_costs[ingredient] * grocery_list[ingredient]
    # return the cost
    return price


def cheapest_flat_recipe(recipes, food_item, forbidden_list=None):
    """
    Given a recipes list and the name of a food item, return a dictionary
    (mapping atomic food items to quantities) representing the cheapest full
    recipe for the given food item.

    Returns None if there is no possible recipe.
    """
    # create an empty forbidden list if no forbidden list is passed in
    if forbidden_list is None:
        forbidden_list = []
    # create the recipe book and atomic costs dictionaries
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    # remove the forbidden items from the atomic costs and recipe book
    for forbidden_ingredient in forbidden_list:
        if forbidden_ingredient in recipe_book:
            del recipe_book[forbidden_ingredient]
        elif forbidden_ingredient in atomic_costs:
            del atomic_costs[forbidden_ingredient]

    def cheapest_flat_helper(food_item):
        """
        Recursive helper function for the cheapest_flat_recipes function
        """
        # base case: if the food item is atomic, return the
        #   recipe of the atomic item
        if food_item in atomic_costs:
            return {food_item: 1}
        # recursive case
        elif food_item in recipe_book:
            # get the lowest cost of the recipe as the target
            target_cost = lowest_cost(recipes, food_item, forbidden_list)
            # for each possible recipe for the item
            current_recipes = recipe_book[food_item]
            for potential_recipe in current_recipes:
                # create a list to store the ingredient recipes
                recipe_list = []
                # store the recipe for each ingredient in the recipe list
                for ingredient in potential_recipe:
                    new_recipe = scale_recipe(
                        cheapest_flat_helper(ingredient[0]), ingredient[1])
                    # only add it if the recipe exists
                    if new_recipe is not None:
                        recipe_list.append(new_recipe)
                # make a grocery list to get the flat recipe of the recipe list
                grocery_list = make_grocery_list(recipe_list)
                # get the cost of the grocery list
                grocery_cost = price_grocery_list(grocery_list, atomic_costs)
                # return the grocery list if it is the right (lowest) cost
                if grocery_cost == target_cost:
                    return grocery_list
    # start the recursion
    return cheapest_flat_helper(food_item)


def ingredient_mixes(flat_recipes):
    """
    Given a list of lists of dictionaries, where each inner list represents all
    the flat recipes make a certain ingredient as part of a recipe, compute all
    combinations of the flat recipes.
    """
    # create a list to store each combination mix
    mixes = []
    # base case: if the recipe has one item, return the dict inside
    if len(flat_recipes) == 1:
        return flat_recipes[0]
    # recursive case
    else:
        # for each ingredient and the next ingredients
        for ingredient in flat_recipes[0]:
            for next_ingredients in ingredient_mixes(flat_recipes[1:]):
                # make a grocery list of the two lists
                combination = make_grocery_list([ingredient, next_ingredients])
                # combine the mixes list and the new combination
                mixes.extend([combination])
    # return the list
    return mixes


def scale_list(recipe_list, n):
    """
    Given a list of dictionaries of ingredients mapped to quantities needed, returns a
    new list of dictionaries with the quantities scaled by n.
    """
    # create a list to store the scaled dictionaries
    new_list = []
    # for each dictionary, scale it and add it to the new list
    for dictionary in recipe_list:
        new_list.append(scale_recipe(dictionary, n))
    # return the new list
    return new_list


def all_flat_recipes(recipes, food_item, forbidden_list=None):
    """
    Given a list of recipes and the name of a food item, produce a list (in any
    order) of all possible flat recipes for that category.

    Returns an empty list if there are no possible recipes
    """
    # create an empty forbidden list if no forbidden list is passed in
    if forbidden_list is None:
        forbidden_list = []
    # create the recipe book and atomic costs dictionaries
    recipe_book = make_recipe_book(recipes)
    atomic_costs = make_atomic_costs(recipes)
    # remove the forbidden items from the atomic costs and recipe book
    for forbidden_ingredient in forbidden_list:
        if forbidden_ingredient in recipe_book:
            del recipe_book[forbidden_ingredient]
        elif forbidden_ingredient in atomic_costs:
            del atomic_costs[forbidden_ingredient]

    def all_flat_helper(food_item):
        """
        Recursive helper function for the all_flat_recipes function
        """
        # create a list to store all the flat lists
        all_flats = []
        # base case: if the food item is atomic, return a list
        #   containing that item
        if food_item in atomic_costs:
            return [{food_item: 1}]
        # recursive case
        elif food_item in recipe_book:
            # get the lowest cost of the recipe as the target
            current_recipes = recipe_book[food_item]
            for potential_recipe in current_recipes:
                # create a list to store the ingredient recipes
                recipe_list = []
                # store the recipe for each ingredient in the recipe list
                for ingredient in potential_recipe:
                    # get the recipe of the scaled flat recipes of the ingredient
                    new_recipe = scale_list(
                        all_flat_helper(ingredient[0]), ingredient[1])
                    # if the new recipe exists, add it to the list
                    if new_recipe is not None:
                        recipe_list.append(new_recipe)
                # get a list of the combinations of the items in the list
                mixes = ingredient_mixes(recipe_list)
                # add the combinations to the list of all flat lists
                all_flats.extend(mixes)
        # return the list of flat lists
        return all_flats
    # start the recursion
    return all_flat_helper(food_item)


if __name__ == "__main__":
    # load example recipes from section 3 of the write-up
    with open("test_recipes/example_recipes.pickle", "rb") as f:
        example_recipes = pickle.load(f)
    # you are free to add additional testing code here!

    # example_book = make_recipe_book(example_recipes)
    # example_cost = make_atomic_costs(example_recipes)
    # length_list = []
    # multiple_recipe_count = sum(
    #     [1 for recipe in example_book.values() if len(recipe) == 1])
    # total_cost_one_each = sum([cost
    #                           for cost in example_cost.values()])
    # print(multiple_recipe_count)
    # print(total_cost_one_each)
    # dairy_recipes = [
    #     ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
    #     ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    #     ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
    #     ('atomic', 'milking stool', 5),
    #     ('atomic', 'cutting-edge laboratory', 1000),
    #     ('atomic', 'time', 10000),
    #     ('atomic', 'cow', 100),
    # ]
    # soup = {"carrots": 5, "celery": 3, "broth": 2,
    #         "noodles": 1, "chicken": 3, "salt": 10}
    # carrot_cake = {"carrots": 5, "flour": 8,
    #                "sugar": 10, "oil": 5, "eggs": 4, "salt": 3}
    # bread = {"flour": 10, "sugar": 3, "oil": 3, "yeast": 15, "salt": 5}
    # grocery_list = [soup, carrot_cake, bread]
    # print(make_grocery_list(
    #    [{'milk': 1, 'chocolate': 1}, {'sugar': 1, 'milk': 2}]))
    # print(make_grocery_list(grocery_list))
    # print(cheapest_flat_recipe(dairy_recipes, 'cheese', ['cow']))
    # cake_recipes = [{"cake": 1}, {"gluten free cake": 1}]
    # icing_recipes = [{"vanilla icing": 1}, {"cream cheese icing": 1}]
    # print(ingredient_mixes([cake_recipes, icing_recipes]))
    # print(all_flat_recipes(example_recipes, 'burger'))
    # for i in all_flat_recipes(example_recipes, 'burger', ('milk',)):
    #     print(i)
    pass
