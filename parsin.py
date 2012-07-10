#!/usr/bin/python
# vim: fdm=indent foldnestmax=1
import sys
import re

from eval_expr import eval_expr

COMMENTCHAR = ';'

# possible variables defined
VARS = {}

# numerical values parsed
NUMS = []

# commands
COMS = [("@sum", lambda: sum(NUMS)),
        ("@avg", lambda: sum(NUMS)/len(NUMS))]

def grab_numbers(s):
    """Collect numbers in a string, return as a list."""

    # check if there are calculations here. TODO this won't collect nums
    # without =. This is a hack anyhow.
    evaledcalcs = re.search(r'<.+= ([0-9. ]+)>', s)
    if evaledcalcs and not "@sum" in s:
        return [float(evaledcalcs.group(1))]

    # else we proceed with the usual
    l = []
    for t in s.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    return l

def format_output(comstr, value):
    """Decide the string output of commands."""

    # get rid of .0 decimal points
    if int(value) == value: value = int(value)

    return "{0}<{1}>".format(comstr, value)

def process_commands(string, bare = False):
    """Search-replace @commands in a string, return replaced."""
    formatterfn = format_output if not bare else lambda com, fn: str(fn)

    # Parse for potential @commands
    for com, fun in COMS:
        if com in string:
            string = string.replace(com, formatterfn(com, fun()))
    return string

def substitute_variables(string):
    """substitute :variables with their numeric counterparts."""
    return string #TODO

def calculate(match):
    """do calculations inside <>s"""
    query = match.group(1)

    # remove stuff from RHS of =
    query = re.sub(r' =.*$', '', query)

    # replace commands here.
    processed = process_commands(query, bare=True)

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

        #l = process_commands(l)

        # inline calculations
        l = re.sub(r'<(.*?)>', calculate, l)

        # fill in variables
        variables = re.search(r'(?P<variable>@[a-zA-Z0-9_]+)'+
                r'\s+(?P<value>-?\d+\.?\d*|<.+= (?P<exprvalue>[0-9. ]+)>)', l)
        if variables:
            exprvalue = variables.group('exprvalue')
            value = variables.group('value') if not exprvalue else exprvalue
            VARS[variables.group('variable')] = float(value)

        # get potential numerical info from the line
        # TODO this won't do with calculations
        nums = grab_numbers(l)                
        if nums: NUMS.append(nums[-1])

        print l
    #print VARS
