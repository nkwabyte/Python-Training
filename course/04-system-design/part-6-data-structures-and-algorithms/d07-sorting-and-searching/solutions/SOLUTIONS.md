# Solutions & Commentary — Module D07: Sorting and Searching

## Key Takeaways
- Comparison-based sort lower bound is $\Omega(N \log N)$.
- Python's `list.sort()` uses Timsort: adaptive, stable, $O(N)$ on partially sorted data, $O(N \log N)$ worst-case.
- Binary search (`bisect`) achieves $O(\log N)$ lookup on sorted sequences.
