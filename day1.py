"""
Part 1:
Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

(()) and ()() both result in floor 0.
((( and (()(()( both result in floor 3.
))((((( also results in floor 3.
()) and ))( both result in floor -1 (the first basement level).
))) and )())()) both result in floor -3.
"""

from collections import Counter

with open("input/day1.txt") as inputfile:
    inp = inputfile.readline()

# part 1; we're only interested in the number of left & right brackets, so using a counter makes this trivial
bracket_counts = Counter(inp)
solution1 = bracket_counts["("] - bracket_counts[")"]
print(solution1)

"""
--- Part Two ---
Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""

# part 2: I'll use a variable to track the current floor. Once it reaches -1, we are done.

current_floor = 0
for char in range(len(inp)):
    if inp[char] == "(":
        current_floor += 1
    elif inp[char] == ")":
        current_floor -= 1
    if current_floor == -1:
        # the position is one-based but range is zero-based, so fix the off by one
        print(char+1)
        break
