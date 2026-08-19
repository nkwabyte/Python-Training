# Solutions & Commentary — Module B03: Making Decisions

## Exercise B03.1: Grade Mapping
- **Why this way:** Sequential `if/elif/else` chains with descending threshold bounds (`score >= 90`, `elif score >= 80`) avoid redundant range comparisons like `80 <= score < 90`.

## Exercise B03.2: Truthiness
- **Why this way:** In Python, empty sequences (`""`, `[]`, `()`), numeric zero (`0`, `0.0`), and `None` evaluate to `False` in boolean contexts. Write `if items:` instead of `if len(items) > 0:`.

## Exercise B03.3: Password Validation
- **Why this way:** Combining boolean conditions with `and` allows early termination via short-circuit evaluation.

## Exercise B03.4: Flattening Conditionals
- **Why this way:** Guard clauses at the top of a function with early returns keep the primary happy path at zero indentation levels.

## Exercise B03.5: Ticket Pricing
- **Why this way:** Compute base price first, then apply multiplicative discount multipliers sequentially.
