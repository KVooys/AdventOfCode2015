
r"""
--- Day 8: Matchsticks ---

Space on the sleigh is limited this year, and so Santa will be bringing his list as a digital copy. He needs to know how much space it will take up when stored.

It is common in many programming languages to provide a way to escape special characters in strings. For example, C, JavaScript, Perl, Python, and even PHP handle special characters in very similar ways.

However, it is important to realize the difference between the number of characters in the code representation of the string literal and the number of characters in the in-memory string itself.

For example:

    "" is 2 characters of code (the two double quotes), but the string contains zero characters.
    "abc" is 5 characters of code, but 3 characters in the string data.
    "aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote character, for a total of 7 characters in the string data.
    "\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal notation.

Santa's list is a file that contains many double-quoted string literals, one on each line. The only escape sequences used are  (which represents a single backslash), " (which represents a lone double-quote character), and \x plus two hexadecimal characters (which represents a single character with that ASCII code).

Disregarding the whitespace in the file, what is the number of characters of code for string literals minus the number of characters in memory for the values of the strings in total for the entire file?

For example, given the four strings above, the total number of characters of string code (2 + 5 + 10 + 6 = 23) minus the total number of characters in memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.
"""

# Part 1 is mostly input parsing
# There are 3 different escape sequences we need to "translate":
# 1) \\ is a slash
# 2) \" is a double-quote
# 3) "\x{2 digits}"" is a ASCII-encoded character

import re

# regular length before escapes; these are all 1 char too long because of the newline character at the end
with open("input/day8.txt") as input_file:
    inp = input_file.readlines()

pattern1 = re.compile(r'(\\\\)')
pattern2 = re.compile(r'(\\")')
pattern3 = re.compile(r'(\\x[0-9a-f]{2})')



regular_length = 0
escaped_length = 0
# for simplicity I'll replace pattern1 with 1s, pattern2 with 2s and pattern3 with 3s

for i in inp:
    regular_length += (len(i)-1)
    i = re.sub(pattern1, "1", i)
    i = re.sub(pattern2, "2", i)
    i = re.sub(pattern3, "3", i)
    # after all the replacements, the strings are still 3 chars too long: the enclosing quotes and the newline character at the end
    escaped_length += (len(i)-3)

print(regular_length, escaped_length, regular_length - escaped_length)

r"""
--- Part Two ---

Now, let's go the other way. In addition to finding the number of characters of code, you should now encode each code representation as a new string and find the number of characters of the new encoded representation, including the surrounding double quotes.

For example:

    "" encodes to "\"\"", an increase from 2 characters to 6.
    "abc" encodes to "\"abc\"", an increase from 5 characters to 9.
    "aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to 16.
    "\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11.

Your task is to find the total number of characters to represent the newly encoded strings minus the number of characters of code in each original string literal. For example, for the strings above, the total encoded length (6 + 9 + 16 + 11 = 42) minus the characters in the original code representation (23, just like in the first part of this puzzle) is 42 - 23 = 19.
"""

# part 2 is a bit more fun; now we have to sub the input for the escape sequences, using similar regex patterns
# the regular lenght answer of the first part still stands: 6202

part2_pattern1 = re.compile(r'"')
part2_pattern2 = re.compile(r'\\')

padded_length = 0
for i in inp:
    i = re.sub(part2_pattern1, "11", i)
    i = re.sub(part2_pattern2, "22", i)
    # the quotes on both ends should be counted for by adding 2 to the results (and still substracting 1 for the newline)
    padded_length += (len(i)+1)
    
print(padded_length, regular_length, padded_length - regular_length)