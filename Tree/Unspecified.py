# Unspecified -- Parse tree node class for the value returned by
# define, set!, set-car!, write, etc.

import sys
from Tree import Node

class Unspecified(Node):
    __instance = None

    @staticmethod
    def getInstance():
        if Unspecified.__instance == None:
            Unspecified()
        return Unspecified.__instance

    def __init__(self):
        if Unspecified.__instance != None:
            raise Exception("Class Unspecified is a singleton")
        else:
            Unspecified.__instance = self

    def print(self, n, p=False):
        if n >= 0:
            sys.stdout.write(' ' * n)
        sys.stdout.write("#{Unspecific}")
        if n >= 0:
            sys.stdout.write('\n')
