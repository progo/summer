#!/usr/bin/python
# vim: fdm=indent foldnestmax=1
import sys
import re

from eval_expr import eval_expr

COMMENTCHAR = ';'
DONT_ACC = '--'

# possible variables defined
VARS = {}

# numerical values parsed
NUMS = []

# commands
COMS = [("@sum", lambda: sum(NUMS)),
        ("@avg", lambda: sum(NUMS)/len(NUMS))]

def grab_numbers(s):
    """Collect numbers in a string, return as a list."""
    l = []

    # Collect eval results from <>s
    evaled_calcs = re.findall(r'<.+?= (-?[0-9\. ]+?)>', s)

    # remove <>s from s
    s = re.sub(r'<.+?>', '', s)

    # with the remaining data we proceed the usual way
    for t in evaled_calcs + s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

def process_commands(string):
    """Search-replace @commands in a string, return replaced."""
    formatterfn = lambda com, fn: str(fn)

    # Parse for potential @commands
    for com, fun in COMS:
        if com in string:
            string = string.replace(com, formatterfn(com, fun()))
    return string

def substitute_variables(string):
    """substitute @variables with their numeric counterparts."""
    for var in VARS.keys():
        string = string.replace(var, VARS[var])
    return string

def calculate(match):
    """do calculations inside <>s"""
    query = match.group(1)

    # remove stuff from RHS of =
    query = re.sub(r' =.*$', '', query)

    # substitute commands and variables here.
    processed = process_commands(query)
    processed = substitute_variables(processed)

    # eval
    ans = eval_expr(processed)

    if query == str(ans):
        return "<{0}>".format(ans)
    else:
        return "<{0} = {1}>".format(query, ans)

if __name__ == '__main__':
    """Run the program for stdin or file input. Output to stdout."""
    import fileinput
    for l in fileinput.input():
        l = l.rstrip('\n')

        # Commentary off. Do print, don't eval.
        if l.lstrip().startswith(COMMENTCHAR):
            print l
            continue

        # inline calculations
        l = re.sub(r'<(.*?)>', calculate, l)

        # fill in variables
        variables = re.search(r'(?P<variable>@[a-zA-Z0-9_]+)'+
                r'\s+(?P<value>-?\d+\.?\d*|<.+= (?P<exprvalue>[0-9. ]+)>)', l)
        if variables:
            exprvalue = variables.group('exprvalue')
            value = variables.group('value') if not exprvalue else exprvalue
            VARS[variables.group('variable')] = value

        # Get potential numerical info from the line, but skip lines with
        # DONT_ACC at the beginning or end.
        if not (l.strip().startswith(DONT_ACC) or l.strip().endswith(DONT_ACC)):
            nums = grab_numbers(l)
            for n in nums:
                NUMS.append(n)

        print l
