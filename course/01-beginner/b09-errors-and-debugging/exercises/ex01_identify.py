"""
B09 When Things Go Wrong: Errors and Debugging
Exercise: ex01_identify.py

Goal
----
Match twelve tracebacks to their causes.

Run it
------
    python ex01_identify.py

Work through the TODOs in order. Run the file as often as you like; the
self-check at the bottom fails until the exercise is done. Do not read the
solution until your own attempt runs, and when you do read it, ask whether
yours is wrong or merely different.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# TODO 1. Read the goal above and write down, in a comment here, what the
#         inputs are and what the output should be. Do this before any code.
#
# TODO 2. Implement the function below. Keep it small: if you cannot name what
#         it does in one sentence, it is doing more than one thing.
#
# TODO 3. Add your own check to CHECKS at the bottom for a case you think the
#         given checks miss. Every exercise in this course expects at least one.
# ---------------------------------------------------------------------------


def solve():
    """Implement the exercise described in the module README.

    Replace the raise below with your own work, and give this function a real
    name, real parameters, and a real return type once you know what they are.
    """
    raise NotImplementedError("TODO: implement solve()")


# ---------------------------------------------------------------------------
# Self-check
#
# Each entry is (description, callable returning True when the check passes).
# The starter ships with one check: that you have implemented anything at all.
# The written lesson replaces it with the real cases for this exercise.
# ---------------------------------------------------------------------------


def _is_implemented() -> bool:
    try:
        solve()
    except NotImplementedError:
        return False
    except Exception:
        # Your code ran and raised something else. That is progress, not a pass.
        return False
    return True


CHECKS = [
    ("solve() is implemented and does not raise", _is_implemented),
]


def _run_checks() -> int:
    failures = 0
    for description, check in CHECKS:
        try:
            passed = bool(check())
        except Exception as exc:  # noqa: BLE001 - a broken check is a failure
            passed = False
            description = "{} (raised {})".format(description, exc.__class__.__name__)
        print("{}  {}".format("PASS" if passed else "FAIL", description))
        failures += 0 if passed else 1

    print()
    if failures:
        print("{} of {} checks failing. Keep going.".format(failures, len(CHECKS)))
    else:
        print("All {} checks passing.".format(len(CHECKS)))
    return failures


if __name__ == "__main__":
    raise SystemExit(1 if _run_checks() else 0)
