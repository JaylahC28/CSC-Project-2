# If -- Parse tree node strategy for printing the special form if

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class If(Special):
    def __init__(self):
        pass
    
    def eval(self, t, env):
        args = t.getCdr()

        condition = args.getCar().eval(env)
        then_expr = args.getCdr().getCar()
        remaining = args.getCdr().getCdr()

        if not condition.isBool() or condition.boolVal:
            return then_expr.eval(env)

        if not remaining.isNull():
            return remaining.getCar().eval(env)

        return Nil.getInstance()


    def print(self, t, n, p):
        Printer.printIf(t, n, p)
