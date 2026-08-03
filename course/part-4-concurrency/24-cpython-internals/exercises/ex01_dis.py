"""Exercise 24.1 — Fifteen disassemblies, fifteen questions.

Several of these settle arguments from earlier modules. Predict the ANSWER to
each question before running.

Run:  python ex01_dis.py
"""
from __future__ import annotations

import dis
import sys


def show(label: str, source: str, question: str) -> None:
    print(f"\n{'=' * 70}\n{label}\n  source: {source!r}\n  Q: {question}\n")
    dis.dis(compile(source, "<s>", "exec"))


CASES: list[tuple[str, str, str]] = [
    ("01 constant folding", "x = 1 + 2",
     "How many arithmetic instructions? What does that tell you about "
     "timeit('1+2')?"),

    ("02 augmented assignment", "a += 1",
     "How many instructions? Now explain Module 21's counter race using them."),

    ("03 local vs global", "def f():\n    x = 1\n    return x + g",
     "Which two different LOAD instructions appear, and why is one faster?"),

    ("04 comprehension scope", "r = [i for i in data]",
     "Where did the loop body go? Why does the loop variable not leak "
     "(Module 04)?"),

    ("05 comprehension vs map", "r = [f(i) for i in data]\ns = list(map(f, data))",
     "Which does more work per element, and why (Module 01)?"),

    ("06 f-string", "s = f'{a}-{b}'",
     "Is this string concatenation? What instruction actually builds it?"),

    ("07 string concat in a loop",
     "out = ''\nfor p in parts:\n    out += p",
     "What is the complexity, and which instruction is doing the work "
     "(Module 03)?"),

    ("08 chained comparison", "r = 1 < x < 10",
     "How many times is x evaluated? Compare with (1 < x) and (x < 10)."),

    ("09 the with statement", "with open(p) as f:\n    pass",
     "Which instructions correspond to __enter__ and __exit__ (Module 09)?"),

    ("10 try with no exception", "try:\n    pass\nexcept ValueError:\n    pass",
     "What does entering the try cost on 3.11+? (Compare with 3.10.)"),

    ("11 a generator", "def g():\n    yield 1\n    yield 2",
     "Which instruction marks it a generator? What is in co_flags?"),

    ("12 method call", "obj.method(1)",
     "Which instruction avoids allocating a bound method, and why does that "
     "matter (Module 08)?"),

    ("13 the walrus", "if (n := len(data)) > 10:\n    pass",
     "How many times is len called? Compare with the version that calls it "
     "twice."),

    ("14 a decorator", "@deco\ndef f():\n    pass",
     "When does deco run -- at definition or at call (Module 15)?"),

    ("15 default arguments", "def f(x=[]):\n    pass",
     "Where does the [] get built -- inside f, or outside? Now explain "
     "Module 02's mutable default trap in terms of what you see."),
]


def part_b() -> None:
    """Inspect a code object directly."""
    def outer(a: int, b: int = 2) -> object:
        x = a + b

        def inner() -> int:
            return x
        return inner

    c = outer.__code__
    print(f"\n{'=' * 70}\nPart B: the code object\n")
    for attr in ("co_name", "co_argcount", "co_varnames", "co_names",
                 "co_freevars", "co_cellvars", "co_stacksize", "co_nlocals"):
        print(f"  {attr:<14} {getattr(c, attr)}")
    inner_code = [k for k in c.co_consts if hasattr(k, "co_name")]
    print(f"\n  co_consts contains inner's code object: {bool(inner_code)}")
    if inner_code:
        print(f"  inner.co_freevars: {inner_code[0].co_freevars}")

    print(
        "\n  Q: co_cellvars on outer and co_freevars on inner name the same\n"
        "     variable. What is that variable, and which Module 04 concept are\n"
        "     you looking at?\n"
        "  Q: remove the inner function and re-run. What happens to\n"
        "     co_cellvars, and why?"
    )


if __name__ == "__main__":
    print(f"Python {sys.version.split()[0]} -- bytecode differs between "
          f"versions, which is itself the lesson.")
    for label, source, question in CASES:
        show(label, source, question)
    part_b()
