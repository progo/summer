"""
Define number types and provide operations for them.
"""

import re
from collections import namedtuple

# the regex to match all numbers
NUMREGEX = r'-?\d+\.?\d*(?:[Ee][-+]?\d+)?'

Number = namedtuple("Number", "val type")

def __analyze(s):
    """Parse the given string and return a list of Numbers."""
    # Collect numbers with a hairy regex.
    evaled_calcs = re.findall(
            # is there a variable defined?
            r'(?P<variable>@[a-zA-Z0-9_]+)?\s*' +
            # evaluation results
            r'(?:<.+?= (?P<exprval>' + NUMREGEX + r')>' +
            # match free standing numbers
            r'|(?P<numval>' + NUMREGEX + r')\b)' +
            # with the possible type
            r'\s*(?P<type>[a-zA-Z_]+)?', s)
    nums = []
    variables = {}
    for n in evaled_calcs:
        variablename = n[0]
        exprval = n[1]
        numval = n[2]
        typestr = n[3]
        val = numval if numval else exprval
        try:
            nums.append(Number(val=float(val), type=typestr))
            if variablename: variables[variablename] = val
        except ValueError:
            pass
    return (nums, variables)

def grab_numbers(s):
    """Parse the given string and return a list of Numbers."""
    nums, vars = __analyze(s)
    return nums

def grab_vars(s):
    """Parse the given string and return introduced variables as a dict."""
    nums, vars = __analyze(s)
    return vars

def grab_numbers_and_vars(s):
    """Parse the given string and return a tuple of a list of collected numbers
    and introduced variables as a dict."""
    return __analyze(s)
