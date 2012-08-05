"""
The reader class Summer is the powerhouse to all of this.
"""

import re
from collections import namedtuple

from eval_expr import eval_expr

# character to mark a line as a comment.
COMMENTCHAR = ';'

# string to mark a line as not to be accumulated towards sums.
DONT_ACC = '--'

Number = namedtuple("Number", "val type")


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

    def __analyze(self, s):
        """Parse the given string and return a list of Numbers."""

        # the regex to match all numbers
        NUMREGEX = r'-?\d+\.?\d*(?:[Ee][-+]?\d+)?'

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
            # here's the key:
            #if exprval: then run calculate with it, use the summer.VARS+variables
            #together for varspace. However, probs lie ahead: should this be
            #included in Summer or vice versa...
            #probably move this functionality in Summer 'cause we need the coms and
            #vars etc.
            try:
                nums.append(Number(val=float(val), type=typestr))
                if variablename: variables[variablename] = val
            except ValueError:
                pass
        return (nums, variables)

    def does_the_line_accumulate(self, line):
        """Determine if the given line's values should accumulate towards
        sums."""
        return (line.strip().startswith(DONT_ACC) or
                line.strip().endswith(DONT_ACC))

    def readline(self, line):
        """Read line of input and return the possible modified line back."""
        line = line.rstrip('\n')

        # when commentary, don't touch it!
        if line.lstrip().startswith(COMMENTCHAR):
            return line

        # inline calculations
        line = re.sub(r'<(.*?)>', self.calculate, line)

        # Get potential numerical info from the line
        nums_, vars_ = self.__analyze(line)
        if not self.does_the_line_accumulate(line):
            self.NUMS.extend(nums_)
        self.VARS.update(vars_)

        return line
