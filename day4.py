"""
--- Day 4: The Ideal Stocking Stuffer ---
Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....
"""

import hashlib

with open("input/day4.txt") as input_file:
    inp = input_file.readline()

# we need to loop over the string <input> + 
result = ""
current_int = 0
while result == "":
    current_str = inp + str(current_int)
    new_md5 = hashlib.md5(current_str.encode())
    test_result = new_md5.hexdigest()
    # print(test_result[0:5])
    if test_result[0:5] == "00000":
        print(current_int, test_result)
        break
    current_int += 1

"""
--- Part Two ---
Now find one that starts with six zeroes.
"""
# Part 2 is very easy as it's almost the same as part 1; it just takes a bit longer
result = ""
current_int = 0
while result == "":
    current_str = inp + str(current_int)
    new_md5 = hashlib.md5(current_str.encode())
    test_result = new_md5.hexdigest()
    # print(test_result[0:5])
    if test_result[0:6] == "000000":
        print(current_int, test_result)
        break
    current_int += 1


