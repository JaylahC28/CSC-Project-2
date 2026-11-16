# Define -- Parse tree node strategy for printing the special form define

from Tree import Ident
from Tree import Nil
from Tree import Cons
#from Tree import Void
from Print import Printer
from Special import Special

class Define(Special):
    def __init__(self):
        pass
    
    def eval(self, t, env):
        from Tree import Closure

        args = t.getCdr()
        target = args.getCar()
        rest = args.getCdr()

        if target.isSymbol():
            value = rest.getCar().eval(env)
            env.define(target, value)
        else:
            name = target.getCar()
            parameters = target.getCdr()

            lambda_expr = Cons(
                Ident("lambda"),
                Cons(parameters, rest)
            )

            closure = Closure(lambda_expr, env)
            env.define(name, closure)

        return Nil.getInstance()

    def print(self, t, n, p):
        Printer.printDefine(t, n, p)
