# Module 29 — Data and Machine Learning Foundations

**Time budget:** 6 hours lesson, 10 hours exercises
**Prerequisite:** Modules 03 (Core Types), 05 (Collections), 18 (Testing), 23 (Performance)

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

Data processing and machine learning workflows demand thinking in terms of memory layouts, array strides, and vectorized transformations rather than scalar Python loops.

This module provides the computational bridge to data science and ML: NumPy's contiguous memory buffers and broadcasting rules, pandas indexing, groupby aggregation pipelines and memory reduction techniques, and scikit-learn's estimator API and leak-free `Pipeline` architecture.

---

## 1. NumPy: Memory, Strides, and Vectorization

Python lists store pointers to heap-allocated objects; NumPy `ndarray` stores homogeneous data in contiguous C or Fortran memory blocks.

```python
import numpy as np

# A 2D array is represented by data buffer, shape, and strides
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], dtype=np.float64)
# shape: (2, 3), strides: (24, 8) -> 24 bytes to next row, 8 bytes to next col

# Vectorized operation (executes in optimized C/SIMD instructions):
doubled = arr * 2.0  # No Python for-loop overhead
```

### Broadcasting Rules
Two dimensions are compatible when:
1. They are equal, OR
2. One of them is 1.

```python
# Shape (3, 4) + Shape (4,) -> Shape (3, 4) (broadcasts along rows)
# Shape (3, 1) + Shape (1, 4) -> Shape (3, 4) (outer operation)
```

---

## 2. pandas: Tabular Pipelines and Memory Efficiency

pandas adds labels, alignment, and relational operations to NumPy arrays.

### Method Chaining and Aggregation

```python
import pandas as pd

# Method chaining with query, assign, and groupby
summary = (
    df.query("status == 'completed'")
      .assign(net_revenue=lambda d: d["gross_revenue"] - d["discount"])
      .groupby(["region", "product_category"], as_index=False)
      .agg(
          total_revenue=("net_revenue", "sum"),
          order_count=("order_id", "count"),
          avg_order_value=("net_revenue", "mean")
      )
      .sort_values("total_revenue", ascending=False)
)
```

### Memory Reduction: Categoricals and Downcasting

```python
# Convert high-cardinality repetitive strings to category
df["status"] = df["status"].astype("category")
# Downcast 64-bit integers to int32 or int16
df["quantity"] = pd.to_numeric(df["quantity"], downcast="integer")
```

---

## 3. scikit-learn: Pipelines and Leak-Free ML

Data leakage occurs when information from test/validation sets is inadvertently used to train feature transformers (like scalers or encoders).

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Define ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), ["age", "income", "tenure"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["country", "device"])
    ]
)

# Pipeline bundles preprocessing and estimator into a single atomic model
model_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# Calling fit() fits transformers ONLY on training folds during cross-validation!
# model_pipeline.fit(X_train, y_train)
```

---

## Exercises

- `exercises/ex01_numpy_vectorization.ipynb`: Memory layouts, array slicing views vs copies, min-max scaling, and broadcasting distances.
- `exercises/ex02_pandas_pipeline.ipynb`: Data cleaning, method-chaining aggregations, and memory optimization.
- `exercises/ex03_sklearn_pipeline.ipynb`: Constructing leak-free preprocessing and classification pipelines.

---

## Solutions

See [`solutions/SOLUTIONS.md`](solutions/SOLUTIONS.md) for full solution commentary and data engineering analysis.
