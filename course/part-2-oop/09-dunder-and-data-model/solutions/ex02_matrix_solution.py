"""Solution 09.2 — A Matrix that behaves like a built-in type."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any


class Matrix:
    """A 2-D matrix of numbers, immutable."""

    __slots__ = ("_rows", "_hash")

    def __init__(self, rows: Sequence[Sequence[float]]) -> None:
        if not rows:
            raise ValueError("a matrix must have at least one row")
        widths = {len(r) for r in rows}
        if len(widths) != 1:
            raise ValueError(f"rows have differing lengths: {sorted(widths)}")
        if 0 in widths:
            raise ValueError("a matrix must have at least one column")
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                if not isinstance(cell, (int, float)) or isinstance(cell, bool):
                    raise TypeError(f"cell [{r},{c}] is {type(cell).__name__}")
        # tuple of tuples: immutable all the way down, so no caller can reach
        # in and change a row (Module 08's leak, prevented structurally).
        object.__setattr__(self, "_rows", tuple(tuple(r) for r in rows))
        object.__setattr__(self, "_hash", None)

    # -- representation --------------------------------------------------------
    def __repr__(self) -> str:
        return f"Matrix({[list(r) for r in self._rows]!r})"

    def __str__(self) -> str:
        width = max(len(f"{c:g}") for row in self._rows for c in row)
        return "\n".join(
            "[" + "  ".join(f"{c:>{width}g}" for c in row) + "]"
            for row in self._rows
        )

    def __format__(self, spec: str) -> str:
        if not spec:
            return str(self)
        cells = [[format(c, spec) for c in row] for row in self._rows]
        width = max(len(c) for row in cells for c in row)
        return "\n".join("[" + "  ".join(f"{c:>{width}}" for c in row) + "]"
                         for row in cells)

    # -- equality and hashing --------------------------------------------------
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self._rows == other._rows

    def __hash__(self) -> int:
        """HASHABLE, because TODO 1 made it immutable.

        The two decisions are one decision. A mutable Matrix must not be
        hashable (Module 03: a mutated key becomes unreachable), and an
        immutable one may as well be -- it costs one method and makes matrices
        usable as memoisation keys and as graph node labels.

        Cached because hashing is O(cells) and hashable objects get hashed
        repeatedly. __slots__ means we need object.__setattr__ to write it.
        """
        if self._hash is None:
            object.__setattr__(self, "_hash", hash(self._rows))
        return self._hash  # type: ignore[return-value]

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError(f"Matrix is immutable; cannot set {name!r}")

    # -- container -------------------------------------------------------------
    def __len__(self) -> int:
        """Number of ROWS.

        Chosen to match len() on a nested list, which is what a reader's
        intuition will reach for. Cell count is available as .size, named
        explicitly so it cannot be confused. When two answers are defensible,
        pick the one matching the nearest built-in and name the other.
        """
        return len(self._rows)

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self._rows), len(self._rows[0]))

    @property
    def size(self) -> int:
        return len(self._rows) * len(self._rows[0])

    def __getitem__(self, index: Any) -> Any:
        if isinstance(index, tuple):
            r, c = index
            return self._rows[r][c]
        if isinstance(index, slice):
            # type(self), not Matrix: a subclass slicing itself gets its own
            # type back rather than being silently downgraded.
            return type(self)(self._rows[index])
        return self._rows[index]

    def __iter__(self) -> Iterator[tuple[float, ...]]:
        """iter() over the underlying tuple: a FRESH iterator every call, so
        two consecutive for loops both work."""
        return iter(self._rows)

    def __contains__(self, value: object) -> bool:
        """Tests for a VALUE, not a row.

        The default derived from __iter__ would test row membership, so
        `5 in m` would be False for a matrix full of fives -- technically
        consistent and completely surprising. NumPy, pandas, and every
        spreadsheet treat a matrix as a container of cells. Match the mental
        model your users already have; leave row testing to
        `row in list(m)`, which says what it means.
        """
        return any(value == cell for row in self._rows for cell in row)

    def __bool__(self) -> bool:
        """A matrix is truthy if it EXISTS, not if it has non-zero entries.

        Following len(): every valid Matrix has at least one row, so every
        Matrix is truthy. Making an all-zero matrix falsy would mean
        `if matrix:` silently skipping a perfectly valid matrix of zeros -- a
        bug that surfaces only with certain data. NumPy refuses to answer this
        question at all (it raises on `if array:`), which is arguably the most
        honest option.
        """
        return True

    # -- operators -------------------------------------------------------------
    def __add__(self, other: object) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        if self.shape != other.shape:
            raise ValueError(f"shape mismatch: {self.shape} + {other.shape}")
        return Matrix([[a + b for a, b in zip(ra, rb, strict=True)]
                       for ra, rb in zip(self._rows, other._rows, strict=True)])

    def __sub__(self, other: object) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        return self + (-other)     # type: ignore[operator]

    def __mul__(self, other: object) -> Matrix:
        if isinstance(other, (int, float)):
            return Matrix([[c * other for c in row] for row in self._rows])
        if isinstance(other, Matrix):
            if self.shape[1] != other.shape[0]:
                raise ValueError(
                    f"cannot multiply {self.shape} by {other.shape}: "
                    f"inner dimensions {self.shape[1]} and {other.shape[0]} differ"
                )
            cols = list(zip(*other._rows, strict=True))
            return Matrix([[sum(a * b for a, b in zip(row, col, strict=True))
                            for col in cols] for row in self._rows])
        return NotImplemented

    __rmul__ = __mul__            # 3 * m as well as m * 3

    def __neg__(self) -> Matrix:
        return Matrix([[-c for c in row] for row in self._rows])

    def transpose(self) -> Matrix:
        return Matrix([list(col) for col in zip(*self._rows, strict=True)])

    # NotImplemented VERSUS ValueError -- the distinction in TODO 8:
    #
    #   NotImplemented means "I do not handle this TYPE". It is a message to
    #   the interpreter: try the other operand's reflected method, and if that
    #   also declines, raise TypeError. Returning it keeps the door open for a
    #   type written later to interoperate with Matrix.
    #
    #   ValueError means "correct type, impossible VALUE". Adding a 2x3 to a
    #   1x1 is not something any other operand could rescue; it is a caller
    #   error and must be reported immediately with the shapes, so the message
    #   says what went wrong.
    #
    # Returning ValueError where NotImplemented belongs breaks interoperability
    # silently. Returning NotImplemented where ValueError belongs produces
    # "unsupported operand type(s) for +: 'Matrix' and 'Matrix'", which is a
    # genuinely baffling message.


def verify() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])

    assert m.shape == (2, 3)
    assert m.size == 6
    assert len(m) == 2
    assert m[0] == (1, 2, 3)
    assert m[1, 2] == 6
    assert m[0:1] == Matrix([[1, 2, 3]])
    assert isinstance(m[0:1], Matrix)

    assert list(m) == [(1, 2, 3), (4, 5, 6)]
    assert list(m) == [(1, 2, 3), (4, 5, 6)], "two loops must both work"

    assert 5 in m and 99 not in m

    assert m + m == Matrix([[2, 4, 6], [8, 10, 12]])
    assert m * 2 == Matrix([[2, 4, 6], [8, 10, 12]])
    assert 2 * m == Matrix([[2, 4, 6], [8, 10, 12]])
    assert -m == Matrix([[-1, -2, -3], [-4, -5, -6]])
    assert m - m == Matrix([[0, 0, 0], [0, 0, 0]])

    a, b = Matrix([[1, 2], [3, 4]]), Matrix([[5, 6], [7, 8]])
    assert a * b == Matrix([[19, 22], [43, 50]])
    assert m.transpose() == Matrix([[1, 4], [2, 5], [3, 6]])

    for bad, exc in [(lambda: m + Matrix([[1]]), ValueError),
                     (lambda: m * m, ValueError),
                     (lambda: m + "x", TypeError),
                     (lambda: Matrix([[1, 2], [3]]), ValueError),
                     (lambda: Matrix([]), ValueError),
                     (lambda: Matrix([["a"]]), TypeError)]:
        try:
            bad()          # type: ignore[operator]
        except exc:
            pass
        else:
            raise AssertionError(f"expected {exc.__name__}")

    assert hash(m) == hash(Matrix([[1, 2, 3], [4, 5, 6]]))
    assert {m: "value"}[Matrix([[1, 2, 3], [4, 5, 6]])] == "value"

    try:
        m._rows = ()       # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Matrix must be immutable")

    assert "Matrix" in repr(m)
    assert eval(repr(m)) == m           # noqa: S307
    assert "\n" in str(m)
    assert f"{m:.2f}".count(".") == 6

    print("all matrix checks passed\n")
    print(m)
    print()
    print(f"{m * 1.5:.2f}")


if __name__ == "__main__":
    verify()
