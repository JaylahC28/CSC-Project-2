# Set -- Parse tree node strategy for printing the special form set!

from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Set(Special):
    def __init__(self):
        pass

    def eval(self, t, env):
        args = t.getCdr()

        name = args.getCar()
        value = args.getCdr().getCar().eval(env)

        env.assign(name, value)

        return Nil.getInstance()
  
    def print(self, t, n, p):
        Printer.printSet(t, n, p)
