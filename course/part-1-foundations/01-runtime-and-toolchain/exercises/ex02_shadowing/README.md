# Exercise 01.2 — The shadowing bug

This little project is broken. Your job is to diagnose it **from the traceback
alone**, before reading any of the source files.

## Steps

1. Run it, without opening any files first:

   ```bash
   cd exercises/ex02_shadowing
   python app.py
   ```

2. Read the traceback. Write down, before looking at anything:
   - the exception type
   - which module it claims to be about
   - your hypothesis for the cause

3. Now diagnose it properly. In a REPL **in this directory**:

   ```python
   import random
   print(random.__file__)
   ```

   What does that tell you?

4. Fix it. There are three things to do, and missing the third one makes the
   bug appear to persist even after you fixed it.

5. Answer the questions below.

## Questions

**Q1.** Why did the interpreter find the wrong `random`? Name the specific
mechanism and the specific list involved.

**Q2.** `sampler.py` also fails, but with a *different* error than `app.py`.
Run it and explain why the two differ.

**Q3.** What was the third fix step, and why does skipping it make the bug
appear to survive the first two?

**Q4.** Name five other filenames that would cause this same class of bug, and
say what each one shadows.

**Q5.** Write a one-line shell command, or a three-line Python snippet, that
would have found this problem automatically. (You built this in Exercise 01.4 —
if you did that one first, run it here and see if it catches this.)

**Q6.** The project's own module is called `stats.py`. Is that also a shadowing
bug? Check `sys.stdlib_module_names`. What does your answer imply about how
careful you need to be when naming modules?
