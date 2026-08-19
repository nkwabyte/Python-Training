# Solutions & Commentary — Module B04: Loops and Repetition

## Exercise B04.1: Countdown Timer
- **Why this way:** `while count > 0:` loop decrements the counter explicitly until the stopping condition is satisfied.

## Exercise B04.2: Accumulator Pattern
- **Why this way:** Initialize total before the loop (`total = 0.0`), update inside the loop body (`total += item`), and return after loop completion.

## Exercise B04.3: Guessing Game
- **Why this way:** `while True:` loop paired with conditional `break` provides clean multi-point exit criteria based on user input.

## Exercise B04.4: Times Table
- **Why this way:** Nested `for` loops iterate row-by-row and column-by-column with formatted output spacing.

## Exercise B04.5: Enumerate
- **Why this way:** `enumerate(items, start=1)` generates `(index, item)` pairs directly without managing a manual index variable.

## Exercise B04.6: Fixing Infinite Loops
- **Why this way:** Ensure the loop variable is guaranteed to move toward the termination condition on every single branch inside the loop body.
