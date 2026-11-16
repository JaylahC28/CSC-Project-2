# Let -- Parse tree node strategy for printing the special form let

from Tree import Nil
from Tree import Environment
from Print import Printer
from Special import Special

class Let(Special):
    def __init__(self):
        pass

    def eval(self, t, env):
        args = t.getCdr()
        bindings = args.getCar()
        body = args.getCdr()

        new_env = Environment.Environment(env)

        while bindings.isPair():
            binding = bindings.getCar()

            name = binding.getCar()
            expression = binding.getCdr().getCar()

            value = expression.eval(env)
            new_env.define(name, value)

            bindings = bindings.getCdr()

        if body.isNull():
            return Nil.getInstance()

        return self.util.begin(body, new_env)

    def print(self, t, n, p):
        Printer.printLet(t, n, p)
