"""Solution 08.4 — Does __slots__ actually matter?"""

from __future__ import annotations

import sys
import timeit
import tracemalloc
import weakref
from dataclasses import dataclass
from functools import cached_property


class PointDict:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z


class PointSlots:
    __slots__ = ("x", "y", "z")

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z


def measure_single_instance() -> None:
    d, s = PointDict(1.0, 2.0, 3.0), PointSlots(1.0, 2.0, 3.0)
    d_obj = sys.getsizeof(d)
    d_dict = sys.getsizeof(d.__dict__)
    s_obj = sys.getsizeof(s)

    print("single instance")
    print(f"  PointDict  object {d_obj:>4} + __dict__ {d_dict:>4} = {d_obj + d_dict:>4} bytes")
    print(f"  PointSlots object {s_obj:>4} + no dict       = {s_obj:>4} bytes")
    print(f"  saving {(d_obj + d_dict) - s_obj} bytes "
          f"({1 - s_obj / (d_obj + d_dict):.0%})")
    print(
        "\n  THE TRAP: sys.getsizeof(obj) does NOT follow references. Reporting\n"
        "  only the object size makes __slots__ look like it saves 8 bytes; the\n"
        "  __dict__ is where the weight is.\n"
        "\n  WHAT IT STILL MISSES: the float objects themselves. x, y and z are\n"
        "  POINTERS to heap floats (Module 02), each ~24 bytes. Neither version\n"
        "  stores the numbers inline. That is what NumPy fixes and __slots__\n"
        "  cannot: __slots__ removes the per-instance dict, not the boxing.\n"
        "  For a million 3-D points, the floats outweigh everything else, and\n"
        "  the real answer is a NumPy array (Module 29), not __slots__."
    )


def measure_at_scale(counts: tuple[int, ...] = (1_000, 10_000, 100_000, 1_000_000)) -> None:
    print(f"\nat scale (tracemalloc)\n  {'count':>10}{'dict MB':>12}{'slots MB':>12}"
          f"{'saved MB':>12}{'saved %':>10}")
    for n in counts:
        results = {}
        for cls in (PointDict, PointSlots):
            tracemalloc.start()
            objs = [cls(float(i), 0.0, 0.0) for i in range(n)]
            current, _peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results[cls.__name__] = current / 1_048_576
            del objs
        d, s = results["PointDict"], results["PointSlots"]
        print(f"  {n:>10,}{d:>12.2f}{s:>12.2f}{d - s:>12.2f}{1 - s / d:>9.0%}")

    print(
        "\n  tracemalloc, not sum(getsizeof(...)): getsizeof is per-object and\n"
        "  ignores allocator overhead, the list holding the objects, and shared\n"
        "  references. tracemalloc measures what the PROCESS actually\n"
        "  allocated, which is the number that decides whether you fit in RAM."
    )


def measure_access_speed() -> None:
    setup = "from __main__ import PointDict, PointSlots\np = {cls}(1.0, 2.0, 3.0)"
    print("\naccess speed (ns per operation)")
    print(f"  {'operation':<22}{'dict':>10}{'slots':>10}{'ratio':>10}")
    cases = [
        ("read attribute", "p.x", 2_000_000),
        ("write attribute", "p.x = 1.0", 2_000_000),
        ("create instance", "{cls}(1.0, 2.0, 3.0)", 500_000),
    ]
    for label, stmt, number in cases:
        times = {}
        for cls in ("PointDict", "PointSlots"):
            s = stmt.format(cls=cls)
            times[cls] = min(timeit.repeat(
                s, setup.format(cls=cls), number=number, repeat=5)) / number * 1e9
        print(f"  {label:<22}{times['PointDict']:>10.1f}{times['PointSlots']:>10.1f}"
              f"{times['PointDict'] / times['PointSlots']:>9.2f}x")

    print(
        "\n  IS SPEED A REASON ON ITS OWN? No. Reads and writes differ by a few\n"
        "  nanoseconds -- real, and swamped by anything else in a real program.\n"
        "  CREATION differs most, because the dict version must allocate and\n"
        "  initialise a hash table per instance while the slots version fills a\n"
        "  fixed array. So __slots__ helps most in exactly the workload where\n"
        "  you also care about memory: creating very many short-lived objects.\n"
        "  Memory is the reason; speed is a bonus that comes along with it."
    )


def what_breaks() -> None:
    print("\nwhat __slots__ takes away")

    p = PointSlots(1.0, 2.0, 3.0)
    try:
        p.w = 4.0                      # type: ignore[attr-defined]
        print("  1. new attribute      : allowed (unexpected!)")
    except AttributeError as exc:
        print(f"  1. new attribute      : AttributeError -- {exc}")

    print(f"  2. __dict__           : {hasattr(p, '__dict__')}")

    try:
        weakref.ref(p)
        print("  3. weakref            : works")
    except TypeError as exc:
        print(f"  3. weakref            : TypeError -- {exc}")

    class WithCached:
        __slots__ = ("n",)

        def __init__(self, n: int) -> None:
            self.n = n

        @cached_property
        def doubled(self) -> int:
            return self.n * 2

    try:
        WithCached(21).doubled
        print("  4. cached_property    : works")
    except TypeError as exc:
        print(f"  4. cached_property    : TypeError -- {exc}")

    class A:
        __slots__ = ("a",)

    class B:
        __slots__ = ("b",)

    try:
        class C(A, B):                 # noqa: B903
            __slots__ = ()
        print("  5. multiple inheritance: works")
    except TypeError as exc:
        print(f"  5. multiple inheritance: TypeError -- {exc}")

    print(
        "\n  DOES IT MATTER FOR:\n"
        "  (a) a Point in a physics engine -- NO, and __slots__ is right here.\n"
        "      Millions of instances, a fixed three-field shape that will never\n"
        "      grow, no weakrefs, no caching. This is the canonical case.\n"
        "  (b) a User in a web application -- YES, it matters, and __slots__ is\n"
        "      wrong. You hold hundreds of Users, not millions, so the saving is\n"
        "      invisible; meanwhile ORMs, serializers, and mocking libraries all\n"
        "      expect to set attributes dynamically, and cached_property is\n"
        "      exactly what you want for a computed permission set.\n"
        "  (c) a Node in a parser -- YES to __slots__, with a caveat. Millions of\n"
        "      nodes, fixed shape: ideal. But parse trees usually need PARENT\n"
        "      pointers, and a strong parent reference creates a cycle\n"
        "      (Module 02). If you want weak parent references you must add\n"
        "      '__weakref__' to __slots__ explicitly."
    )


def with_dataclass() -> None:
    @dataclass(slots=True)
    class PointDataclass:
        x: float
        y: float
        z: float

    n = 200_000
    print("\nhand-written __slots__ vs @dataclass(slots=True)")
    for cls in (PointSlots, PointDataclass):
        tracemalloc.start()
        objs = [cls(float(i), 0.0, 0.0) for i in range(n)]
        current, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        del objs
        print(f"  {cls.__name__:<20}{current / 1_048_576:>8.2f} MB")

    print(
        "\n  Identical memory -- @dataclass(slots=True) generates exactly the\n"
        "  same __slots__ declaration. Line count: 5 hand-written versus 4\n"
        "  declarative, and the dataclass also gives you __init__, __repr__,\n"
        "  __eq__ and keyword construction for free.\n"
        "\n  WHY THE ANSWER CHANGED IN 3.10: before it, @dataclass could not\n"
        "  generate __slots__ at all, so you had to choose between dataclass\n"
        "  convenience and slots memory, or hand-write both and keep them in\n"
        "  sync. Since 3.10, slots=True removes the trade entirely. Write the\n"
        "  dataclass. (Module 11.)"
    )


if __name__ == "__main__":
    measure_single_instance()
    measure_at_scale((1_000, 10_000, 100_000, 500_000))
    measure_access_speed()
    what_breaks()
    with_dataclass()
