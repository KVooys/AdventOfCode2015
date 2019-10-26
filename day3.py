"""
Part 1:
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.
"""

# Part 1: I'm going to overengineer this a little bit, and make a dataclass for representing coordinates (x,y) because it seems neater
from dataclasses import dataclass
from collections import defaultdict
import pprint

@dataclass
class Coordinate:
    x: int
    y: int

    def tuple(self):
        return (self.x,self.y)


print(Coordinate(0,0).tuple())
with open("input/day3.txt") as input_file:
    inp = input_file.readline()

# Now we'll do some map traversal, using a dict to store frequencies of coordinates passed. We'll start by storing the base coordinate
freq_dict = defaultdict(int)
freq_dict[Coordinate(0,0).tuple()] = 1

x = 0
y = 0
for char in inp:
    if char == "<":
        x -= 1
    if char == ">":
        x += 1
    if char == "^":
        y += 1
    if char == "v":
        y -= 1
    freq_dict[Coordinate(x,y).tuple()] += 1

print(len(freq_dict))

"""
--- Part Two ---
The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
"""

# we can use the same method, but use a santa_x & y and a robo_x & y to keep track of both, and the first house starts with 2 presents
freq_dict = defaultdict(int)
freq_dict[Coordinate(0,0).tuple()] = 2

santa_x = 0
santa_y = 0
robo_x = 0
robo_y = 0
total = 0
for char in inp:
    if total % 2 == 0:
        if char == "<":
            robo_x -= 1
        if char == ">":
            robo_x += 1
        if char == "^":
            robo_y += 1
        if char == "v":
            robo_y -= 1
        freq_dict[Coordinate(robo_x,robo_y).tuple()] += 1
    else:
        if char == "<":
            santa_x -= 1
        if char == ">":
            santa_x += 1
        if char == "^":
            santa_y += 1
        if char == "v":
            santa_y -= 1
        freq_dict[Coordinate(santa_x,santa_y).tuple()] += 1
    total += 1

print(len(freq_dict))