"""Exercise 10.1 — MRO predictions.

For each case: write the MRO you expect, then the output of the super() chain,
THEN run. One of them does not compile at all -- predict which and why.

Run:  python ex01_mro_lab.py
"""

from __future__ import annotations


def show(cls: type) -> None:
    print(f"  {cls.__name__:<10} MRO: {' -> '.join(c.__name__ for c in cls.__mro__)}")


# --- q01: the diamond ---------------------------------------------------------
class A:
    def greet(self) -> str: return "A"


class B(A):
    def greet(self) -> str: return "B->" + super().greet()


class C(A):
    def greet(self) -> str: return "C->" + super().greet()


class D(B, C):
    def greet(self) -> str: return "D->" + super().greet()


# --- q02: order matters -------------------------------------------------------
class D2(C, B):
    def greet(self) -> str: return "D2->" + super().greet()


# --- q03: three levels --------------------------------------------------------
class Base:
    def run(self) -> list[str]: return ["Base"]


class Left(Base):
    def run(self) -> list[str]: return ["Left", *super().run()]


class Right(Base):
    def run(self) -> list[str]: return ["Right", *super().run()]


class Middle(Left):
    def run(self) -> list[str]: return ["Middle", *super().run()]


class Bottom(Middle, Right):
    def run(self) -> list[str]: return ["Bottom", *super().run()]


# --- q04: a mixin, in both positions ------------------------------------------
class UpperMixin:
    def render(self) -> str: return super().render().upper()   # type: ignore[misc]


class Widget:
    def render(self) -> str: return "widget"


class GoodOrder(UpperMixin, Widget): ...
class BadOrder(Widget, UpperMixin): ...


# --- q05: a broken cooperative chain ------------------------------------------
class Root:
    def __init__(self, **kwargs: object) -> None:
        self.initialised = ["Root"]


class Alpha(Root):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.initialised.append("Alpha")


class Beta(Root):
    def __init__(self, **kwargs: object) -> None:
        # BUG: no super().__init__() call
        self.initialised = getattr(self, "initialised", [])
        self.initialised.append("Beta")


class Gamma(Alpha, Beta):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.initialised.append("Gamma")


# --- q06: which fails to linearise? -------------------------------------------
def q06() -> None:
    print("q06: which of these class statements raises, and why?")

    class X: ...
    class Y(X): ...

    for label, bases in [("Z1(X, Y)", (X, Y)), ("Z2(Y, X)", (Y, X))]:
        try:
            cls = type("Z", bases, {})
            print(f"  {label:<10} OK   -> "
                  f"{' -> '.join(c.__name__ for c in cls.__mro__)}")
        except TypeError as exc:
            print(f"  {label:<10} TypeError: {exc}")


# --- q07: super() outside a method --------------------------------------------
def q07() -> None:
    # PREDICTION: does the zero-argument form work here?
    print("q07")

    class P:
        def hello(self) -> str: return "P"

    class Q(P):
        def hello(self) -> str:
            def inner() -> str:
                try:
                    return super().hello()      # type: ignore[misc]
                except Exception as exc:
                    return f"{type(exc).__name__}: {exc}"
            return inner()

    print("  ", Q().hello())
    # Then answer: what does the zero-argument super() actually rely on? Inspect
    # Q.hello.__code__.co_freevars. What must the compiler have put there?


# --- q08: super() with explicit arguments -------------------------------------
def q08() -> None:
    print("q08")

    class R:
        def hello(self) -> str: return "R"

    class S(R):
        def hello(self) -> str: return "S->" + super(S, self).hello()

    class T(S):
        def hello(self) -> str:
            # PREDICTION: what does super(S, self) do HERE, in T?
            return "T->" + super(S, self).hello()

    print("  ", T().hello())


if __name__ == "__main__":
    print("q01 diamond")
    show(D); print("   ", D().greet())
    print("q02 reversed bases")
    show(D2); print("   ", D2().greet())
    print("q03 three levels")
    show(Bottom); print("   ", " ".join(Bottom().run()))
    print("q04 mixin position")
    show(GoodOrder); print("   ", GoodOrder().render())
    show(BadOrder); print("   ", BadOrder().render())
    print("q05 broken cooperative chain")
    show(Gamma); print("   ", Gamma().initialised)
    print("    which classes were skipped, and could Beta have known?")
    q06()
    q07()
    q08()
