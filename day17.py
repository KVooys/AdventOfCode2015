"""
--- Day 17: No Such Thing as Too Much ---

The elves bought too much eggnog again - 150 liters this time. To fit it all into your refrigerator, you'll need to move it into smaller containers. You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters. If you need to store 25 liters, there are four ways to do it:

    15 and 10
    20 and 5 (the first 5)
    20 and 5 (the second 5)
    15, 5, and 5

Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?
"""

from collections import Counter
from itertools import combinations
import pprint

with open("input/day17.txt") as input_file:
    inp = input_file.readlines()

# part 1: input parsing
# Add all the container sizes to a list
container_list = [int(line) for line in inp]

print(container_list)

# It would be efficient to store partial answers (like 100 = 50 + 44 + 6), but that makes it more difficult to see if we already have a container in use.
# Also it could lock us out of any amount of combinations if there are more than 1 way to make a partial answer

# At the very least we should only try finding combinations that make sense, drastically cutting down on the amount of possibilities
# from the size of the containers, we can see we need at least 4 containers to make 150, and at most 10
# so we only have to calculate combinations of length 4-10 out of the list
all_combinations = [c for i in range(4, 11) for c in combinations(container_list, i) if sum(c) == 150]
# pprint.pprint(all_combinations)
print(len(all_combinations))

"""
--- Part Two ---

While playing with all the containers in the kitchen, another load of eggnog arrives! The shipping and receiving department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you fill that number of containers and still hold exactly 150 litres?

In the example above, the minimum number of containers was two. There were three ways to use that many containers, and so the answer there would be 3.
"""
# We can use the same combination logic, but only looking at a certain number of containers. 
# From looking at the input, we already knew the minimum number of containers is 4, so a check is unnecessary
# If the input were a lot larger, we'd have to loop over range(0, len(input)) to see where the first possibility occurs and then count those
count = 0
for c in all_combinations:
    if len(c) == 4:
        count += 1
    else:
        break
print(count)
