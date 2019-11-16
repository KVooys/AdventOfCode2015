"""
--- Day 18: Like a GIF For Your Yard ---

After the million lights incident, the fire code has gotten stricter: now, at most ten thousand lights are allowed. You arrange them in a 100x100 grid.

Never one to let you down, Santa again mails you instructions on the ideal lighting configuration. With so few lights, he says, you'll have to resort to animation.

Start by setting your lights to the included initial configuration (your puzzle input). A # means "on", and a . means "off".

Then, animate your grid in steps, where each step decides the next configuration based on the current one. Each light's next state (either on or off) depends on its current state and the current states of the eight lights adjacent to it (including diagonals). Lights on the edge of the grid might have fewer than eight neighbors; the missing ones always count as "off".

For example, in a simplified 6x6 grid, the light marked A has the neighbors numbered 1 through 8, and the light marked B, which is on an edge, only has the neighbors marked 1 through 5:

1B5...
234...
......
..123.
..8A4.
..765.

The state a light should have next is based on its current state (on or off) plus the number of neighbors that are on:

    A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.

All of the lights update simultaneously; they all consider the same current state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid:

Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......

After 4 steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?
"""

sample_input = """
.#.#.#
...##.
#....#
..#...
#.#..#
####..
""".split("\n")


from collections import defaultdict, Counter
import pprint

with open("input/day18.txt") as input_file:
    inp = input_file.readlines()

# Save all light states in a grid of booleans, on = True, off = False

def parse(lines):
    for line_number, line in enumerate(lines):
        # print(line_number, line)
        grid_dict[line_number] = [char == "#" for char in line]

def get_coord(x, y):
    # This function is needed to deal with edge cases; chars that are off the edge of the grid
    # There are two ways a char can be off the grid: 
    # it has negative value for a coordinate
    # or it has a value greater than the grid_size
    
    # part 2 code, all 4 corners are always on:
    if (x, y) == (0, 0) or (x, y) == (0, grid_size-1) or (x, y) == (grid_size-1, 0) or (x, y) == (grid_size-1, grid_size-1):
        return True

    if x >= grid_size or x < 0 or y >= grid_size or y < 0:
        return False
    else:
        return grid_dict[y][x]

def step_light(x, y):
    # Steps to take to check a single light's new state

    # A character has at most 8 neighbours, which are the coordinates around it. Get their values as a list
    # y -1: -1 0 1
    # y 0:  -1 # 1
    # y 1:  -1 0 1

    # part 2 code, all 4 corners are always on:
    if (x, y) == (0, 0) or (x, y) == (0, grid_size-1) or (x, y) == (grid_size-1, 0) or (x, y) == (grid_size-1, grid_size-1):
        return True

    current_light = grid_dict[y][x]
    current_neighbours = [
        get_coord(x-1, y-1), get_coord(x, y-1), get_coord(x+1, y-1),
        get_coord(x-1, y), get_coord(x+1, y),
        get_coord(x-1, y+1), get_coord(x, y+1), get_coord(x+1, y+1)
    ]

    count = Counter(current_neighbours)[True]
    # print("Current", (x,y), count, current_light)
    #   A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
    if current_light:
        if count == 2 or count == 3:
            return True
        else:
            return False

    #   A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
    else:
        if count == 3:
            return True
        else:
            return False

def step_grid(grid):
    # to step the entire grid, we simply make a new one by using the step_light on each coordinate
    new_grid = defaultdict(list)
    for y in range(0, grid_size):
        line_list = []
        for x in range(0, grid_size):
            line_list.append(step_light(x, y))
        new_grid[y] = line_list
    return new_grid

grid_dict = defaultdict(list)
# parse(sample_input[1:7])
parse(inp)

pprint.pprint(grid_dict)
grid_size = 100

for i in range(100):
    grid_dict = step_grid(grid_dict)
    # pprint.pprint(grid_dict)
    total = 0
    for k, v in grid_dict.items():
        total += Counter(v)[True]
    print(i, total)

"""
--- Part Two ---

You flip the instructions over; Santa goes on to point out that this is all just an implementation of Conway's Game of Life. At least, it was, until you notice that something's wrong with the grid of lights you bought: four lights, one in each corner, are stuck on and can't be turned off. The example above will actually run like this:

Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#

After 5 steps, this example now has 17 lights on.

In your grid of 100x100 lights, given your initial configuration, but with the four corners always in the on state, how many lights are on after 100 steps?
"""

# part 2 is an easy change to the get_coord and the step_light code, simply making the corner checks always return True