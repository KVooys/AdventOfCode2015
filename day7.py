"""
--- Day 7: Some Assembly Required ---
This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

For example:

123 -> x means that the signal 123 is provided to wire x.
x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.
Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456
In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?
"""


# part 1: some input parsing first. Apparently there are these kinds of lines:
# 1) simple assignment: var1 -> var2 (var1 being an int or another var)
# 2) inverse assignment: NOT var1 -> var2
# 3) operator-wise assignment: var1 OPERATOR var2 -> var3

from collections import defaultdict
from dataclasses import dataclass

with open("input/day7.txt") as input_file:
    inp = input_file.readlines()

def parse_line(line):
    # simple assignment
    if len(line.split()) == 3:
        var1, _, var2 = line.split()
        assign(var1, var2)

    # inverse assignment
    elif line[0:3] == "NOT":
        _, var1, _, var2 = line.split()
        inverse_assign(var1, var2)
    # operator-wise assignment
    else:
        var1, operator, var2, _, var3 = line.split()
        op_assign(var1, var2, var3, operator)


# first populate the dict with Wires we already know the values for
def assign(var1, var2):
    # 3 usecases: 
    if var1 in wire_dict.keys():
        # var1 is a known Wire already
        if wire_dict[var1].value is not None:
            wire_dict[var2] = Wire(value=wire_dict[var1].value, signal=True)

    # var1 is an integer (and therefore known)
    else:
        try:
            var1 = int(var1)
            wire_dict[var2] = Wire(value=var1, signal=True)
    # var1 is unknown, so make a wire out of var2 for later use
        except:
            wire_dict[var2] = Wire(instruction="this.value = " + var1)


def inverse_assign(var1, var2):
    pass

def op_assign(var1, var2, var3, operator):
    pass

    
    
test_inp = [
    "123 -> x",
    "456 -> y",
    "x -> y",
    "a -> b",
    "x AND y -> d",
    "x OR y -> e",
    "x LSHIFT 2 -> f",
    "y RSHIFT 2 -> g",
    "NOT x -> h",
    "NOT y -> i",
]


"""
Instead of constantly looping, it feels like I can do this more cleanly

Let's make a wire class: by default, it has no signal, it will eventually have a value and it will have an instruction field
Once the value is known, the signal is set to True so the object can be ignored for the rest of the circuit
The instruction fields will be tested constantly during the loop, until all values are known

Flow of the circuit:
    Loop once to make Wire objects out of all the lines
    After that, keep looping until all Wires have a signal

"""

@dataclass
class Wire:
    instruction: str=""
    value: int=None
    signal: bool=False

    # def __repr__(self):
    #     if self.value:
    #         return str(self.value)
    #     else:
    #         return self.instruction

wire_dict = {}

for line in test_inp:
    # make wire objects out of the lines
    parse_line(line)
print(wire_dict)
a = 2
try:
    eval(wire_dict[b].instruction)
except:
    pass
print(wire_dict)