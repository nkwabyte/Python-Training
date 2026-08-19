# Solutions & Commentary — Module 16: Error Handling and Robustness

## Key Takeaways
- Custom exception hierarchies: inherit from a domain base exception (`AppError(Exception)`).
- Exception chaining: use `raise NewException(...) from original_exc` to preserve root-cause tracebacks.
- In Python 3.11+, use `ExceptionGroup` and `except*` for handling concurrent async exceptions.
