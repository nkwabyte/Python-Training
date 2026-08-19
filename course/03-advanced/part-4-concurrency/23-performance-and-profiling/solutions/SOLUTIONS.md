# Solutions & Commentary — Module 23: Performance and Profiling

## Key Takeaways
- Measure before optimizing: profile CPU with `cProfile` and memory with `tracemalloc`.
- Use `__slots__` on data-heavy classes to eliminate per-instance `__dict__` memory overhead.
- Choose appropriate data structures ($O(1)$ set/dict lookups vs $O(N)$ list scans).
