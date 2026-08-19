# Solutions & Commentary — Module B05: Collections

## Exercise B05.1: Shopping List (Lists)
- **Why this way:** Lists provide ordered, mutable sequences with $O(1)$ append and indexed lookup.

## Exercise B05.2: Phonebook (Dictionaries)
- **Why this way:** Dictionaries map unique hashable keys to values with $O(1)$ average lookup and insertion time.

## Exercise B05.3: Deduplication (Sets)
- **Why this way:** `set(items)` removes duplicates with $O(N)$ time complexity compared to $O(N^2)$ manual list scanning.

## Exercise B05.4: Student Records (Nested Structures)
- **Why this way:** Combining lists of dictionaries represents structured relational datasets cleanly in pure Python.

## Exercise B05.5: Container Selection Worksheet
- **Why this way:** Choose `list` for ordered sequences, `set` for uniqueness/membership tests, `dict` for key-value lookups, and `tuple` for immutable records.

## Exercise B05.6: Object Aliasing
- **Why this way:** Using `.copy()` or `list(original)` creates a shallow copy, preventing unexpected mutations from shared references.
