"""
--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

For example:

    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?
"""

import json
import pprint 

with open("input/day12.txt") as input_file:
    json_list = json.load(input_file)


# part 1: look into the input file a bit; it's actually a list of nested JSON objects

# print(len(json_list))
# print(type(json_list))
# for json in json_list:
#     pprint.pprint(json)
#     print(type(json))
#     break


# I'm going a bit overboard here, but writing a function to traverse the JSON object seems fun
def traverse_json(obj):
    print("Traversing ", obj)
    if type(obj) == dict:
        # print("obj is dict")
        for k, v in obj.items():
            # the keys are never numbers, so ignore those
            traverse_json(v)
    elif type(obj) == list:
        # print("obj is list")
        for item in obj:
            traverse_json(item)
    elif type(obj) == int:
        # print("obj is int")
        num_list.append(obj)
    # we can disregard strings; they will not contain numbers according to the description
    else:
        pass
    

test_list = [{"a":2,"b":4}, [1,2,3]]

# solution to part 1:
# num_list = []
# traverse_json(json_list)
# print(sum(num_list))

"""
--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything red.

Ignore any object (and all of its children) which has any property with the value "red". Do this only for objects ({...}), not arrays ([...]).

    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.

"""

# part 2: this is an easy change to the traversal function because of the way I solved part 1
# simply check all the dict items for "red" before traversing further

def traverse_json__and_disregard_red(obj):
    print("Traversing ", obj)
    if type(obj) == dict:
        if ('red' in obj or 'red' in obj.values()):
            pass
        else:
            for k, v in obj.items():
                # the keys are never numbers, so ignore those
                traverse_json__and_disregard_red(v)
                    
    elif type(obj) == list:
        for item in obj:
            traverse_json__and_disregard_red(item)
    elif type(obj) == int:
        num_list.append(obj)
    # we can disregard strings; they will not contain numbers according to the description
    else:
        pass

num_list = []
traverse_json__and_disregard_red(json_list)
print(sum(num_list))