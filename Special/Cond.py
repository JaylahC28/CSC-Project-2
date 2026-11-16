# Cond -- Parse tree node strategy for printing the special form cond

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Cond(Special):
    def __init__(self):
        pass

    def eval(self, t, env):
        clauses = t.getCdr()

        while clauses.isPair():
            clause = clauses.getCar()
            test = clause.getCar()
            body = clause.getCdr()

            if test.isSymbol() and test.getName() == "else":
                return self.util.begin(body, env)

            result = test.eval(env)

            if not result.isBool() or result.boolVal:
                if body.isNull():
                    return result
                return self.util.begin(body, env)

            clauses = clauses.getCdr()

        return Nil.getInstance()

    def print(self, t, n, p):
        Printer.printCond(t, n, p)
