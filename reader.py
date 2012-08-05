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

    def does_the_line_accumulate(self, line):
        """Determine if the given line's values should accumulate towards
        sums."""
        return not (line.strip().startswith(DONT_ACC) or
                line.strip().endswith(DONT_ACC))

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

    def calculate(self, query):
        """read and eval an expression in string. Return modified string back
        with the result."""
        #query = match.group(1)

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

    def calculate_match(self, match):
        """Calculate using match objects of 're'. Return result string with the
        answer."""
        return self.calculate(match.group(1))

    def extract_rhs(self, expr):
        """return the X of <A+B/C = X>"""
        return re.sub(r'^.*= ', '', expr).rstrip('> ')

    def go_through_the_string(self, s, do_acc=True):
        """Do the hairy work. The unit amount is one line. We will gather
        numbers and define variables and evaluate expressions."""
        # the regex to match all numbers
        NUMREGEX = r'-?\d+\.?\d*(?:[Ee][-+]?\d+)?'

        # Collect numbers and expressions with a hairy regex.
        evaled_calcs = re.findall(
                # is there a variable defined?
                r'(?P<variable>@[a-zA-Z0-9_]+)?\s*' +
                # evaluation results
                r'(?:(?P<expr><.+?(?:= (?P<exprval>' + NUMREGEX + r'))?>)' +
                # match free standing numbers
                r'|(?P<numval>' + NUMREGEX + r')\b)' +
                # with the possible type
                r'\s*(?P<type>[a-zA-Z_]+)?', s)
        for n in evaled_calcs:
            variablename = n[0]
            expr = n[1]
            exprval = n[2]
            numval = n[3]
            typestr = n[4]
            val = numval if numval else exprval
            if expr:
                # TODO this here contains a nasty source of bugs. Consider a
                # line that contains two identical expressions. We can
                # circumvent this with a placeholder hack or doing this
                # properly with a parser.
                evaled_result = self.calculate(expr[1:-1])
                s = s.replace(expr, evaled_result)
                val = self.extract_rhs(evaled_result)
            try:
                if do_acc:
                    self.NUMS.append(Number(val=float(val), type=typestr))
                if variablename: self.VARS[variablename] = val
            except ValueError:
                pass
        return s

    def readline(self, line):
        """Read line of input and return the possible modified line back."""
        line = line.rstrip('\n')

        # when commentary, don't touch it!
        if line.lstrip().startswith(COMMENTCHAR):
            return line

        line = self.go_through_the_string(line,
                do_acc=self.does_the_line_accumulate(line))

        return line
