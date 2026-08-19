# Solutions & Commentary — Module 15: Decorators, Closures, and functools

## Key Takeaways
- Always use `@functools.wraps(fn)` inside decorator wrappers to preserve docstrings, function names, and annotations.
- Parameterized decorators require three nested functions: `decorator_factory(*args) -> decorator(fn) -> wrapper(*args, **kwargs)`.
- Use `functools.lru_cache` for memoization of pure functions with hashable arguments.
