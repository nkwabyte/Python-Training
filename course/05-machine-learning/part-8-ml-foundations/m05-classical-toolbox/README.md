# Module M05 — The Classical Toolbox: Trees, Ensembles, and Unsupervised Methods

**Level:** 05 Machine Learning, Part 8 (Foundations of Learning)  |  **Time:** L5 E7  |  **Prerequisite:** Module M04

> **Status: curriculum outline.** The full lesson, notebooks, exercises, and
> solutions are written in a later build pass. This file specifies exactly what
> the module must contain, so the build can resume without re-deriving anything.

---

## Why this module

Deep learning is not the strongest method for most problems a working engineer
meets, and a course that goes straight from linear models to neural networks
quietly teaches otherwise. On tabular data, which is what most organisations
actually have, gradient boosted trees remain the method to beat, and they train
in seconds on a laptop. This module builds that toolbox properly, so that the
selection module at the end of the level can recommend it honestly, and so that
the deep learning you meet next has a real baseline standing in its way.

## What you will be able to do

- Explain how a decision tree splits, and why one tree alone overfits.
- Distinguish bagging from boosting by what each one reduces.
- Tune a gradient boosted model and know which four hyperparameters matter.
- Say why trees still beat neural networks on most tabular problems.
- Cluster and reduce dimensions, and state honestly what those results support.
- Interpret a model with permutation importance and partial dependence, and name the limits.

## Concept sections

1. **Decision trees** — Recursive splitting, impurity criteria, depth and leaf size, and the interpretability that makes a single tree worth drawing. Why an unpruned tree memorises.
2. **Bagging and random forests** — Bootstrap sampling and feature subsampling as variance reduction. Out-of-bag estimation as free validation. Feature importance and the bias that makes it misleading.
3. **Gradient boosting** — Additive stagewise fitting against the residual. XGBoost, LightGBM, and CatBoost, and the differences that matter in practice. Learning rate against number of trees, depth, and early stopping.
4. **Why trees still win on tabular data** — Heterogeneous feature types, no scaling required, robustness to irrelevant features, and monotone-transform invariance. The evidence, cited, not asserted.
5. **Feature engineering for tabular problems** — Categorical encoding, ordinal versus one-hot versus target encoding, missing values as signal, dates and cyclical features, and interactions trees find for free.
6. **Clustering** — k-means and its assumptions, hierarchical clustering, DBSCAN for shapes and noise. Choosing k, evaluating without labels, and the honest statement that a clustering is a hypothesis.
7. **Dimensionality reduction** — PCA and what explained variance means. t-SNE and UMAP as visualisation tools only, with the warning about reading distances, cluster sizes, and gaps in their output.
8. **Interpretability** — Permutation importance, partial dependence, and SHAP. What each answers, what none of them establishes, and why correlation between features breaks all three.

## What you build

A gradient boosted baseline on a tabular dataset of your choosing, tuned with
early stopping and recorded formally, because Part 9 asks you to beat it with a
neural network and Module M20 asks you what the attempt proved.

## Exercises to build

| File | What it drills |
|---|---|
| `ex01_tree.py` | Implement a decision tree splitter and compare against scikit-learn. |
| `ex02_forest.py` | Show bagging reducing variance, using out-of-bag error. |
| `ex03_boosting.py` | Tune a gradient boosted model with early stopping and record the baseline. |
| `ex04_importance.py` | Show impurity importance misleading where permutation importance does not. |
| `ex05_encoding.py` | Apply target encoding correctly, then leak it deliberately and measure the damage. |
| `ex06_cluster.py` | Cluster with three algorithms and defend the number of clusters. |
| `ex07_pca.py` | Reduce dimensions, then misread a t-SNE plot on purpose and explain the error. |
| `ex08_baseline.md` | Write the baseline record that Part 9 and Module M20 will refer back to. |

## Compute budget

CPU only. Every exercise finishes in under a minute on a laptop, which is itself one of the arguments the module is making.

## Common mistakes this module must address

- **Fitting the target encoder before splitting** — Leakage, and it looks like the best model you have ever built.
- **Reading impurity-based feature importance as causal** — It is biased toward high-cardinality features and says nothing about causation.
- **Reading distances and cluster sizes in a t-SNE plot** — They are not preserved. The plot is for looking, not for measuring.
- **Choosing k from the elbow alone** — Combine it with silhouette, stability across seeds, and whether the clusters mean anything to a domain expert.
- **Reaching for a neural network on five thousand rows of tabular data** — Boost it first. The baseline usually wins and it took a minute.

## Self check questions

1. What does bagging reduce, and what does boosting reduce?
2. Which four gradient boosting hyperparameters matter most, and what does each control?
3. Why do trees not need feature scaling?
4. What can you conclude from a t-SNE plot, and what can you not?
5. Why is permutation importance preferred to impurity importance?
6. When would you choose a single shallow tree over a boosted ensemble?

## Going deeper

- Hastie, Tibshirani, Friedman, The Elements of Statistical Learning, chapters 9, 10, and 15
- Grinsztajn, Oyallon, Varoquaux, Why do tree-based models still outperform deep learning on typical tabular data?
- The scikit-learn user guide, ensemble and clustering sections
- Wattenberg, Viegas, Johnson, How to Use t-SNE Effectively
