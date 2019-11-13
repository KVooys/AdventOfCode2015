"""
--- Day 16: Aunt Sue ---
Your Aunt Sue has given you a wonderful gift, and you'd like to send her a thank you card. However, there's a small problem: she signed it "From, Aunt Sue".

You have 500 Aunts named "Sue".

So, to avoid sending the card to the wrong person, you need to figure out which Aunt Sue (which you conveniently number 1 to 500, for sanity) gave you the gift. You open the present and, as luck would have it, good ol' Aunt Sue got you a My First Crime Scene Analysis Machine! Just what you wanted. Or needed, as the case may be.

The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few specific compounds in a given sample, as well as how many distinct kinds of those compounds there are. According to the instructions, these are what the MFCSAM can detect:

children, by human DNA age analysis.
cats. It doesn't differentiate individual breeds.
Several seemingly random breeds of dog: samoyeds, pomeranians, akitas, and vizslas.
goldfish. No other kinds of fish.
trees, all in one group.
cars, presumably by exhaust or gasoline or something.
perfumes, which is handy, since many of your Aunts Sue wear a few kinds.
In fact, many of your Aunts Sue have many of these. You put the wrapping from the gift into the MFCSAM. It beeps inquisitively at you a few times and then prints out a message on ticker tape:

children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
You make a list of the things you can remember about each Aunt Sue. Things missing from your list aren't zero - you simply don't remember the value.

What is the number of the Sue that got you the gift?
"""

import re 

with open("input/day16.txt") as input_file:
    inp = input_file.readlines()

# the detected values from the intro
known_values = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

# part 1 & input parsing
# a line from the list of Sues looks like this:
# Sue 1: goldfish: 9, cars: 0, samoyeds: 9
# Each line has exactly 1 aunt, the ID at the start
# and has exactly 3 attributes and their numeric values, in an undefined order

pattern = r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)"

for line in inp:
    m = re.match(pattern, line)
    aunt_id, attr1, value1, attr2, value2, attr3, value3 = m.groups()
    value1, value2, value3 = map(int, [value1, value2, value3])

    # Now for some simple matching logic
    # for every defined attribute, check if it matches the known value
    pairs = [(attr1, value1), (attr2, value2), (attr3, value3)]
    if all([known_values[k] == v for k, v in pairs]):
        print(aunt_id)



"""
--- Part Two ---
As you're about to send the thank you note, something in the MFCSAM's instructions catches your eye. Apparently, it has an outdated retroencabulator, and so the output from the machine isn't exact values - some of them indicate ranges.

In particular, the cats and trees readings indicates that there are greater than that many (due to the unpredictable nuclear decay of cat dander and tree pollen), while the pomeranians and goldfish readings indicate that there are fewer than that many (due to the modial interaction of magnetoreluctance).

What is the number of the real Aunt Sue?
"""
# part 2: Unfortunately this means we have to redo the matching logic.
# No fancy all() check this time =(
# but with simple conditions this is still a very quick check

for line in inp:
    m = re.match(pattern, line)
    # print(m.groups())
    aunt_id, attr1, value1, attr2, value2, attr3, value3 = m.groups()
    value1, value2, value3 = map(int, [value1, value2, value3])
    pairs = [(attr1, value1), (attr2, value2), (attr3, value3)]
    matched_attrs = 0
    for k, v in pairs:
        if k in ("cats", "trees"):
            # continue if the value is greater than the known value
            if v > known_values[k]:
                matched_attrs += 1
        elif k in ("pomeranians", "goldfish"):
            # continue if the value is smaller than the known value
            if v < known_values[k]:
                matched_attrs += 1
        else:
            if v == known_values[k]:
                matched_attrs += 1
    if matched_attrs == 3:
        print(aunt_id)


