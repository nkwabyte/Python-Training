# Module B03 — Making Decisions

**Level:** Beginner  |  **Time:** L3 E5  |  **Prerequisite:** Module B02

---

## Why this module

Programs become useful the moment they can take different paths depending on
their data. This module teaches you how Python asks questions and branches on
the answers. You will learn how comparisons work, how indentation defines
blocks of code, how `if`, `elif`, and `else` combine, how boolean logic works,
and how to keep your conditional logic readable and flat rather than deeply nested.

## What you will be able to do

- Use comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) to produce boolean values.
- Write branching logic using `if`, `elif`, and `else`.
- Combine conditions with `and`, `or`, and `not`.
- Understand truthiness and which values evaluate to `False`.
- Refactor deeply nested conditionals into clean guard clauses.
- Use pattern matching (`match` / `case`) for multi-way branches.

## Concept sections

1. **Comparisons and booleans** — Equality (`==`) vs assignment (`=`), inequality, ordering, and chaining (`0 <= age < 18`).
2. **The `if` statement and indentation** — How Python uses 4 spaces to define blocks; execution flow.
3. **Multi-way branching with `elif` and `else`** — Mutual exclusion, order of evaluation, and default branches.
4. **Logical operators and short-circuiting** — `and`, `or`, `not`; why `x or y` stops evaluating once truth is determined.
5. **Truthiness in Python** — Truth value testing; empty sequences (`""`, `[]`, `{}`), `0`, and `None` evaluate to `False`.
6. **Flattening nested decisions** — Guard clauses, early returns, and avoiding the "pyramid of doom".
7. **Structural pattern matching** — A first look at `match` and `case` introduced in Python 3.10+.

## Worked example

```python
def check_admission(age: int, has_ticket: bool, is_vip: bool = False) -> str:
    """Determine venue entry status based on credentials."""
    # Guard clauses keep the main logic un-nested
    if is_vip:
        return "Admitted (VIP Access)"
    if not has_ticket:
        return "Denied: Ticket required"
    if age < 18:
        return "Denied: Must be 18 or older"
    
    return "Admitted (Standard)"

print(check_admission(20, has_ticket=True))
print(check_admission(16, has_ticket=True))
print(check_admission(19, has_ticket=False, is_vip=True))
```

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_grades.ipynb` | Map numeric scores to letter grades using `if/elif/else`. |
| `ex02_truthiness.ipynb` | Explore truthiness of empty collections, zero, and strings. |
| `ex03_password_rules.ipynb` | Validate password complexity with combined boolean conditions. |
| `ex04_flatten.ipynb` | Refactor a 4-level nested conditional into clear guard clauses. |
| `ex05_ticket_price.ipynb` | Calculate discounted ticket prices with age, residency, and promo codes. |

## Common mistakes this module must address

- **Confusing `=` with `==`** — `=` assigns a name, `==` tests for equality.
- **Checking booleans with `== True`** — Write `if is_valid:` instead of `if is_valid == True:`.
- **String comparison traps** — `"10" > "2"` evaluates to `False` because alphabetical comparison is used.
- **Misunderstanding `or` chaining** — `if fruit == "apple" or "banana":` is always truthy because `"banana"` is truthy; write `if fruit in ("apple", "banana"):`.
- **Floating point equality** — Using `a == b` on computed floats instead of `math.isclose()`.

## Self check questions

1. What is the value of `x` after: `x = 5 == 5`?
2. Why is `bool([])` equal to `False`?
3. In the expression `a and b`, if `a` is false, does Python evaluate `b`?
4. How would you refactor `if user: if user.is_active: if user.has_permission: do_thing()`?
5. When should you choose `match/case` over an `if/elif/else` chain?

## Going deeper

- Python Documentation: More Control Flow Tools (`if` statements and `match` statements)
- PEP 634: Structural Pattern Matching Specification
- Real Python: Conditional Statements in Python
