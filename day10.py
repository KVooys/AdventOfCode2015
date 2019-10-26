"""
--- Day 10: Elves Look, Elves Say ---

Today, the Elves are playing a game called look-and-say. They take turns making sequences by reading aloud the previous sequence and using that reading as the next sequence. For example, 211 is read as "one two, two ones", which becomes 1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as input for the next step. For each step, take the previous value, and replace each run of digits (like 111) with the number of digits (3) followed by the digit itself (1).

For example:

    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?
"""

import re
from time import sleep

with open("input/day10.txt") as input_file:
    inp = input_file.readline()

# part 1: we need a recursive algoritm for the look-and-say translation, and then simply apply it 40 times
# I've made a regex pattern to separate a number into groups of the same numbers
pattern = re.compile(r"(\d)\1{0,}")
def look_and_say(num):
    result = ""
    matches = re.finditer(pattern, num)
    for m in matches:
        # Add the number of occurrences, and then add the value of the number
        result += str(len(m.group()))
        result += str(m.group()[0])
    return result

for i in range(0,50):
    inp = look_and_say(inp)
print(len(inp))

"""
--- Part Two ---

Neat, right? You might also enjoy hearing John Conway talking about this sequence (that's Conway of Conway's Game of Life fame).

Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?

Your puzzle input is still 1113222113.
"""

# part 2 is very easy because of how we did part 1, simply changed 40 to 50 in the loop above
