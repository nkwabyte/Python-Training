"""Exercise 08.1 — The attribute lookup ladder.

Twelve predictions. Write your answer AND the rung number (1-5) that the lookup
stopped at, before running.

    1 data descriptor on the type   2 instance __dict__
    3 the type and its bases        4 __getattr__        5 AttributeError

Run:  python ex01_lookup_lab.py
"""

from __future__ import annotations

from functools import cached_property


class Base:
    shared_list: list[str] = []
    shared_int = 0
    name = "base"

    def __init__(self) -> None:
        self.own = "instance"

    def method(self) -> str:
        return "from Base"

    @property
    def computed(self) -> str:
        return "computed"

    @cached_property
    def expensive(self) -> str:
        print("    (expensive ran)")
        return "cached"


def q01() -> None:
    # PREDICTION:                         rung:
    a, b = Base(), Base()
    a.shared_list.append("x")
    print("q01", b.shared_list)


def q02() -> None:
    # PREDICTION:                         rung:
    Base.shared_list = []   # reset -- q01 mutated the CLASS attribute, and it
                            # is still mutated. That cross-contamination between
                            # two functions that share no variables is itself
                            # the lesson of q01. Note how easily it hid here.
    a, b = Base(), Base()
    a.shared_list = ["x"]
    print("q02", b.shared_list, a.__dict__.get("shared_list"))


def q03() -> None:
    # PREDICTION:                         rung:
    a = Base()
    a.shared_int += 1
    print("q03", a.shared_int, Base.shared_int)


def q04() -> None:
    # PREDICTION:                         rung:
    a = Base()
    print("q04", a.name, a.__dict__.get("name"))


def q05() -> None:
    # PREDICTION:                         rung:
    a = Base()
    a.__dict__["computed"] = "sneaky"
    print("q05", a.computed, a.__dict__["computed"])


def q06() -> None:
    # PREDICTION:                         rung:
    a = Base()
    try:
        a.computed = "assigned"
        print("q06", a.computed)
    except Exception as exc:
        print("q06", type(exc).__name__)


def q07() -> None:
    # PREDICTION: how many times does "(expensive ran)" appear?
    a = Base()
    print("q07", a.expensive, a.expensive, a.expensive)
    print("q07 in __dict__?", "expensive" in a.__dict__)


def q08() -> None:
    # PREDICTION:                         rung:
    a = Base()
    print("q08", type(Base.method).__name__, type(a.method).__name__)


def q09() -> None:
    # PREDICTION:                         rung:
    a = Base()
    a.method = lambda: "shadowed"       # type: ignore[method-assign]
    print("q09", a.method(), Base.method(a))


class WithGetattr(Base):
    def __getattr__(self, name: str) -> str:
        return f"<generated {name}>"


def q10() -> None:
    # PREDICTION:                         rung:
    w = WithGetattr()
    print("q10", w.own, w.anything_at_all)


def q11() -> None:
    # PREDICTION:                         rung:
    w = WithGetattr()
    try:
        print("q11", w.computed)
    except Exception as exc:
        print("q11", type(exc).__name__)
    # Careful. What happens if the property itself raises AttributeError?
    # Try adding `raise AttributeError("boom")` inside Base.computed and
    # re-running. Explain the result. This is a genuinely nasty real-world bug.


class Mangled:
    def __init__(self) -> None:
        self.__hidden = "secret"

    def reveal(self) -> str:
        return self.__hidden


def q12() -> None:
    # PREDICTION: what are the keys of m.__dict__?
    m = Mangled()
    print("q12", list(m.__dict__), m.reveal())
    try:
        print("q12", m.__hidden)          # type: ignore[attr-defined]
    except AttributeError as exc:
        print("q12 AttributeError:", exc)


# TODO -------------------------------------------------------------------------
class Tracer:
    """Implement __getattribute__ so that EVERY attribute access is logged,
    then use it to trace the ladder on a real object.

    Requirements:
      - log the attribute name to self._log
      - delegate to super().__getattribute__ for the actual lookup
      - do NOT infinitely recurse (accessing self._log inside
        __getattribute__ is itself an attribute access -- this is the trap)

    Then answer:
      - which of q01-q12 above would produce a DIFFERENT log if you used
        __getattr__ instead of __getattribute__?
      - why is __getattribute__ almost never the right tool in production code?
    """

    def __init__(self) -> None:
        self._log: list[str] = []
        self.value = 42


if __name__ == "__main__":
    for fn in [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12]:
        fn()
