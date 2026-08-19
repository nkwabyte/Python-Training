# Solutions & Commentary — Module B09: Errors and Debugging

## Exercise B09.1: Exception Identification
- **Why this way:** Recognize the core standard exceptions: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, and `ZeroDivisionError`.

## Exercise B09.2: Fixing Tracebacks
- **Why this way:** Read tracebacks bottom-up: the last line identifies the exception type and reason; the line above gives the file and line number.

## Exercise B09.3: Narrow Exception Handling
- **Why this way:** Catch only specific expected exception types (`except ValueError:`) rather than bare `except:` or `except Exception:`.

## Exercise B09.4: Debugger Worksheet
- **Why this way:** Using `breakpoint()` opens an interactive PDB session to inspect local variables and step through execution.

## Exercise B09.5: Minimizing Bug Surface
- **Why this way:** Create small, isolated reproducing scripts to diagnose edge cases.
