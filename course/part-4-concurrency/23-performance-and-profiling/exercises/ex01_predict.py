"""Exercise 23.1 — Rank ten operations, then measure.

Write your predicted ranking (1 = fastest) BEFORE running. Then score yourself.

Getting the ORDER right matters more than the numbers -- the order is what you
use when reading code, and the numbers change with hardware and version.

Run:  python ex01_predict.py
"""
from __future__ import annotations

import timeit

PREDICTIONS = """
Rank these 1 (fastest) to 10 (slowest), per operation:

  __ read a local variable
  __ read a global variable
  __ read an attribute (obj.x)
  __ call a function that does nothing
  __ call a method that does nothing
  __ create a small object (a 3-field class instance)
  __ dict lookup by string key
  __ list append
  __ enter a try block where nothing raises
  __ raise and catch an exception

Then predict the RATIO between the fastest and the slowest. Most people
underestimate it by an order of magnitude.
"""

SETUP = """
class Thing:
    __slots__ = ('x', 'y', 'z')
    def __init__(self): self.x = self.y = self.z = 1
    def method(self): pass

def function(): pass

obj = Thing()
d = {'key': 1}
lst = []
g = 1
"""

CASES = [
    ("local variable read",   "x = 1\nx"),
    ("global variable read",  "g"),
    ("attribute read",        "obj.x"),
    ("function call",         "function()"),
    ("method call",           "obj.method()"),
    ("object creation",       "Thing()"),
    ("dict lookup",           "d['key']"),
    ("list append",           "lst.append(1)"),
    ("try, no exception",     "try:\n    pass\nexcept ValueError:\n    pass"),
    ("raise and catch",       "try:\n    raise ValueError()\nexcept ValueError:\n    pass"),
]


def measure() -> None:
    results: list[tuple[str, float]] = []
    for label, stmt in CASES:
        best = min(timeit.repeat(stmt, SETUP, number=200_000, repeat=5))
        results.append((label, best / 200_000 * 1e9))

    results.sort(key=lambda kv: kv[1])
    fastest = results[0][1]
    print(f"\n  {'rank':<6}{'operation':<24}{'ns/op':>10}{'relative':>12}")
    print("  " + "-" * 52)
    for rank, (label, ns) in enumerate(results, start=1):
        print(f"  {rank:<6}{label:<24}{ns:>10.1f}{ns / fastest:>11.1f}x")

    print(
        "\n  THE ONE THAT MATTERS: compare the function-call row with the\n"
        "  local-variable row. That ratio is why a comprehension beats\n"
        "  map(lambda ...), why hot loops sometimes bind builtins to locals,\n"
        "  and above all why NumPy wins -- one call over a million elements\n"
        "  instead of a million calls."
    )


# TODO 1: score your ranking. How many of the ten did you place correctly?

# TODO 2: the try/except row surprises people. Explain the result -- what does
#         entering a try block cost when nothing raises, and why? (Module 24
#         and the `dis` module will tell you.)

# TODO 3: add three more rows and predict each first:
#         - a list comprehension over 100 items
#         - the same with map(lambda ...)
#         - the same with a plain for loop and append
#         Explain the ordering in terms of the function-call cost.

# TODO 4: now the question that matters. Take the SLOWEST operation here and
#         compute how many times per second you would have to do it before it
#         accounted for one percent of a 200ms request. Then say what that
#         means for how much time you should spend micro-optimising.


if __name__ == "__main__":
    print(PREDICTIONS)
    measure()
