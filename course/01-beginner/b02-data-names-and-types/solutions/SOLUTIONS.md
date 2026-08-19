# Solutions & Commentary — Module B02: Data, Names, and Types

## Exercise B02.1: Labels, Not Boxes
- **Why this way:** Python names are labels pointing to objects in memory. When you execute `a = [1, 2]; b = a; b.append(3)`, both `a` and `b` point to the same list. Reassignment (`b = [4, 5]`) rebinds the label `b` without modifying the list `a` points to.
- **The detail most people miss:** `int` and `str` are immutable, so rebinding behaves like a copy conceptually, but mutable containers (`list`, `dict`) reveal shared object references.

## Exercise B02.2: Calculator
- **Why this way:** Converting `input()` with `float()` or `int()` before arithmetic is mandatory because string concatenation (`"2" + "2" == "22"`) differs from numeric addition (`2 + 2 == 4`).
- **Near misses:** Forgetting to handle `ValueError` when non-numeric text is supplied.

## Exercise B02.3: Type Conversions
- **Why this way:** `int("3.5")` fails with `ValueError` because `int()` expects integer literals in base 10. You must convert via `int(float("3.5"))` or parse explicitly.

## Exercise B02.4: Formatted Receipt
- **Why this way:** f-strings with format specifiers like `f"{total:.2f}"` format float numbers to two decimal places cleanly.

## Exercise B02.5: Naming Worksheet
- **Why this way:** Descriptive `snake_case` variable names (`total_price`, `item_count`) convey intent better than abbreviations (`tp`, `cnt`).
