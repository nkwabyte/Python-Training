# Solutions & Commentary — Module 29: Data and ML Foundations

## Overview of Exercises

This module drilled contiguous array operations in NumPy, vectorized scaling, pandas aggregations, and leak-free machine learning pipelines.

---

## Exercise 29.1: NumPy Vectorization & Broadcasting

### Key Takeaways
- Min-Max scaling is vectorized column-wise by computing `X.min(axis=0)` and `X.max(axis=0)` and applying subtraction and division across broadcasted shapes.
- Pairwise distance calculation uses `np.newaxis` to expand shapes `(N, 1, D)` and `(1, M, D)` so that differences `(N, M, D)` are computed concurrently across all pairs without a single Python loop.

---

## Exercise 29.2: pandas Aggregations

### Key Takeaways
- Using `as_index=False` in `groupby()` keeps grouping keys as standard DataFrame columns, making downstream transformations and joins cleaner.
- Named aggregation with `.agg(new_col=('source_col', 'func'))` produces explicit, readable schema outputs.

---

## Exercise 29.3: scikit-learn Pipelines

### Key Takeaways
- Never call `scaler.fit(X)` on the entire dataset prior to train/test splitting. Doing so leaks test set variance and mean into training features.
- Encapsulating preprocessing inside a `Pipeline` guarantees that each cross-validation fold transforms validation data strictly using statistics learned from the corresponding training fold.
