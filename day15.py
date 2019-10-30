"""
--- Day 15: Science for Hungry People ---

Today, you set out on the task of perfecting your milk-dunking cookie recipe. All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a list of the remaining ingredients you could use to finish the recipe (your puzzle input) and their properties per teaspoon:

    capacity (how well it helps the cookie absorb milk)
    durability (how well it keeps the cookie intact when full of milk)
    flavor (how tasty it makes the cookie)
    texture (how it improves the feel of the cookie)
    calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately, and you have to be accurate so you can reproduce your results in the future. The total score of a cookie can be found by adding up each of the properties (negative totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon (because the amounts of each ingredient must add up to 100) would result in a cookie with the following properties:

    A capacity of 44*-1 + 56*2 = 68
    A durability of 44*-2 + 56*3 = 80
    A flavor of 44*6 + 56*-2 = 152
    A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in a total score of 62842880, which happens to be the best score possible given these ingredients. If any properties had produced a negative total, it would have instead become zero, causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?
"""

import re
import pprint
from dataclasses import dataclass
from itertools import permutations

SAMPLE_INPUT = ["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
                "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]


with open("input/day15.txt") as input_file:
    inp = input_file.readlines()

# part 1:  

@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

def parse_line(lines):
    for line in lines:
        match = re.match(pattern, line)
        name = match.groups()[0]
        capacity, durability, flavor, texture, calories = [int(m) for m in match.groups()[1:]]
        ingredient_dict[name] = Ingredient(name, capacity, durability, flavor, texture, calories)

# apparently all ingredients have values for all 5 properties, and all of them can be negative as well, so parsing them is easy
pattern = r"(\w+): capacity (-{0,1}\d+), durability (-{0,1}\d+), flavor (-{0,1}\d+), texture (-{0,1}\d+), calories (-{0,1}\d+)"
ingredient_dict = {}

# so now we know the properties of the cookies, let's calculate the total score any selection can give
# input for the score is a teaspoon dict which sum is equal to 100 and which length is the number of cookies

def total_score(ingredients, teaspoons):
    total_capacity = 0
    total_durability = 0
    total_flavor = 0
    total_texture = 0
    total_calories = 0

    for ingredient in ingredients.values():
        num_teaspoons = teaspoons[ingredient.name]
        total_capacity += ingredient.capacity * num_teaspoons
        total_durability += ingredient.durability * num_teaspoons
        total_flavor += ingredient.flavor * num_teaspoons
        total_texture += ingredient.texture * num_teaspoons
        # part 2
        total_calories += ingredient.calories * num_teaspoons
    
    # part 2
    if total_calories != 500:
        return 0

    # take into account that any negative property will cause the cookie to score 0
    if total_capacity <= 0:
        return 0
    if total_durability <= 0:
        return 0
    if total_flavor <= 0:
        return 0
    if total_texture <= 0:
        return 0
    
    return total_capacity * total_durability * total_flavor * total_texture

# testing for sample input
# parse_line(SAMPLE_INPUT)
# print(ingredient_dict)
# teaspoons = {"Butterscotch": 44, "Cinnamon": 56}
# print(total_score(ingredient_dict, teaspoons))

# now to find the best combination. 
# We check every quantity of every ingredient where the sum is 100
# with only 2 ingredients this is easy, but with 4 it becomes more messy; apparently there's 161664 permutations. Should still be quick enough since counting the score is so cheap.


def find_ingredient_permutations(num_ingredients):
    nums = range(0, 101)
    return [p for p in permutations(nums, num_ingredients) if sum(p) == 100]
        
parse_line(inp)
print(ingredient_dict)
teaspoons = {}
max_score = 0

for p in find_ingredient_permutations(len(ingredient_dict)):
    teaspoons["Sprinkles"] = p[0]
    teaspoons["Butterscotch"] = p[1]
    teaspoons["Chocolate"] = p[2]
    teaspoons["Candy"] = p[3]
    this_score = total_score(ingredient_dict, teaspoons)
    print(p, this_score)
    max_score = max(max_score, this_score)
print(max_score)


"""
--- Part Two ---

Your cookie recipe becomes wildly popular! Someone asks if you can make another recipe that has exactly 500 calories per cookie (so they can use it as a meal replacement). Keep the rest of your award-winning process the same (100 teaspoons, same ingredients, same scoring system).

For example, given the ingredients above, if you had instead selected 40 teaspoons of butterscotch and 60 teaspoons of cinnamon (which still adds to 100), the total calorie count would be 40*8 + 60*3 = 500. The total score would go down, though: only 57600000, the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make with a calorie total of 500?
"""

# we can do this in a similar way as part 1, so I added another condition that sets score to 0 for calories not matching 500
# This actually makes part 2 slightly faster than part 1.
# Alternatively, what you could do is make new permutations that take into account the sum of the calories, but this requires backreferencing the Ingredient object every time, so I thought it'd be slower.
# Since so many results are 0 (because they're not 500 calories) this might actually be faster in the end.
