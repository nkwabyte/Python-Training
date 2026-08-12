# Exercise 06.1 — Five import failures

Each numbered case below fails. For each one, **before** looking at the files:

1. Run the given command.
2. Write down the exception type and your hypothesis.
3. Then diagnose properly, fix it, and answer the questions.

Do not fix any of them with `sys.path` manipulation. If your fix contains
`sys.path`, it is the wrong fix.

---

## Case 1 — run a package module directly

```bash
python mypkg/core.py
```

- Q1a. What error, and what does `__package__` equal at that moment?
- Q1b. Give the command that works, and explain what changes about `sys.path`
  and `__package__`.
- Q1c. `mypkg/util.py` uses an absolute import instead of a relative one. Does
  `python mypkg/util.py` work? Why is the answer different?

## Case 2 — the module that is not there

```bash
cd /tmp && python -c "import mypkg"
```

- Q2a. Why does this fail from `/tmp` but work from this directory?
- Q2b. Name two correct fixes. One of them is a single command.

## Case 3 — the import that runs code

```bash
python -c "import mypkg.slow_init"
```

- Q3a. What happened that should not have?
- Q3b. Why is this a problem for a test suite specifically?
- Q3c. Fix it, and state the general rule.

## Case 4 — the stale name

```bash
python -c "
import mypkg.settings as s
from mypkg.settings import DEBUG
s.DEBUG = True
print('module attribute:', s.DEBUG)
print('imported name:   ', DEBUG)
"
```

- Q4a. Why do the two lines disagree?
- Q4b. Which form should code use if the value can change, and why does this
  matter for `unittest.mock.patch` (Module 18)?

## Case 5 — the missing `__init__.py`

```bash
python -c "import broken1.thing"
```

- Q5a. This one actually *works*. Explain what kind of package `broken1` is.
- Q5b. Now run `python -m pytest broken1` and note what happens.
- Q5c. Why does this course recommend always adding `__init__.py` even though
  namespace packages are legal?
