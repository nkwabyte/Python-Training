# Exercise 01.1 — Watch the pipeline

Not a coding exercise. An observation exercise. Answer in this file, below each
question. The point is to convert the README's diagram into something you have
personally seen happen.

Estimated time: 30 minutes.

---

## Part A — The compile/run split

Create `scratch/a.py`:

```python
print("line 1 ran")
x = 1 +
print("line 3 ran")
```

Run it.

**A1.** What was printed before the error?

> your answer:

**A2.** Which stage of the pipeline produced this error? How do you know?

> your answer:

Now create `scratch/b.py`:

```python
print("line 1 ran")
def f():
    return undefined_name
print("line 4 ran")
```

Run it.

**A3.** What was printed? Why is this different from `a.py`, given that both
files reference something that does not work?

> your answer:

**A4.** Now add `f()` as the last line and run again. What changed, and at which
stage did the error occur this time?

> your answer:

---

## Part B — Bytecode

In a REPL:

```python
import dis
dis.dis(compile("x = 1 + 2", "<s>", "exec"))
dis.dis(compile("x = a + b", "<s>", "exec"))
```

**B1.** The first one has no addition instruction. What happened to the `+`?

> your answer:

**B2.** Disassemble these three and note the differences:

```python
dis.dis(compile("s = 'a' + 'b'", "<s>", "exec"))
dis.dis(compile("nums = [i*2 for i in data]", "<s>", "exec"))
dis.dis(compile("nums = list(map(lambda i: i*2, data))", "<s>", "exec"))
```

Which of the last two does more work per element, and can you see why from the
bytecode?

> your answer:

**B3.** Disassemble a function that uses a local variable and one that uses a
global:

```python
g = 1
def uses_local():
    x = 1
    return x
def uses_global():
    return g

dis.dis(uses_local)
dis.dis(uses_global)
```

Two different instructions load the value. Name them, and predict which is
faster. (Module 24 explains why. Write your guess now and check it later.)

> your answer:

---

## Part C — The cache

**C1.** Create `scratch/mymod.py` with any content, and `scratch/main.py` that
imports it. Run `main.py`. Which file got a `__pycache__` entry, and which did
not?

> your answer:

**C2.** What is in the `.pyc` filename besides the module name, and why?

> your answer:

**C3.** Edit `mymod.py` and run `main.py` again. Did the cache update? What is
the invalidation key?

> your answer:

---

## Part D — Import cost

Run this on any script that imports something substantial:

```bash
python -X importtime -c "import json, csv, sqlite3"
```

**D1.** Which import was most expensive, and what does the tree structure of
the output tell you?

> your answer:

**D2.** Why might this matter for a CLI tool that users run hundreds of times a
day, but not for a web server?

> your answer:
