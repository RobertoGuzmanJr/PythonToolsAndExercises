#!/bin/python3

import math
import os
import random
import re
import sys

"""
How many legal phone numbers can be generated by a knight on a keypad? A valid phone number cannot begin with
0 or 1 and may not have a # or a * in it. It also has to be 7 digits long.

Here is a visual representation of a keypad:

1 2 3
4 5 6
7 8 9
* 0 #

We can proceed recursively, by adding elements to a global sequences set and then remove those cases that do not qualify.
"""

d = {
    '1': ['6', '8'],
    '2': ['7', '9'],
    '3': ['4', '8'],
    '4': ['3', '9', '0'],
    '5': ['*', '#'],
    '6': ['1', '7', '0'],
    '7': ['#', '6', '2'],
    '8': ['1', '3'],
    '9': ['2', '4', '*'],
    '*': ['9', '5'],
    '0': ['6', '4'],
    '#': ['5', '7']
}

sequences = []

def generate_numbers(key, seq):
    global sequences
    global d

    if len(seq) == 7:
        sequences.append(seq)
        return
    else:
        for k in d[key]:
            for num in k:
                newSeq = seq + str(num)
                generate_numbers(num, newSeq)



def keypad_chess():
    for k in d.keys():
        generate_numbers(str(k),str(k))
    s = sequences #to make this unique
    s = [x for x in s if (x.find('#') == -1) and (x.find('*') == -1) and x[0] not in ['0','1']]
    return len(s)

if __name__ == '__main__':
    result = keypad_chess()
    print(result)
