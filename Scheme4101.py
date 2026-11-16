
# Scheme4101 -- The main program of the Scheme interpreter

import os
import sys

from Parse import *
from Tokens import TokenType
from Tree import Ident, BuiltIn, Cons
from Tree.BuiltIn import NAMES, load
from Tree.Environment import Environment
from Tree.Closure import Closure
from Special.Special import Special
from Util import Util

prompt = "> "

if __name__ == "__main__":
    # Create scanner that reads from standard input
    scanner = Scanner(sys.stdin)

    # Initialize shared interpreter utilities
    util = Util()
    Cons.setUtil(util)
    Closure.setUtil(util)
    Special.setUtil(util)

    # Check command-line arguments
    if (len(sys.argv) > 2 or
        (len(sys.argv) == 2 and sys.argv[1] != "-d")):
        sys.stderr.write("Usage: python3 Scheme4101.py [-d]\n")
        sys.exit(2)

    # Debug scanner mode
    if len(sys.argv) == 2 and sys.argv[1] == "-d":
        tok = scanner.getNextToken()

        while tok is not None:
            tt = tok.getType()
            sys.stdout.write(tt.name)

            if tt == TokenType.INT:
                sys.stdout.write(
                    ", intVal = " + str(tok.getIntVal())
                )
            elif tt == TokenType.STR:
                sys.stdout.write(
                    ", strVal = " + tok.getStrVal()
                )
            elif tt == TokenType.IDENT:
                sys.stdout.write(
                    ", name = " + tok.getName()
                )

            sys.stdout.write("\n")
            tok = scanner.getNextToken()

    else:
        # Create parser
        parser = Parser(scanner)
        BuiltIn.parser = parser

        # Create environment for built-in functions
        builtins = Environment()

        for name in NAMES:
            identifier = Ident(name)
            builtins.define(identifier, BuiltIn(identifier))

        # Load built-in Scheme definitions
        BuiltIn.env = builtins

        ini = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "ini.scm"
        )

        if os.path.exists(ini):
            load(ini, builtins)

        # Create environment for user-defined variables
        env = Environment(builtins)
        BuiltIn.env = env

        # Read-eval-print loop
        sys.stdout.write(prompt)
        sys.stdout.flush()

        root = parser.parseExp()

        while root is not None:
            result = root.eval(env)
            result.print(0)

            sys.stdout.write(prompt)
            sys.stdout.flush()

            root = parser.parseExp()

        sys.stdout.write("\n")

