"""
--- Day 11: Corporate Policy ---
Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has devised a method of coming up with a password based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons), so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
For example:

hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
abbcegjk fails the third requirement, because it only has one double letter (bb).
The next password after abcdefgh is abcdffaa.
The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.
Given Santa's current password (your puzzle input), what should his next password be?
"""

import re
from string import ascii_lowercase
from itertools import cycle

with open("input/day11.txt") as input_file:
    inp = input_file.readline()

# part 1: let's start with looping over the cycle of valid letters (so the alphabet but not i, o and l)
# remove i, o, l
pattern_iol = re.compile(r"i|o|l")
s = ascii_lowercase
s = re.sub(pattern_iol, "", s)
# make it a cycle to allow the "wraparound feature" when the z is reached
possible_chars = cycle(s)

# print(ord("z"), ord("y"), ord("a"))

# function to "increment" the word
def increment_word(word):
    # if the final letter is not unicode point 122 /z, just increment it and pass
    if (ord(word[len(word)-1])) != 122:
        new_word =  word[0:len(word)-1] + chr(ord(word[len(word)-1])+1)
    # if the final letter is a z, increment one letter before it, then change the z to an a
    # if the letter before it is also a z, keep checking until one isn't
    else:
        # 2nd to last letter is not a z
        # new_word = word[0:len(word)-2] + chr(ord(word[len(word)-2])+1) + 1*"a"
        # 3rd to last letter is not a z
        # new_word = word[0:len(word)-3] + chr(ord(word[len(word)-3])+1) + 2*"a"
        # etc.
        # Do this quickly by splitting on the first z instead of looping over every letter
        # since there is a pattern here, I've come up with the below algorithm:
        word_parts = word.split("z")
        new_word = word_parts[0][0:-1] + chr(ord(word_parts[0][-1])+1) + (len(word_parts)-1)*"a"
        
    return new_word

print(increment_word("Hello")) # should be Hellp
print(increment_word("Hellz")) # should be Helma
print(increment_word("Hezzz")) # should be Hfaaa

# workflow:
# check against constraints
# increment the word
# Good to note:
# if we hit the "iol" constraint at any point, we can smartly discard a certain number of possibilities.
# so let's say Hhzzz becomes Hiaaa, then we should skip straight to Hjaaa (saving 26**3 loops)

