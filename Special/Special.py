# Special -- Parse tree node strategy for printing special forms

import sys
from abc import ABC, abstractmethod
from Tree import Nil
from Tree import Cons

# There are several different approaches for how to implement the Special
# hierarchy.  We'll discuss some of them in class.  The easiest solution
# is to not add any fields and to use empty constructors.

class Special(ABC):
    util = None

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    @abstractmethod
    def print(self, t, n, p):
        pass

    def eval(self, t, env):
        from Tree import Nil # Each subclass overrides this to handle its own behavior
        self._error("special form evaluation not implemented")
        return Nil.getInstance()

    def _error(self, msg):
        sys.stderr.write("Error: " + msg + "\n")
        sys.stderr.flush()
