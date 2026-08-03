# NotebookLM Visual Prompts — Module 07: Inventory CLI Project

This module is a build, not a lesson, so the visuals serve a different purpose:
they are for **planning before you code** and **reviewing after**. Generate the
architecture video before Stage 1, and the review guide after Stage 8.

---

## Sources to add

| Source | Type |
|---|---|
| `07-project-inventory-cli/README.md` | Upload |
| The Part 1 module READMEs (01-06) | Upload |
| Your own `src/inventory/` files, once written | Upload |
| https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ | Website |
| https://clig.dev/ | Website |

---

## 1. Cinematic Video Overview — architecture, before you build

**Format:** Explanation
**Visual style:** Retro Print, or Custom:

```
Flat architectural diagram on a dark background. Modules as labelled boxes,
dependencies as one-way arrows. Data flow as a distinct line style from control
flow. Terminal output shown in monospace. No characters, no mascots.
```

**Steering prompt:**

```
Audience: a developer about to build a command-line application, who has
written scripts but never structured one.

Thesis: a CLI is three layers -- an interface layer that knows about argv and
exit codes, a logic layer that knows nothing about either, and a storage layer
that knows nothing about the logic. Every quality attribute in the brief falls
out of keeping those layers apart.

1. THE THREE LAYERS. Draw them stacked, with arrows going ONE WAY only:
   cli -> operations -> store. Show that `print` and `sys.exit` live ONLY in the
   top box, and that the middle box can therefore be tested by calling a
   function and looking at what it returns. Show the same operation being driven
   by a test, by the CLI, and by a hypothetical HTTP handler, to make the point
   that the logic does not know or care who called it.

2. WHY IMMUTABLE ITEMS. Show an operation taking an Item and returning a NEW
   Item plus a Change record, next to the mutating version. Show that the
   history log falls out for free in the first design and has to be maintained
   by hand in the second, and that the first can be tested with a single
   equality assertion.

3. THE ATOMIC WRITE. This deserves its own 45 seconds and should be dramatised.
   Show a direct overwrite: the file is truncated to zero, the process is
   killed, and the user's data is GONE. Then show write-to-temp-then-rename:
   the original is untouched until a single atomic rename swaps it. Show the
   kill happening at three different moments in each version, and which of
   those six moments loses data.

4. EXIT CODES AND STREAMS. Show a shell pipeline consuming the tool's stdout
   while error text goes to stderr and appears on the terminal. Then show the
   same pipeline when errors were printed to stdout: the garbage flows into the
   next command. Then show a CI script branching on the exit code, and what
   happens when a failing command returns 0.

5. THE DATA MODEL. Show Item, Location, Money and Change as boxes with their
   fields, and the operations as arrows that transform them. Highlight the
   partial-move case: 10 of 40 units leaving A1 for B3, and the question of what
   happens if B3 already holds that SKU at a different unit price. Present it as
   an OPEN DECISION the builder must make, not as a solved problem.

6. THE FILE FORMAT WITH A VERSION FIELD. Show a v1 file being read by v2 code,
   and what the version field lets that code do that a version-less file does
   not.

Do not cover: specific argparse syntax, or how to write tests. Cover the
SHAPE of the program.
```

---

## 2. Mind Map — the plan

**Prompt:**

```
Build a mind map for planning a command-line application.

Branch 1 "Layers": interface, logic, storage -- with the rule about which one
may import which, and where print/sys.exit/argv are allowed.

Branch 2 "Data model": the entities, which are immutable and why, where
validation happens, and how change history is captured.

Branch 3 "Storage": atomic writes, schema versioning, encoding, indexes held in
memory, and what happens on a corrupt file.

Branch 4 "CLI contract": subcommands, flags, exit codes, stdout vs stderr,
--json for machine consumption, and what makes output composable in a pipeline.

Branch 5 "Failure modes": a checklist of at least twelve things to deliberately
break, from an empty file to two concurrent writers.

Branch 6 "Definition of done": the checklist from the brief, as leaves that can
be ticked.
```

---

## 3. Study Guide — the design review

Generate this **after** Stage 8, with your own source files added as sources.

**Prompt:**

```
Act as a senior engineer reviewing this command-line application. The source
files are provided as sources.

Produce a review with three sections.

SECTION 1 -- LAYER VIOLATIONS. Find every place where the interface layer's
concerns leaked into the logic layer or vice versa: a print or sys.exit outside
the CLI module, a logic function that reads argv or the environment, a storage
function that formats output for a human, a CLI function containing a business
rule. Quote the line and say which layer it belongs in.

SECTION 2 -- FAILURE MODES NOT HANDLED. Work through this list against the
code and state what actually happens for each: empty data file, malformed JSON,
data file is a directory, data file unreadable, disk full during save, process
killed mid-save, a SKU containing a comma exported to CSV, a name containing a
newline, a name containing an emoji, quantity present as a string in the JSON,
a negative quantity, two processes writing simultaneously, a data file from a
future schema version. For each, say whether the result is a clear message or a
traceback.

SECTION 3 -- TESTABILITY. Identify every function that cannot be tested without
touching the filesystem, the clock, the environment, or stdout, and say what
minimal change would fix it. For each, name the technique: parameter injection,
a Protocol, a fake, or a fixture.

Do not rewrite the code. Ask the questions a reviewer would ask.
```

---

## The specific visuals to insist on

1. **Three layers with one-way arrows**, and `print`/`sys.exit` confined to the
   top box.
2. **The same operation called by a test, the CLI, and an HTTP handler** —
   proving the logic layer is independent.
3. **The atomic write, dramatised**: six kill moments across two
   implementations, and which lose data.
4. **A shell pipeline** with errors correctly on stderr, and the same pipeline
   corrupted when they go to stdout.
5. **The partial move**, drawn as stock physically splitting between two
   locations, with the merge question left visibly open.
6. **A v1 file being read by v2 code**, with the version field as the hinge.

---

## Accuracy guardrails

```
Accuracy requirements:
- os.replace (and Path.replace) is atomic only WITHIN THE SAME FILESYSTEM.
  Writing the temp file to /tmp and renaming onto a different mount is a copy,
  not a rename, and is not atomic. Say this.
- An atomic rename protects against a crash. It does NOT protect against two
  concurrent writers -- the second write still wins entirely and the first is
  lost. Concurrency needs locking, and that is a separate problem.
- Exit code conventions: 0 success, 1 general failure, 2 usage error (argparse
  already uses 2). Codes above 128 are reserved for signals.
- Money must not be represented as float. Decimal or integer minor units.
- Do not present `if __name__ == "__main__"` as the way to make a package
  runnable; that is what __main__.py and console_scripts entry points are for.
- CSV requires the csv module, not str.split. Fields legitimately contain
  commas, quotes and newlines.
- Do not claim type hints are enforced at runtime.
```

---

## After building, you should be able to

- [ ] Explain why the logic layer must not import `sys`.
- [ ] Draw the atomic write and say exactly which failure it prevents and which
      it does not.
- [ ] Justify your choice about mutable versus immutable items.
- [ ] Say what each of your exit codes means and who consumes them.
- [ ] Name three failure modes you found by trying to break your own program.
- [ ] Explain why tests import the installed package rather than a path.
