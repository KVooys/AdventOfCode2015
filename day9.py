"""
--- Day 9: All in a Single Night ---

Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?
"""


import pprint
from collections import defaultdict

with open("input/day9.txt") as input_file:
    inp = input_file.readlines()


test_inp = ["London to Dublin = 464", "London to Belfast = 518", "Dublin to Belfast = 141"]

# part 1: find a good way to display the current information
# Thinking of something like a nested dict:
# London: {Dublin: 464, Belfast: 518 }

def prettify_locations(location1, location2, distance):
    # first add the distance from location1's perspective
    location_dict[location1][location2] = int(distance)

    # same logic from location2's perspective
    location_dict[location2][location1] = int(distance)

# to solve the problem in the travelling salesman way, we need to get the distances between any 2 points in an easy way
# I'll use a defaultdict again, this time with sorted tuples like this:
# {(Dublin, London) : 464,
#  (Belfast, Dublin) : 141}

def store_location_pairs(location1, location2, distance):
    sorted_pair = tuple(sorted((location1, location2)))
    location_pairs[sorted_pair] = int(distance)


location_dict = defaultdict(dict)
location_pairs = defaultdict(tuple)

for line in inp:
    location1, _, location2, _, distance = line.split()
    prettify_locations(location1, location2, distance)
    store_location_pairs(location1, location2, distance)
    
# pprint.pprint(location_dict)
# print(len(location_dict)) 
total_locations = list(location_dict.keys())
print(total_locations)
# there are 8 locations total apparently, and all of them are connected to each other
pprint.pprint(location_pairs)

# we can solve this as a travelling salesman problem, by dividing it recursively into multiple subproblems
def dynamically_solve(current_location, locations_left, distance_so_far):
    # if there is just one more location, simply return the distance to it and exit
    # print("Calculating routes from ", current_location)
    # print("Locations left: ", locations_left)
    if len(locations_left) == 1:
        travel_route = tuple(sorted((current_location, locations_left[0])))
        distance_so_far += location_pairs[travel_route]
        final_distances.append(distance_so_far)
        return

    # if there are still more than 1 location left, solve for each possible next location, with the remainder of locations as locations_left
    else:
        for loc in locations_left:
            new_location_list = locations_left[:]
            new_location_list.remove(loc)
            travel_route = tuple(sorted((current_location, loc)))
            new_distance = distance_so_far + location_pairs[travel_route]
            print(travel_route, new_distance)
            dynamically_solve(loc, new_location_list, new_distance)

# keep track of final distances
final_distances = []

# start all starting locations
# dynamically_solve(total_locations[0], total_locations[1:], 0)
for loc in total_locations:
    location_list = total_locations[:]
    location_list.remove(loc)
    dynamically_solve(loc, location_list, 0)

print(final_distances, min(final_distances))

"""
--- Part Two ---

The next year, just to show off, Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants, and he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?
"""

# part 2 is trivial because of the way I did part 1!
print(max(final_distances))