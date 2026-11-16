# Scheme4101 -- The main program of the Scheme interpreter

import os
import sys
from Parse import *
from Tokens import TokenType
from Tree import Ident, BuiltIn
from Tree.BuiltIn import NAMES, load
from Tree.Environment import Environment

prompt = "> "

if __name__ == "__main__":
    # Create scanner that reads from standard input
    scanner = Scanner(sys.stdin)
    
    if (len(sys.argv) > 2 or
        (len(sys.argv) == 2 and sys.argv[1] != "-d")):
        sys.stderr.write("Usage: python3 Scheme4101.py [-d]\n")
        sys.exit(2)
    
    # If command line option -d is provided, debug the scanner.
    if len(sys.argv) == 2 and sys.argv[1] == "-d":
        # sys.stdout.write("Scheme 4101> ")
        # sys.stdout.flush()
        tok = scanner.getNextToken()
        while tok != None:
            tt = tok.getType()

            sys.stdout.write(tt.name)
            if tt == TokenType.INT:
                sys.stdout.write(", intVal = " + str(tok.getIntVal()) + "\n")
            elif tt == TokenType.STR:
                sys.stdout.write(", strVal = " + tok.getStrVal() + "\n")
            elif tt == TokenType.IDENT:
                sys.stdout.write(", name = " + tok.getName() + "\n")
            else:
                sys.stdout.write("\n")

            # sys.stdout.write("Scheme 4101> ")
            # sys.stdout.flush()
            tok = scanner.getNextToken()
    else:
        # Create parser
        parser = Parser(scanner)
        BuiltIn.parser = parser

        # Frame for the built-in functions
        builtins = Environment()
        for name in NAMES:
            id = Ident(name)
            builtins.define(id, BuiltIn(id))

        # Load the Scheme definitions in ini.scm into the built-in frame
        BuiltIn.env = builtins
        ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ini.scm")
        if os.path.exists(ini):
            load(ini, builtins)

        # Frame for user definitions (the interaction environment)
        env = Environment(builtins)
        BuiltIn.env = env

        # Read-eval-print loop
        sys.stdout.write(prompt)
        sys.stdout.flush()
        root = parser.parseExp()
        while root != None:
            root.eval(env).print(0)
            sys.stdout.write(prompt)
            sys.stdout.flush()
            root = parser.parseExp()
        sys.stdout.write("\n")
