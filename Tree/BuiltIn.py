# BuiltIn -- Parse tree node class for representing built-in functions
#
# A BuiltIn holds the symbol for the function name.  apply() looks at
# the name and runs the matching Python code.  args is the Scheme list
# of argument values (already evaluated by the caller).

import sys
from Tree import Node, Ident, IntLit, StrLit, BoolLit, Nil, Cons
from Tree.Unspecified import Unspecified

class BuiltIn(Node):
    # Set by main before anything is evaluated
    env = None          # the interaction (global) environment
    parser = None       # parser on stdin, used by read

    def __init__(self, s):
        self.symbol = s

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def eval(self, env):
        return self

    def print(self, n, p=False):
        if n >= 0:
            sys.stdout.write(' ' * n)
        sys.stdout.write("#{Procedure " + self.symbol.name + "}")
        if n >= 0:
            sys.stdout.write('\n')

    def apply(self, args):
        name = self.symbol.name
        argv = []
        while args.isPair():
            argv.append(args.getCar())
            args = args.getCdr()

        if name in ARGCOUNT and len(argv) != ARGCOUNT[name]:
            return error("wrong number of arguments to " + name)

        nargs = len(argv)
        arg1 = argv[0] if nargs > 0 else None
        arg2 = argv[1] if nargs > 1 else None

        # arithmetic
        if name in ("b+", "b-", "b*", "b/", "b=", "b<"):
            if not (arg1.isNumber() and arg2.isNumber()):
                return error("non-integer argument to " + name)
            x = arg1.intVal
            y = arg2.intVal
            if name == "b+":
                return IntLit(to32(x + y))
            if name == "b-":
                return IntLit(to32(x - y))
            if name == "b*":
                return IntLit(to32(x * y))
            if name == "b/":
                if y == 0:
                    return error("division by zero")
                q = abs(x) // abs(y)
                if (x < 0) != (y < 0):
                    q = -q
                return IntLit(to32(q))
            if name == "b=":
                return BoolLit.getInstance(x == y)
            return BoolLit.getInstance(x < y)

        # type tests
        if name == "symbol?":
            return BoolLit.getInstance(arg1.isSymbol())
        if name == "number?":
            return BoolLit.getInstance(arg1.isNumber())
        if name == "null?":
            return BoolLit.getInstance(arg1.isNull())
        if name == "pair?":
            return BoolLit.getInstance(arg1.isPair())
        if name == "procedure?":
            return BoolLit.getInstance(arg1.isProcedure())

        # list operations
        if name == "car":
            if not arg1.isPair():
                return error("car of non-pair")
            return arg1.getCar()
        if name == "cdr":
            if not arg1.isPair():
                return error("cdr of non-pair")
            return arg1.getCdr()
        if name == "cons":
            return Cons(arg1, arg2)
        if name == "set-car!":
            if not arg1.isPair():
                return error("set-car! of non-pair")
            arg1.setCar(arg2)
            return Unspecified.getInstance()
        if name == "set-cdr!":
            if not arg1.isPair():
                return error("set-cdr! of non-pair")
            arg1.setCdr(arg2)
            return Unspecified.getInstance()
        if name == "eq?":
            return BoolLit.getInstance(isEq(arg1, arg2))

        # I/O
        if name == "read":
            exp = BuiltIn.parser.parseExp()
            if exp == None:
                return Nil.getInstance()
            return exp
        if name == "write":
            arg1.print(-1)
            sys.stdout.flush()
            return Unspecified.getInstance()
        if name == "display":
            if arg1.isString():
                sys.stdout.write(arg1.strVal)
            else:
                arg1.print(-1)
            sys.stdout.flush()
            return Unspecified.getInstance()
        if name == "newline":
            sys.stdout.write("\n")
            sys.stdout.flush()
            return Unspecified.getInstance()

        # interpreter hooks
        if name == "eval":
            return arg1.eval(arg2)
        if name == "apply":
            return arg1.apply(arg2)
        if name == "interaction-environment":
            return BuiltIn.env
        if name == "load":
            if not arg1.isString():
                return error("load needs a file name string")
            return load(arg1.strVal, BuiltIn.env)

        return error("unknown built-in " + name)


# Number of arguments each built-in takes
ARGCOUNT = {
    "b+": 2, "b-": 2, "b*": 2, "b/": 2, "b=": 2, "b<": 2,
    "symbol?": 1, "number?": 1, "null?": 1, "pair?": 1, "procedure?": 1,
    "car": 1, "cdr": 1, "cons": 2, "set-car!": 2, "set-cdr!": 2, "eq?": 2,
    "read": 0, "write": 1, "display": 1, "newline": 0,
    "eval": 2, "apply": 2, "interaction-environment": 0, "load": 1,
}

NAMES = list(ARGCOUNT.keys())


def error(msg):
    sys.stderr.write("Error: " + msg + "\n")
    return Nil.getInstance()

# Keep results in the 32-bit signed range
def to32(x):
    x = x & 0xFFFFFFFF
    if x >= 0x80000000:
        x -= 0x100000000
    return x

def isEq(a, b):
    if a is b:
        return True
    if a.isSymbol() and b.isSymbol():
        return a.name == b.name
    if a.isNumber() and b.isNumber():
        return a.intVal == b.intVal
    return False

# Read-eval loop over a file.  Results are not printed.
def load(filename, env):
    from Parse import Scanner, Parser
    try:
        f = open(filename)
    except IOError:
        return error("could not open file " + filename)
    parser = Parser(Scanner(f))
    exp = parser.parseExp()
    while exp != None:
        exp.eval(env)
        exp = parser.parseExp()
    f.close()
    return Unspecified.getInstance()
