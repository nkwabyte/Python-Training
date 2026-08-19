# Solutions & Commentary — Module B07: Working with Text

## Exercise B07.1: String Immutability
- **Why this way:** Python strings cannot be modified in-place; all string methods (`.replace()`, `.upper()`) return new string objects.

## Exercise B07.2: Cleaning User Input
- **Why this way:** `.strip().lower()` normalizes whitespace and casing before comparison.

## Exercise B07.3: Split and Join
- **Why this way:** `", ".join(items)` is $O(N)$ efficient, avoiding repeated quadratic string concatenations.

## Exercise B07.4: Slicing Text
- **Why this way:** Python slicing `text[start:stop:step]` extracts substrings cleanly without index out-of-range errors.

## Exercise B07.5: Formatted Table Output
- **Why this way:** String alignment specifiers (`f"{name:<20} {price:>8.2f}"`) produce aligned terminal columns.
