# Solutions & Commentary — Module B06: Functions

## Exercise B06.1: Unit Converter
- **Why this way:** Functions should accept arguments and return values rather than interacting with global state.

## Exercise B06.2: Return vs Print
- **Why this way:** `return` passes data back to the caller for further composition; `print` only displays text on stdout.

## Exercise B06.3: Default Arguments
- **Why this way:** Never use mutable default arguments (`def f(items=[]):`). Always use `None` as default and assign `items = []` inside the function.

## Exercise B06.4: Refactoring Long Code
- **Why this way:** Break large monolithic scripts into small, single-responsibility helper functions.

## Exercise B06.5: Variable Scope
- **Why this way:** Local variables defined inside a function are destroyed when the function returns, preventing accidental side-effects.

## Exercise B06.6: Input Validator
- **Why this way:** Return booleans or structured validation result tuples `(is_valid, error_msg)`.
