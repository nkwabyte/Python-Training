# Exercise 06.2 — A real circular import

Three modules in `shop/`: `order.py`, `customer.py`, and `pricing.py`. They form
a cycle. Run it and watch it fail:

```bash
python -m shop.main
```

## Your tasks

**Task 1.** Draw the cycle. Which module imports which? Which specific line
fails, and what is in `sys.modules` at that moment?

**Task 2.** Fix it four different ways, each on its own git branch or in its own
copy of the directory:

- **A.** Extract the shared piece into a new module.
- **B.** Move an import inside a function.
- **C.** Import the module rather than the name.
- **D.** Use `if TYPE_CHECKING` (note: check whether the cycle here is purely a
  typing cycle, or a real runtime one. If it is real, D alone will not be
  enough — say so, and say what that tells you).

**Task 3.** Argue for one. Your answer should address:

- which fix a new reader would understand fastest
- which fix survives someone adding a new module to the package next month
- which fix hides a dependency from the top of the file
- what the cycle was telling you about the design

**Task 4.** After fixing, add a test that would fail if someone reintroduced
the cycle. (Hint: importing the modules in a fresh subprocess, in either order,
must work. `subprocess.run([sys.executable, "-c", "import shop.order"])`.)
