"""
--- Day 6: Probably a Fire Hazard ---
Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

turn on 0,0 through 999,999 would turn on (or leave on) every light.
toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
After following the instructions, how many lights are lit?
"""

from collections import defaultdict, Counter
import pprint

# part 1 will require some text parsing
with open("input/day6.txt") as input_file:
    inp = input_file.readlines()

# there are 2 kinds of lines, turn off/on and toggle. Parse both kinds of text first
def parse_line(line):
    if line[0:6] == "toggle":
        _, coord1, _, coord2 = line.split()
        mode = "toggle"
    else:
        _, on_off, coord1, _, coord2 = line.split()
        mode = "turn " + on_off
    return {"mode": mode, "coord1": coord1, "coord2": coord2}

# Do a certain action depending on mode
def light_action(mode, low_x, low_y, high_x, high_y):
    for x in range(low_x, high_x+1):
        for y in range(low_y, high_y+1):
            current_coord = (x,y)
            if mode == "turn off":
                coords[current_coord] = False
            elif mode == "turn on":
                coords[current_coord] = True
            # toggle; simply invert the bool; I'm using a defaultdict to circumvent keyerrors for clarity
            else:
                coords[current_coord] = not coords[current_coord]


# all light start turned off
coords = defaultdict(bool)

test_inp = ["turn off 499,499 through 500,500", "toggle 0,0 through 999,0"]

for line in inp:
    current_line = parse_line(line)
    mode = current_line["mode"]
    low_x, low_y = map(int, current_line["coord1"].split(","))
    high_x, high_y = map(int, current_line["coord2"].split(","))
    light_action(mode, low_x, low_y, high_x, high_y)
       
# check if there is a reasonable number of lights, somewhere below 1m (1000x1000 grid)
print(len(coords))
# Count number of lit lights
counts = Counter(coords.values())
print(counts)

"""
--- Part Two ---
You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

turn on 0,0 through 0,0 would increase the total brightness by 1.
toggle 0,0 through 999,999 would increase the total brightness by 2000000.
"""

# part 2: I'll use a defaultdict(int) to keep track of brightness, and a slightly different action algorithm
brightness = defaultdict(int)

def bright_action(mode, low_x, low_y, high_x, high_y):
    for x in range(low_x, high_x+1):
        for y in range(low_y, high_y+1):
            current_coord = (x,y)
            # turn off decreases brightness by 1, to a minimum of zero
            if mode == "turn off":
                if brightness[current_coord] == 0:
                    pass
                else:
                    brightness[current_coord] -= 1
            elif mode == "turn on":
                brightness[current_coord] += 1
            # toggle; increase brightness by 2
            else:
                brightness[current_coord] += 2

for line in inp:
    current_line = parse_line(line)
    mode = current_line["mode"]
    low_x, low_y = map(int, current_line["coord1"].split(","))
    high_x, high_y = map(int, current_line["coord2"].split(","))
    bright_action(mode, low_x, low_y, high_x, high_y)

# print total brightness
print(sum(brightness.values()))
