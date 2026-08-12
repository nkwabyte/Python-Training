"""Solution 02.5 — Reference counting, cycles, and weakref.

Everything observed here is CPython-specific. See the answers at the bottom.
"""

from __future__ import annotations

import gc
import sys
import weakref


class Tracked:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ref: object | None = None

    def __repr__(self) -> str:
        return f"Tracked({self.name!r})"

    def __del__(self) -> None:
        print(f"    [{self.name} destroyed]")


def part1_refcounts() -> None:
    data = [1, 2, 3]
    print(f"    one name bound      : {sys.getrefcount(data)}")
    alias = data
    print(f"    two names bound     : {sys.getrefcount(data)}")
    holder = {"key": data}
    print(f"    plus a dict value   : {sys.getrefcount(data)}")
    del alias
    print(f"    after del alias     : {sys.getrefcount(data)}")
    del holder
    print(f"    after del holder    : {sys.getrefcount(data)}")


def part2_deterministic_destruction() -> None:
    obj = Tracked("solo")
    print("    before del")
    del obj
    print("    after del")


def part3_cycle() -> None:
    gc.collect()  # start from a clean slate
    a = Tracked("A")
    b = Tracked("B")
    a.ref = b
    b.ref = a       # cycle: each holds a strong reference to the other
    del a, b
    print("    names deleted -- note that nothing was destroyed")
    collected = gc.collect()
    print(f"    gc.collect() reclaimed {collected} objects")


def part4_weakref() -> None:
    gc.collect()
    a = Tracked("A-weak")
    b = Tracked("B-weak")
    a.ref = b                     # strong: A owns B
    b.ref = weakref.ref(a)        # weak: B merely observes A
    print(f"    weakref resolves to : {b.ref()!r}")
    del a, b
    print("    names deleted -- both should already be gone, no gc needed")


def part5_finding_the_leak() -> None:
    gc.collect()
    target = Tracked("hunted")

    in_a_list = [target]
    in_a_dict = {"cached": target}

    class Holder:
        pass

    holder = Holder()
    holder.attr = target  # type: ignore[attr-defined]

    referrers = [r for r in gc.get_referrers(target) if r is not locals()]
    print(f"    {len(referrers)} referrer(s) found:")
    for r in referrers:
        kind = type(r).__name__
        preview = repr(r)[:60]
        print(f"      {kind:<12} {preview}")

    del in_a_list, in_a_dict, holder, target
    gc.collect()


if __name__ == "__main__":
    for part in (
        part1_refcounts,
        part2_deterministic_destruction,
        part3_cycle,
        part4_weakref,
        part5_finding_the_leak,
    ):
        print(f"\n=== {part.__name__} ===")
        part()
    print()


ANSWERS = """
1. WHY DOES getrefcount REPORT ONE EXTRA?

   Calling getrefcount(data) passes the object as an argument, which binds it
   to the function's parameter name -- a temporary extra reference that exists
   for exactly the duration of the call. So the reported number is always your
   count plus one. (Since 3.11 the exact bookkeeping around temporaries has
   shifted with the specialising interpreter, so treat the absolute number as
   indicative and the DELTAS as the meaningful signal.)

2. WHEN DID __del__ RUN IN PART 2?

   Between "before del" and "after del". The `del` statement removed the last
   reference, the refcount hit zero, and CPython freed the object immediately
   and synchronously -- inside the del statement, not at some later point.

   This determinism is a genuine CPython advantage over tracing-GC languages,
   and it is why `with open(...)` and even the sloppier `open(...).read()`
   happen to work. It is ALSO a trap: code that relies on it silently breaks on
   PyPy, and breaks on CPython the moment the object gets caught in a cycle or
   captured by a traceback. Use context managers.

3. THE GAP IN PART 3

   Between the deletion and gc.collect(), A and B were UNREACHABLE from any
   name -- genuinely garbage -- but NOT FREED. Their refcounts were each still
   1, held by the other. Refcounting cannot see that the group as a whole is
   unreachable; it only sees per-object counts.

   In a long-running server that gap means memory climbs between collections,
   and collection pauses grow with the number of surviving objects. A service
   that creates many cyclic structures per request (parent pointers in a parsed
   tree, observer registries, ORM identity maps) can spend real CPU in gc. The
   fixes: break the cycle with weakref, clear references explicitly when done,
   or tune gc thresholds. Some high-throughput services disable the cycle
   collector entirely (gc.freeze() after startup, gc.disable()) and manage
   lifetimes manually -- an advanced move with real risk.

4. WHAT DOES A DEAD WEAKREF RETURN?

   None. weakref.ref objects are CALLED to dereference: `r()` gives the object,
   or None if it has been collected. Therefore every holder must check:

       obj = self._ref()
       if obj is None:
           ...handle the gone case...

   Never `self._ref().method()`. The object can vanish between two lines of
   your own code if another thread drops the last strong reference.

   Note also: not everything is weak-referenceable. Instances of your own
   classes are; int, str, tuple, list and dict instances are not, unless
   subclassed. And a class using __slots__ needs '__weakref__' in the slots.

5. REAL-WORLD UNINTENDED STRONG REFERENCES

   The classic four:
     - An unbounded module-level dict used as a cache. Nothing ever evicts, so
       every object ever cached lives forever. Fix: functools.lru_cache with a
       maxsize, or weakref.WeakValueDictionary, or an explicit TTL.
     - Event listener / callback registries that keep strong references to
       subscribers, so an "unregistered" object is still alive. Fix:
       WeakMethod / WeakSet.
     - A captured traceback. `except Exception as e:` binds a traceback that
       references every frame and therefore every local in the whole call
       stack. Python deletes `e` at the end of the except block for exactly
       this reason -- but storing the exception elsewhere defeats that.
     - Logging or metrics that stash whole request objects.

   The tool for diagnosing all of them is the one in part5: gc.get_referrers,
   plus tracemalloc snapshots (Module 23) to see what is growing.

6. WHICH OBSERVATIONS WOULD BE FALSE ON PyPy?

   Almost all of parts 1, 2 and 4. PyPy does not use reference counting; it
   uses a tracing garbage collector. Consequences:
     - sys.getrefcount does not exist in a meaningful form.
     - Objects are NOT destroyed at the moment the last name disappears.
       __del__ runs at some unspecified later time, or possibly not before
       interpreter exit.
     - Cycles are collected by the same mechanism as everything else, so part 3
       and part 4 are not distinguishable there.
   This is the practical reason "use with, never rely on __del__" is a rule and
   not a style preference.
"""
