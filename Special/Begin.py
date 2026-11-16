# Begin -- Parse tree node strategy for printing the special form begin

from Tree import Nil
from Print import Printer
from Special import Special

class Begin(Special):
    def __init__(self):
        pass

    def eval(self, t, env):
        #Evaluate expressions in order and return last
        expressions = t.getCdr()

        if expressions.isNull():
            return Nil.getInstance()

        return self.util.begin(expressions, env)


    def print(self, t, n, p):
        Printer.printBegin(t, n, p)
