# Solutions & Commentary — Module B10: Organising Code

## Exercise B10.1: Splitting Code into Modules
- **Why this way:** Group related functions into separate `.py` files and import them with `from module import function`.

## Exercise B10.2: The Main Guard
- **Why this way:** `if __name__ == "__main__":` allows a file to be both imported as a library and executed directly as a script.

## Exercise B10.3: Standard Library Tour
- **Why this way:** Leverage built-in modules (`math`, `random`, `datetime`, `collections`) before adding third-party dependencies.

## Exercise B10.4: Virtual Environments Worksheet
- **Why this way:** Virtual environments isolate project dependencies from global system Python packages.

## Exercise B10.5: Resolving Import Errors
- **Why this way:** Understand `sys.path` resolution and avoid circular imports by restructuring dependency hierarchy.
