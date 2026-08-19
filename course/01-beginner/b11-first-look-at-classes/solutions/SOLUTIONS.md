# Solutions & Commentary — Module B11: A First Look at Classes

## Exercise B11.1: Bank Account Class
- **Why this way:** Encapsulate account balance and transaction rules (`deposit`, `withdraw`) inside a class with `__init__`.

## Exercise B11.2: String Representations (`__repr__` and `__str__`)
- **Why this way:** `__repr__` should provide an unambiguous developer representation (e.g. `BankAccount(balance=100.0)`).

## Exercise B11.3: Class vs Function Worksheet
- **Why this way:** Use functions for stateless data transformations; use classes when state and behavior must be bound together.

## Exercise B11.4: Dataclasses
- **Why this way:** `@dataclass` generates `__init__`, `__repr__`, and `__eq__` methods automatically, reducing boilerplate.

## Exercise B11.5: Using Library Classes
- **Why this way:** Instantiate and interact with library classes like `datetime.datetime` and `pathlib.Path`.
