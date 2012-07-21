"""
The reader class Summer is the powerhouse to all of this.
"""

import re

from eval_expr import eval_expr

COMMENTCHAR = ';'
DONT_ACC = '--'

class Summer():
    # possible variables defined
    VARS = {}

    # numerical values parsed
    NUMS = []

    # commands. This needs a tough refactoring.
    COMS = [("@sum", lambda self: sum(self.NUMS))]

    def grab_numbers(self, s):
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

    def process_commands(self, string):
        """Search-replace @commands in a string, return replaced."""
        formatterfn = lambda com, fn: str(fn)

        # Parse for potential @commands
        for com, fun in self.COMS:
            if com in string:
                # fun() now an instance method :/
                string = string.replace(com, formatterfn(com, fun(self)))
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
                r'(?P<variable>@[a-zA-Z0-9_]+)'+
                r'\s+(?P<value>-?\d+\.?\d*|<.+= (?P<exprvalue>[0-9. ]+)>)',
                line)
        if variables:
            exprvalue = variables.group('exprvalue')
            value = variables.group('value') if not exprvalue else exprvalue
            self.VARS[variables.group('variable')] = value

        # Get potential numerical info from the line, but skip lines with
        # DONT_ACC at the beginning or end.
        if not (line.strip().startswith(DONT_ACC) or
                line.strip().endswith(DONT_ACC)):
            nums = self.grab_numbers(line)
            if nums: self.NUMS.append(nums[-1])

        return line