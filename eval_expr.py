# kudos to J.F. Sebastian. http://stackoverflow.com/a/9558001/308668
import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor}

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr).body[0].value) # Module(body=[Expr(value=...)])

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.operator): # <operator>
        return operators[type(node)]
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return eval_(node.op)(eval_(node.left), eval_(node.right))
    else:
        raise TypeError(node)

