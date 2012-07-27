"""
Define number types and provide operations for them.
"""

import re
from collections import namedtuple


Number = namedtuple("Number", "val type")

def grab_numbers(s):
    """Parse the given string and return a list of Numbers."""
    # Collect numbers with a hairy regex.
    evaled_calcs = re.findall(
            # evaluation results
            r'(?:<.+?= (?P<exprval>-?[0-9\. ]+?)>' + 
            # match free standing numbers
            r'|\s*(?P<numval>-?[0-9\. ]+?)(?:\D|\Z))' +
            # with the possible type
            r'\s*(?P<type>[a-zA-Z_]+)?', s)
    nums = []
    for n in evaled_calcs:
        exprval = n[0]
        numval = n[1]
        typestr = n[2]
        val = numval if numval else exprval
        try:
            nums.append(Number(val=float(val), type=typestr))
        except ValueError:
            pass
    return nums

