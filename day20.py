"""
--- Day 20: Infinite Elves and Infinite Houses ---

To keep the Elves busy, Santa has them deliver some presents by hand, door-to-door. He sends them down a street with infinite houses numbered sequentially: 1, 2, 3, 4, 5, and so on.

Each Elf is assigned a number, too, and delivers presents to houses based on that number:

    The first Elf (number 1) delivers presents to every house: 1, 2, 3, 4, 5, ....
    The second Elf (number 2) delivers presents to every second house: 2, 4, 6, 8, 10, ....
    Elf number 3 delivers presents to every third house: 3, 6, 9, 12, 15, ....

There are infinitely many Elves, numbered starting with 1. Each Elf delivers presents equal to ten times his or her number at each house.

So, the first nine houses on the street end up like this:

House 1 got 10 presents.
House 2 got 30 presents.
House 3 got 40 presents.
House 4 got 70 presents.
House 5 got 60 presents.
House 6 got 120 presents.
House 7 got 80 presents.
House 8 got 150 presents.
House 9 got 130 presents.

The first house gets 10 presents: it is visited only by Elf 1, which delivers 1 * 10 = 10 presents. The fourth house gets 70 presents, because it is visited by Elves 1, 2, and 4, for a total of 10 + 20 + 40 = 70 presents.

What is the lowest house number of the house to get at least as many presents as the number in your puzzle input?
"""

import math
from time import sleep

SAMPLE_INPUT = 70

with open("input/day20.txt") as input_file:
    inp = int(input_file.readline())

# part 1: there's not really any input parsing, it's all just math.
# House 1 gets packages only from elf 1 (=10)
# House 2 gets packages from elf 1 + 2 (=30)
# House 4 gets packages from elf 1 + 2 + 4 (=70)
# In general, a house gets packages equal to sum(house_factors) * 10
# Unfortunately calculating factors can very expensive
# One commonly used method is to keep dividing a number by the lowest possible number (1, 2, 3, 4, 5 etc) if that doesn't work or is exhausted, move on the next, etc.
# So a random high number, say house 144, would get packages from:
# (1) 144
# (2) 72 36 18 9
# (3) 48 16 
# (4) 36 9 
# (6) 24 4 
# (8) 18 
# (12)
# which is already a lot of calculations.
# It probably makes sense to store a dict of already calculated factors to reduce amount of computations needed, but this might be impractical; we'll see.

# Also, we can skip ahead quite a bit.
# Say the number of presents is 100000 (so factors totalling 10000). All houses up to 199 cannot have a sum(house_factors).
# That is because the max sum(house_factors) would be sum(n!), in short, n*((n+1)/2)
# Of course, in reality, it's way less. But this could be a good early cutoff point.
# My input is 34000000, so factors totalling 3400000. That means we should start looking at around sqrt(2*340000000/10) which is 2608.

starting_point = int(round(math.sqrt(2*inp/10)))
print(starting_point)

def find_factors(n):
    factors = set()
    # we can stop at sqrt(n) because we get both factors every loop
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    return factors, sum(factors)

def find_all_factor_sums(start, end):
    for i in range(start, end):
        # sleep(0.1)
        factors, sum_factors = find_factors(i)
        # print(i, factors, sum_factors)
        if sum_factors*10 >= inp:
            print(i, factors, sum_factors)
            break


print(find_factors(144))
# find_all_factor_sums(starting_point, inp//10)

"""
--- Part Two ---

The Elves decide they don't want to visit an infinite number of houses. Instead, each Elf will stop after delivering presents to 50 houses. To make up for it, they decide to deliver presents equal to eleven times their number at each house.

With these changes, what is the new lowest house number of the house to get at least as many presents as the number in your puzzle input?
"""

# part 2: more math.
# Now the amount of houses visited changes a lot, and possibly also the number of relevant calculations we should do.
# Let's look at 144 again, factors {1, 2, 3, 4, 36, 6, 72, 8, 9, 12, 144, 48, 18, 16, 24}
# Of these factors, 1 and 2 can be dismissed immediately just by looking at it; the first two elves will already have quit after their 50 houses without ever reaching house 144.
# As a rule, house_number // 50 should be cut off from further calculation
# Since the number of packages per delivery also changed, I rewrote both functions slightly

def find_factors2(n):
    factors = set()
    fixed_factors = set()
    cutoff_point = n // 50
    # print(cutoff_point)
    # we can stop at sqrt(n) because we get both factors every loop
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    for f in factors:
        if f > cutoff_point:
            fixed_factors.add(f)
    return fixed_factors, sum(fixed_factors)

def find_all_factor_sums2(start, end):
    for i in range(start, end):
        # sleep(0.1)
        factors, sum_factors = find_factors2(i)
        # print(i, factors, sum_factors)
        if sum_factors*11 >= inp:
            print(i, factors, sum_factors)
            break


print(find_factors2(144))
find_all_factor_sums2(starting_point, inp//11)
