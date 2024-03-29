import lab
dairy_recipes = [
    ('compound', 'milk', [('cow', 2), ('milking stool', 1)]),
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
    ('atomic', 'milking stool', 5),
    ('atomic', 'cutting-edge laboratory', 1000),
    ('atomic', 'time', 10000),
    ('atomic', 'cow', 100),
]


forbidden_list = []
recipe_book = lab.make_recipe_book(dairy_recipes)
atomic_costs = lab.make_atomic_costs(dairy_recipes)
for forbidden_ingredient in forbidden_list:
    if forbidden_ingredient in recipe_book:
        del recipe_book[forbidden_ingredient]
    elif forbidden_ingredient in atomic_costs:
        del atomic_costs[forbidden_ingredient]


def cheapest_flat_helper(food_item):
    if food_item in atomic_costs:
        return {food_item: 1}
    elif food_item in recipe_book:
        current_recipes = recipe_book[food_item]
        for potential_recipe in current_recipes:
            recipe_list = []
            for ingredient in potential_recipe:
                recipe_list.append(lab.scale_recipe(
                    cheapest_flat_helper(ingredient[0]), ingredient[1]))
            return lab.make_grocery_list(recipe_list)


print(cheapest_flat_helper('milk'))
