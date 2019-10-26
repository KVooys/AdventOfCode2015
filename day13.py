"""
--- Day 13: Knights of the Dinner Table ---

In years past, the holiday feast with your family hasn't gone so well. Not everyone gets along! This year, you resolve, will be different. You're going to find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their happiness would increase or decrease if they were to find themselves sitting next to each other person. You have a circular table that will be just big enough to fit everyone comfortably, and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned, and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.

Then, if you seat Alice next to David, Alice would lose 2 happiness units (because David talks so much), but David would gain 46 happiness units (because Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83

After trying every other seating arrangement in this hypothetical scenario, you find that this one is the most optimal, with a total change in happiness of 330.

What is the total change in happiness for the optimal seating arrangement of the actual guest list?
"""

import pprint
from itertools import permutations

with open("input/day13.txt") as input_file:
    inp = input_file.readlines()

# part 1: the input is not that long, so a naive solution might be possible.
# That would require (num_people)! possible arrangements. As there are 8 people in the input, that's 40320.
# Because of the circular form of the arrangement, there will be much overlap in the solutions
# for instance, (ABCD) is essentially the same as (BCDA) etc

# First decide on data structure
# We have to consider both happiness changes per person
# in the example, A next to B would give A +54, but B next to A would give B +83; the sum of happiness is what matters here
# First way I can think of to represent that:
# {
# A: {B: 54, C: -79, D: -2},
# B: {A: 83, C: -7, D: -63},
# C: {A: -63, B: 60, D: 55},
# D: {A: 46, B: -7, C: 41}
# }
# Now to calculate the first possibility, ABCD:
# calc(AB): A[B] + B[A]
# calc(BC): B[C] + C[B]
# calc(CD): C[D] + D[C]
# figure out that the final pair is the first + last seat: AD
# calc(AD): A[D] + D[A]
# and sum all the pairs


# format: Alice would gain 54 happiness units by sitting next to Bob 
# put the relevant items into the dict
def parse_input(line):
    name1, _, gain_or_lose, happiness, _, _, _, _, _, _, name2 = line.split()
    # remove dot at the end of the line
    name2 = name2[:-1]
    print(name1, gain_or_lose, happiness, name2)
    if name1 not in happiness_dict:
        happiness_dict[name1] = {}
    if gain_or_lose == "gain":
        happiness_dict[name1][name2] = int(happiness)
    elif gain_or_lose == "lose":
        happiness_dict[name1][name2] = -1 * int(happiness)

# naively return all arrangements (there will be functional duplicates)
def find_arrangements(names):
    return permutations(names, len(names))

# given 2 people are next to each other, calculate the impact on total happiness
def calculate_happiness(name1, name2):
    return happiness_dict[name1][name2] + happiness_dict[name2][name1]

def sum_happiness_per_arrangement(arrangement, size):
    current_happiness = 0
    # loop over pairs in circle
    for i in range(size-1):
        current_happiness += calculate_happiness(arrangement[i], arrangement[i+1])
    # add the first and last people in the circle
    current_happiness += calculate_happiness(arrangement[0], arrangement[size-1])
    return current_happiness


happiness_dict = {}

for line in inp:
    parse_input(line)

pprint.pprint(happiness_dict)
circle_size = len(happiness_dict)


# solution to part 1
# keep track of max possible happiness
# best_happiness = -10000
# for arrangement in find_arrangements(happiness_dict.keys()):
#     this_happiness = sum_happiness_per_arrangement(arrangement, circle_size)
#     best_happiness = max(this_happiness, best_happiness)

# print(best_happiness)

"""
--- Part Two ---

In all the commotion, you realize that you forgot to seat yourself. At this point, you're pretty apathetic toward the whole thing, and your happiness wouldn't really go up or down regardless of who you sit next to. You assume everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve you a score of 0.

What is the total change in happiness for the optimal seating arrangement that actually includes yourself?
"""

# first add yourself to the dict
happiness_dict["You"] = {}
for key in happiness_dict:
    happiness_dict["You"][key] = 0
    happiness_dict[key]["You"] = 0

# then solve in the same way as before
circle_size = len(happiness_dict)
# keep track of max possible happiness
best_happiness = -10000
for arrangement in find_arrangements(happiness_dict.keys()):
    this_happiness = sum_happiness_per_arrangement(arrangement, circle_size)
    best_happiness = max(this_happiness, best_happiness)

print(best_happiness)