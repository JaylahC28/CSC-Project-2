# Closure -- the data structure for function closures

# Class Closure is used to represent the value of lambda expressions.
# It consists of the lambda expression itself, together with the
# environment in which the lambda expression was evaluated.

# The method apply() takes the environment out of the closure,
# adds a new frame for the function call, defines bindings for the
# parameters with the argument values in the new frame, and evaluates
# the function body.

import sys
from Tree import Node
from Tree.Environment import Environment
from Tree import Nil, Cons

class Closure(Node):
    util = None

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, f, e):
        self.fun = f                    # a lambda expression
        self.env = e                    # the environment in which
                                        # the function was defined

    def getFun(self):
        return self.fun

    def getEnv(self):
        return self.env

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Procedure")
        if self.fun != None:
            self.fun.print(abs(n) + 4)
        for _ in range(abs(n)):
            sys.stdout.write(' ')
        sys.stdout.write(" }\n")
        sys.stdout.flush()

    # TODO: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    
    def apply(self, args):
        # create a new scope using the closure's saved environment
        new_env = Environment(self.env)

        # extract parameters and function body
        lambda_parts = self.fun.getCdr()
        parameters = lambda_parts.getCar()
        body = lambda_parts.getCdr()

        # bind required parameters
        while parameters.isPair():
            if not args.isPair():
                self._error("too few arguments")
                return Nil.getInstance()

            name = parameters.getCar()
            value = args.getCar()

            new_env.define(name, value)

            parameters = parameters.getCdr()
            args = args.getCdr()

        # handle remaining arguments
        if parameters.isSymbol():
            new_env.define(parameters, args)
        elif not args.isNull():
            self._error("too many arguments")
            return Nil.getInstance()

        # evaluate the function body
        result = Nil.getInstance()

        while body.isPair():
            result = body.getCar().eval(new_env)
            body = body.getCdr()

        return result

