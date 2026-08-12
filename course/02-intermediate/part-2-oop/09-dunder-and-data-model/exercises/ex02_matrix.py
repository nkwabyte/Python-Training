"""Exercise 09.2 — A Matrix that behaves like a built-in type.

Implement enough of the data model that Matrix works with Python's syntax
rather than beside it. The tests are the specification.

Run:  python ex02_matrix.py
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence


class Matrix:
    """A 2-D matrix of floats.

    TODO 1  __init__(rows) where rows is a sequence of equal-length sequences.
            Validate: non-empty, rectangular, numeric. Store immutably enough
            that a caller cannot reach in and change it (Module 08).

    TODO 2  __repr__ -- unambiguous, ideally reconstructing.
            __str__  -- an aligned grid a human can read.

    TODO 3  __eq__ and __hash__. Decide whether Matrix is hashable AT ALL and
            justify it in a comment. (Think about what you chose in TODO 1.)

    TODO 4  __len__  -- number of rows. Say why that is the right answer rather
            than the number of cells, in one comment line.

    TODO 5  __getitem__ supporting THREE index forms:
              m[1]        -> a row (as a tuple)
              m[1, 2]     -> a single cell
              m[0:2]      -> a Matrix of those rows -- note: your OWN type
            Use type(self)(...) for the slice case, not Matrix(...), and say why.

    TODO 6  __iter__ yielding rows. Two consecutive for loops must both work.

    TODO 7  __contains__ -- is a VALUE present anywhere in the matrix?
            Note this differs from the default derived from __iter__, which
            would test whether a ROW is present. Decide which is less
            surprising and write down the reasoning.

    TODO 8  __add__ (elementwise, same shape), __mul__ (by a scalar OR by
            another Matrix as matrix multiplication), __rmul__, __neg__.
            Return NotImplemented for types you do not handle, and raise
            ValueError for shape mismatches. Explain the difference between
            those two responses in a comment -- it is not arbitrary.

    TODO 9  __bool__ -- what should an all-zero matrix be? Justify.

    TODO 10 __format__ supporting f"{m:.2f}" to control cell formatting.

    TODO 11 transpose() and a `shape` property.
    """


def verify() -> None:
    m = Matrix([[1, 2, 3], [4, 5, 6]])

    assert m.shape == (2, 3)
    assert len(m) == 2
    assert m[0] == (1, 2, 3)
    assert m[1, 2] == 6
    assert m[0:1] == Matrix([[1, 2, 3]])
    assert isinstance(m[0:1], Matrix)

    assert list(m) == [(1, 2, 3), (4, 5, 6)]
    assert list(m) == [(1, 2, 3), (4, 5, 6)], "two loops must both work"

    assert 5 in m
    assert 99 not in m

    assert m + m == Matrix([[2, 4, 6], [8, 10, 12]])
    assert m * 2 == Matrix([[2, 4, 6], [8, 10, 12]])
    assert 2 * m == Matrix([[2, 4, 6], [8, 10, 12]])
    assert -m == Matrix([[-1, -2, -3], [-4, -5, -6]])

    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    assert a * b == Matrix([[19, 22], [43, 50]])

    assert m.transpose() == Matrix([[1, 4], [2, 5], [3, 6]])

    try:
        m + Matrix([[1]])
    except ValueError:
        pass
    else:
        raise AssertionError("shape mismatch must raise ValueError")

    assert (m + "not a matrix") is NotImplemented or True   # see the comment
    try:
        m + "not a matrix"      # type: ignore[operator]
    except TypeError:
        pass
    else:
        raise AssertionError("adding a str must raise TypeError")

    assert "Matrix" in repr(m)
    assert "\n" in str(m)
    assert f"{m:.2f}".count(".") >= 6

    assert bool(Matrix([[0, 0], [0, 0]])) is False or True   # your call
    print("all matrix checks passed\n")
    print(m)
    print()
    print(f"{m * 1.5:.2f}")


if __name__ == "__main__":
    verify()
