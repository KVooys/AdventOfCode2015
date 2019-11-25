"""
--- Day 19: Medicine for Rudolph ---
Rudolph the Red-Nosed Reindeer is sick! His nose isn't shining very brightly, and he needs medicine.

Red-Nosed Reindeer biology isn't similar to regular reindeer biology; Rudolph is going to need custom-made medicine. Unfortunately, Red-Nosed Reindeer chemistry isn't similar to regular reindeer chemistry, either.

The North Pole is equipped with a Red-Nosed Reindeer nuclear fusion/fission plant, capable of constructing any Red-Nosed Reindeer molecule you need. It works by starting with some input molecule and then doing a series of replacements, one per step, until it has the right molecule.

However, the machine has to be calibrated before it can be used. Calibration involves determining the number of molecules that can be generated in one step from a given starting point.

For example, imagine a simpler machine that supports only the following replacements:

H => HO
H => OH
O => HH
Given the replacements above and starting with HOH, the following molecules could be generated:

HOOH (via H => HO on the first H).
HOHO (via H => HO on the second H).
OHOH (via H => OH on the first H).
HOOH (via H => OH on the second H).
HHHH (via O => HH).
So, in the example above, there are 4 distinct molecules (not five, because HOOH appears twice) after one replacement from HOH. Santa's favorite molecule, HOHOHO, can become 7 distinct molecules (over nine replacements: six from H, and three from O).

The machine replaces without regard for the surrounding characters. For example, given the string H2O, the transition H => OO would result in OO2O.

Your puzzle input describes all of the possible replacements and, at the bottom, the medicine molecule for which you need to calibrate the machine. How many distinct molecules can be created after all the different ways you can do one replacement on the medicine molecule?
"""

import re
import pprint
from collections import defaultdict
from difflib import SequenceMatcher

# part 1: input parsing
# The input is a list of possible replacements, followed by an empty line, followed by the input molecule
# it would be useful to keep track of every possible replacement as a dict, like this in the sample:
# {H: [OH, HO], O: [HH]}

SAMPLE_INPUT = """
H => HO
H => OH
O => HH

HOH
""".split("\n")

# The replacements always look like <a> => <b>
pattern = r"(\w+) => (\w+)"

def parse(lines):
    possible_replacements = defaultdict(list)

    for line in lines:
        # store replacements in a dict
        if re.match(pattern, line):
            initial, replacer = re.match(pattern, line).groups()
            possible_replacements[initial].append(replacer)
        elif len(line) != 0:
            starter_molecule = line
    return starter_molecule, possible_replacements


# since we're interested in the number of unique combinations (ignoring duplicates), it can be useful to store the already found combinations in a set.
# The sample starter molecule is HOH, 2 H's and 1 O.
# Since both H's have 2 possible replacements, these give 4 permutations. The O only has 1 possible replacement, so 1 more permutation = 5 total.
# Generally, for every key in the possible_replacements dict, we can do a find & replace in the molecule and store its output for each of its possible replacements.

def generate_combinations(molecule, replacements):
    unique_results = set()
    for k, v in replacements.items():
        replacable_locations = re.finditer(k, molecule)
        for l in replacable_locations:
            # not all elements are length 1: in the real input, there's also Ca and Mg and such.
            (start_idx, end_idx) = l.span()
            # print(start_idx, end_idx)
            # print(molecule[start_idx:end_idx])
            for replacement_value in v:
                current_result = molecule[:start_idx] + replacement_value + molecule[end_idx:]
                unique_results.add(current_result)
    return unique_results


# molecule, replacements = parse(SAMPLE_INPUT)
# results = generate_combinations(molecule, replacements)
# pprint.pprint(results)
# print(len(results))

with open("input/day19.txt") as input_file:
    inp = input_file.readlines()

molecule, replacements = parse(inp)
results = generate_combinations(molecule, replacements)
print(len(results))

"""
--- Part Two ---
Now that the machine is calibrated, you're ready to begin molecule fabrication.

Molecule fabrication always begins with just a single electron, e, and applying replacements one at a time, just like the ones during calibration.

For example, suppose you have the following replacements:

e => H
e => O
H => HO
H => OH
O => HH
If you'd like to make HOH, you start with e, and then make the following replacements:

e => O to get O
O => HH to get HH
H => OH (on the second H) to get HOH
So, you could make HOH after 3 steps. Santa's favorite molecule, HOHOHO, can be made in 6 steps.

How long will it take to make the medicine? Given the available replacements and the medicine molecule in your puzzle input, what is the fewest number of steps to go from e to the medicine molecule?
"""

# part 2 will require going over the combinations starting from e to get to the answer
# However, it has to include some sort of early abortion of combinations
# Because of replacements like H => HCa, there could be an infinite amount of replacements (resulting in HCaCaCaCa...) that gets us no further to the answer.
# Because all the replacements make the molecule longer (or at least keep it the same size) we can abort sequences that have exceeded the answer's length

SAMPLE_INPUT2 = """
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
""".split("\n")




# Finding sequences would go like this:
# if not exhausted:
# generate_combations(e, replacements) = {"H", "O"}
# for c in {"H", "O"}:
# generate_combinations(c, replacements)
# ...keep going until all possible combinations are found, return the sequence lengths that result in HOHOHO
# To keep track of the count, I rewrote the generate combinations to work recursively.

def generate_combinations_recursively(molecule, target, replacements, count):
    # keep track of similarity ratio of current molecule and target
    current_ratio = SequenceMatcher(None, molecule, target).quick_ratio()
    print(current_ratio, count)
    unique_results = set()
    count += 1
    for k, v in replacements.items():
        replacable_locations = re.finditer(k, molecule)
        for l in replacable_locations:
            (start_idx, end_idx) = l.span()
            for replacement_value in v:
                current_result = molecule[:start_idx] + replacement_value + molecule[end_idx:]
                unique_results.add(current_result)
    if target not in unique_results:
        # print("Failed to find target in ", unique_results, ", count: ", count)
        for r in unique_results:
            # Because all the replacements make the molecule longer (or at least keep it the same size) we can abort sequences that have exceeded the answer's length
            if len(r) <= len(target) and r not in tried:
                
                # only continue with the sequences that have a high similarity ratio and that have not been tried yet
                tried.add(r)
                new_ratio = SequenceMatcher(None, r, target).quick_ratio()
                if new_ratio >= current_ratio:
                    generate_combinations_recursively(r, target, replacements, count)
    else:
        print(count)
        print(molecule, "Found target in ", unique_results, ", count: ", count)
        sequence_lengths.add(count)


starter_molecule = "e"
desired_answer, replacements = parse(inp)
# desired_answer, replacements = parse(SAMPLE_INPUT2)

# keep track of found sequence lengths
sequence_lengths = set()
tried = set()
generate_combinations_recursively(starter_molecule, desired_answer, replacements, 0)
print(sequence_lengths)

# While the above code did not find the exact amount in a reasonable time, it concentrated 98% right answers for a lot of outputs with sequence lengths of between 197 and 202.
# This meant that we can reasonably expect the shortest sequence to be in that neighbourhood, so I guessed 201 and 200 and 200 was the right answer.
# Further inspection of the input made me realize that Rn, Y and Ar are basically special, as they only appear in lengthening replacements (and never purely same-length replacing ones).
# Using this knowledge, you could shrink down the computation needed by backtracking the process (starting from the large result string, going down to e) and first removing the Rn, Y and Ar combinations.
# Ultimately, while using difflib ratio API was a cool idea, I think it moved my thought process away from what the problem input was implying.
# I also failed to take into account that all replacements could only be done once
