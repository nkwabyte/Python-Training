# NotebookLM Visual Prompts — Module 20: Library and CLI Project

Generate the architecture video **before** Stage 1 and the API review **after**
Stage 8.

---

## Sources to add

| Source | Type |
|---|---|
| `20-project-library-and-cli/README.md` | Upload |
| The Part 3 module READMEs (14-19) | Upload |
| Your own `src/logmine/` files, once written | Upload |
| https://packaging.python.org/en/latest/tutorials/packaging-projects/ | Website |
| https://peps.python.org/pep-0561/ | Website |

---

## 1. Cinematic Video Overview — before you build

**Format:** Explanation
**Visual style:** Retro Print, or Custom:

```
Flat architectural schematic on a dark background. The library drawn as a box
with a PUBLIC SURFACE on its edge and internals behind it. Data flowing as a
single record travelling through pipeline stages. Memory shown as a meter that
stays flat. Monospace type for code. No characters, no mascots.
```

**Steering prompt:**

```
Audience: a developer who has written applications and is now writing a
LIBRARY -- code other people import, depend on, and cannot modify.

Thesis: a library is a promise. Everything you export you must support;
everything you print, exit, or log happens inside someone else's process; and
every dependency you take, you impose on all of them.

1. LIBRARY VERSUS APPLICATION. Draw an application as a box that owns the whole
   process, and a library as a box INSIDE someone else's. Then show three
   things going wrong: a library calling print() and corrupting a caller's
   stdout pipeline; a library calling sys.exit() and killing a web server
   handling other requests; and a library calling logging.basicConfig() and
   reconfiguring the host application's logging. State the rule: a library
   raises, returns, and stays silent.

2. THE PUBLIC SURFACE. Draw the package with a small set of exported names on
   its edge and a large set of internals behind it. Then show a consumer
   reaching PAST the surface into an internal module, a refactor moving that
   internal, and the consumer breaking. Show __all__ and __init__.py as the
   surface, and note that anything importable is de facto public whether you
   meant it or not.

3. THE LAZY PIPELINE OVER 100 GB. Reuse Module 14's picture, now with types.
   Show four chained stages, one record travelling the whole chain, and the
   memory meter flat. Then show the moment the design breaks: an EXACT
   percentile, which needs every value in memory. Animate the memory meter
   climbing as the exact version buffers, then the approximate version
   (reservoir or histogram) holding a fixed-size structure with the meter flat
   and an error bar drawn on the result. That trade -- exactness for bounded
   memory, honestly labelled -- is the intellectual centre of the project.

4. EVAL IS A VULNERABILITY. Show the filter expression 'status >= 500' going
   into eval() and working. Then show the input
   '__import__("os").system("rm -rf ~")' going into the same eval() and also
   working. Then show a real lexer/parser producing an AST, and the same
   malicious input failing at the LEXER with a column number and a caret,
   because those characters are not tokens in the language. Emphasise that the
   parser is not merely safer, it also gives better error messages -- security
   and usability pointing the same way.

5. PY.TYPED. Show a consumer running mypy against your library WITHOUT the
   py.typed marker: every symbol is Any, and their type checking silently
   degrades. Then with it: your annotations flow into their codebase. One empty
   file, and it is the difference between a typed library and a decorative one.

6. THE WHEEL TEST. Show the src layout again (Module 06), a wheel being built,
   and it being installed into a clean environment in a DIFFERENT directory.
   Show a module the author forgot to include: the local tests pass, and the
   installed import fails. Then show the same failure caught by the author's
   own test run under the src layout.

7. FOLLOW AND ROTATION. Show a tail following a file by descriptor, logrotate
   renaming it and creating a new one, and the tail happily following a file
   nobody writes to any more -- silently producing nothing. Then show inode
   detection noticing the swap and reopening. A small feature, a genuinely
   non-obvious bug.

Do not cover: asyncio, or CI. Modules 22 and 30.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map for designing a Python library.

Branch 1 "Library discipline": never print, never exit, never configure
logging, NullHandler, raise don't handle, and zero required dependencies as a
default.

Branch 2 "Public surface": __init__.py, __all__, what "public" means, semantic
versioning, and an API compatibility test.

Branch 3 "Laziness": generator stages, constant memory, and the aggregates that
break it (exact percentiles, exact cardinality) with their approximations and
error bounds.

Branch 4 "Typing for consumers": py.typed, PEP 561, no Any in public
signatures, generics that track through a fluent chain.

Branch 5 "Errors as an API": one base, data-carrying, documented per function,
and what a consumer's except clause should look like.

Branch 6 "Parsing without eval": lexer, AST, evaluator, error messages with
column and caret, and compile-once evaluate-many.

Branch 7 "Packaging": pyproject, entry points, wheels vs sdists, testing from
the built artifact, and the src layout's role.

Branch 8 "Docs that cannot rot": doctests run in CI, examples in every public
docstring, a README that is also a test.
```

---

## 3. Study Guide — the API review

Generate **after** Stage 8, with your source files added.

**Prompt:**

```
Act as a senior engineer reviewing a library before its 1.0 release. The source
is provided.

SECTION 1 -- THE PROMISE. List every name importable from the top-level
package. For each, decide whether it is intended to be public. Then find every
place a consumer would plausibly reach into an internal module because the
public surface does not offer what they need -- those are the gaps that produce
support tickets and accidental API commitments.

SECTION 2 -- LIBRARY DISCIPLINE. Find every print, sys.exit, logging
configuration, environment read, global mutation, and hardcoded file path
outside the CLI package. For each, say what it does to a host application.

SECTION 3 -- MEMORY. Trace every path from input to output and identify every
point where an unbounded amount of data could accumulate: a materialised list,
a growing dict, an aggregate holding all values, a cache with no maxsize, a
buffer with no limit. For each, state the input that would exhaust memory.

SECTION 4 -- ERRORS. For each public function, list every exception it can
raise, including ones from the standard library that it does not catch or
translate. Then say whether a consumer could write a sensible except clause
using only the documented hierarchy.

SECTION 5 -- TYPES. Find every Any, every untyped public function, and every
place a generic loses its parameter through a chain of calls.

SECTION 6 -- THE 1.0 QUESTION. What in this API would you regret in two years?
Name three things that will be hard to change once people depend on them.

Do not rewrite the code.
```

---

## The specific visuals to insist on

1. **A library inside someone else's process**, with `print`, `sys.exit` and
   `basicConfig` each causing a distinct visible failure.
2. **The public surface versus the internals**, and a consumer reaching past it.
3. **The memory meter flat for streaming aggregates and climbing for an exact
   percentile**, then flat again with an error bar on the result.
4. **`eval` accepting both a filter expression and an `__import__` payload**,
   then the lexer rejecting the second with a caret.
5. **mypy seeing `Any` without `py.typed` and real types with it.**
6. **A wheel installed in a clean directory failing on a forgotten module.**
7. **logrotate swapping the file** while a tail follows the old descriptor.

---

## Accuracy guardrails

```
Accuracy requirements:
- A library must not call print(), sys.exit(), or logging.basicConfig(). It
  should add a NullHandler to its logger and let the application configure
  output.
- py.typed (PEP 561) is required for a library's inline annotations to be
  visible to downstream type checkers, and it must be included in the built
  distribution -- not just present in the source tree.
- Exact percentiles and exact distinct counts require memory proportional to
  the data. Streaming versions are APPROXIMATE and must state an error bound.
- eval() on user input is arbitrary code execution. There is no safe subset
  achievable by blacklisting names.
- os.replace is atomic only within one filesystem (Module 07).
- Tailing a file by descriptor does not follow a rotation; detection requires
  comparing the inode (or device+inode) of the path.
- The src layout means the installed package, not the source tree, is what
  tests import. That is the mechanism that catches packaging mistakes.
- Zero dependencies is a design GOAL, not a moral rule. State the trade: fewer
  dependencies means less to break in consumers, and more code to maintain.
```

---

## After building, you should be able to

- [ ] Say three things a library must never do, and what each breaks.
- [ ] Explain why an exact percentile is incompatible with constant memory, and
      state your chosen approximation's error bound.
- [ ] Show that your filter language rejects a code-execution payload at the
      lexer.
- [ ] Explain what `py.typed` does and why it must be in the wheel.
- [ ] Describe the packaging bug the `src` layout catches.
- [ ] Name three API decisions you would regret in two years.
