"""
The reader class Summer is the powerhouse to all of this.
"""

import re

from eval_expr import eval_expr
import nums

COMMENTCHAR = ';'
DONT_ACC = '--'

class Summer():

    def do_sum(self, arg):
        if not arg:
            return sum(x.val for x in self.NUMS)
        return sum(x.val for x in self.NUMS if x.type == arg)

    def __init__(self):
        # possible variables defined
        self.VARS = {}

        # numerical values parsed. This is of type Number.
        self.NUMS = []

        # commands. This needs a tough refactoring.
        self.COMS = {"sum": self.do_sum}

    def process_commands(self, string):
        """Search-replace @commands in a string, return replaced. Commands can
        have arguments. The syntax comes: `@com[:args]`. """

        def do_func_eval(m):
            """fetch the function from COMS and call it."""
            if m.group('func') not in self.COMS:
                return '@'+m.group('func')
            return str(self.COMS[m.group('func')](m.group('arg')))

        string = re.sub(r'@(?P<func>[a-zA-Z]+)(?::(?P<arg>[a-zA-Z_]+))?',
                do_func_eval, string)

        return string

    def substitute_variables(self, string):
        """substitute @variables with their numeric counterparts."""
        for var in self.VARS.keys():
            string = string.replace(var, self.VARS[var])
        return string

    def calculate(self, match):
        """do calculations inside <>s"""
        query = match.group(1)

        # remove stuff from RHS of =
        query = re.sub(r' =.*$', '', query)

        # substitute commands and variables here.
        processed = self.process_commands(query)
        processed = self.substitute_variables(processed)

        # eval
        ans = eval_expr(processed)

        if query == str(ans):
            return "<{0:g}>".format(ans)
        else:
            return "<{0} = {1:g}>".format(query, ans)

    def readline(self, line):
        """Read line of input and return the possible modified line back."""
        line = line.rstrip('\n')

        # when commentary, just return it back
        if line.lstrip().startswith(COMMENTCHAR):
            return line

        # inline calculations
        line = re.sub(r'<(.*?)>', self.calculate, line)

        # fill in variables
        variables = re.search(
                # variable name
                r'(?P<variable>@[a-zA-Z0-9_]+)'+
                # plain value
                r'\s+(?P<value>' + nums.NUMREGEX + r'|' +
                # expression result
                r'<.+= (?P<exprvalue>'+ nums.NUMREGEX + r')>)',
                line)
        if variables:
            exprvalue = variables.group('exprvalue')
            value = variables.group('value') if not exprvalue else exprvalue
            self.VARS[variables.group('variable')] = value

        # Get potential numerical info from the line
        if not (line.strip().startswith(DONT_ACC) or
                line.strip().endswith(DONT_ACC)):
            self.NUMS.extend(nums.grab_numbers(line))

        return line
