"""Exercise 10.4 — Four mixins that compose, one that does not.

Run:  python ex04_mixins.py
"""

from __future__ import annotations

from typing import Any

# TODO 1-4: write four STATELESS mixins.
#
#   ReprMixin        __repr__ from vars(self)
#   ComparableMixin  __eq__, __lt__ and total ordering from a _key() method the
#                    host must provide. Document that requirement.
#   DictMixin        to_dict() / from_dict() using the host's annotations
#   ValidateMixin    validate() calling every method named _check_*
#
# Constraints for all four:
#   - no __init__, no instance attributes
#   - depend only on a small documented interface
#   - work in any order relative to each other
#   - each must work on a host class that knows nothing about the others


# TODO 5: write one STATEFUL mixin that breaks -------------------------------
#
#   AuditMixin  with an __init__ that sets self._audit_log = [] and an
#               audit(msg) method
#
# Then demonstrate, with running code, three ways it goes wrong:
#   (a) a host class whose __init__ does not call super().__init__()
#   (b) two stateful mixins whose __init__ keyword arguments collide
#   (c) the mixin placed after the concrete base
#
# Then rewrite the same capability as COMPOSITION (self._audit = AuditLog())
# and show that all three problems disappear.
#
# Finally answer: what did composition cost you, in lines and in call-site
# verbosity? Is that price ever too high?


def verify() -> None:
    class Product(ReprMixin, ComparableMixin, DictMixin, ValidateMixin):  # type: ignore[name-defined]
        def __init__(self, name: str, price: float) -> None:
            self.name, self.price = name, price

        def _key(self) -> tuple[Any, ...]:
            return (self.price, self.name)

        def _check_price(self) -> None:
            if self.price < 0:
                raise ValueError("price must not be negative")

    a = Product("widget", 10.0)
    b = Product("gizmo", 5.0)

    assert "Product(" in repr(a) and "widget" in repr(a)
    assert b < a
    assert a == Product("widget", 10.0)
    assert sorted([a, b])[0] is b
    assert a.to_dict() == {"name": "widget", "price": 10.0}
    a.validate()

    bad = Product("broken", -1.0)
    try:
        bad.validate()
    except ValueError:
        pass
    else:
        raise AssertionError("validate must run _check_ methods")

    # order among the mixins must not matter
    class Reordered(ValidateMixin, DictMixin, ComparableMixin, ReprMixin):  # type: ignore[name-defined]
        def __init__(self, name: str, price: float) -> None:
            self.name, self.price = name, price

        def _key(self) -> tuple[Any, ...]:
            return (self.price, self.name)

    assert "Reordered(" in repr(Reordered("x", 1.0))

    print("all mixin checks passed")


if __name__ == "__main__":
    verify()
