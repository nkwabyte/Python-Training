# Module 18 — Testing, Debugging, and Quality

**Time budget:** 5 hours lesson, 8 hours exercises
**Prerequisite:** Modules 12 (DI), 16, 17

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

In a language with no compiler, tests are your only proof that the code does
what you think. But most test suites are slow, brittle, and test the wrong
things — they assert that methods were called rather than that outcomes
happened, they need a database to run, and they break whenever anything is
refactored.

This module is about writing tests that survive refactoring and catch real
bugs, which is a design problem more than a tooling one.

---

## 1. pytest, the parts you need

```python
def test_addition() -> None:
    assert add(2, 3) == 5          # plain assert; pytest rewrites it to show
                                    # both operands on failure
```

```bash
pytest                     # run everything
pytest -q                  # quiet
pytest -x                  # stop at the first failure
pytest -k "user and not slow"     # select by name
pytest -m integration      # select by marker
pytest --lf                # last failed
pytest --ff                # failed first, then the rest
pytest -vv                 # full diff on assertion failure
pytest --pdb               # drop into the debugger on failure
pytest -n auto             # parallel (pytest-xdist)
```

`--lf` and `--ff` are the two that change your day: after a broad failure, you
iterate on only the failing tests until they pass.

### Exceptions and approximations

```python
import pytest

def test_raises() -> None:
    with pytest.raises(ValueError, match="must be positive"):
        parse(-1)

def test_exception_attributes() -> None:
    with pytest.raises(ValidationError) as exc_info:
        validate({"age": -1})
    assert exc_info.value.field == "age"      # Module 16: carry data

def test_float() -> None:
    assert compute() == pytest.approx(0.3)    # Module 03
```

Always pass `match=`. `pytest.raises(ValueError)` alone passes when *any*
`ValueError` is raised, including one from a typo in your test setup.

---

## 2. Fixtures

```python
@pytest.fixture
def db() -> Iterator[Database]:
    conn = Database(":memory:")
    conn.migrate()
    yield conn              # the test runs here
    conn.close()            # teardown, even if the test fails

def test_insert(db: Database) -> None:
    db.insert({"id": 1})
    assert db.count() == 1
```

A fixture is dependency injection for tests (Module 12), and it composes:
fixtures can request other fixtures.

```python
@pytest.fixture(scope="session")     # once per test run
@pytest.fixture(scope="module")      # once per test file
@pytest.fixture(scope="function")    # the default: once per test
```

**Scope is a trade between speed and isolation, and getting it wrong is the
most common cause of "passes alone, fails in the suite".** A session-scoped
fixture holding mutable state is shared by every test; one test mutating it
changes what the others see, and the failure depends on *ordering*. Session
scope is for genuinely immutable or externally-managed things: a started
container, a compiled asset, a read-only fixture file.

### The built-in fixtures worth knowing

```python
def test_files(tmp_path: Path) -> None:          # a fresh temp dir per test
    (tmp_path / "f.txt").write_text("x", encoding="utf-8")

def test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("API_KEY", "test")        # undone automatically
    monkeypatch.setattr(module, "CONSTANT", 42)
    monkeypatch.chdir(tmp_path)

def test_output(capsys: pytest.CaptureFixture[str]) -> None:
    run()
    assert "done" in capsys.readouterr().out

def test_logs(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):
        risky()
    assert "retrying" in caplog.text
```

`monkeypatch` undoes everything at teardown, which `setattr` by hand does not.

### `conftest.py`

Fixtures defined there are available to every test in that directory and below,
with no import. Put shared fixtures there; put nothing else there, because code
in `conftest.py` is invisible to a reader of the test file.

---

## 3. `parametrize`

```python
@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("1.00", 100),
        ("0.01", 1),
        ("1000000.00", 100_000_000),
        pytest.param("abc", None, marks=pytest.mark.xfail(raises=ValueError)),
    ],
    ids=["one", "one-cent", "million", "invalid"],
)
def test_parse_money(raw: str, expected: int) -> None:
    assert Money.parse(raw).minor_units == expected
```

Each case is a **separate test** with its own name, so one failure does not hide
the rest and the report tells you exactly which input broke. A loop inside one
test does the opposite on both counts.

`ids=` is worth the extra line: `test_parse_money[one-cent]` in a CI log beats
`test_parse_money[1]`.

---

## 4. Test doubles, and why fakes beat mocks

| Kind | What it is | Use when |
|---|---|---|
| **Dummy** | A placeholder never used | Filling a required parameter |
| **Stub** | Returns canned answers | You need a specific return value |
| **Fake** | A working, simpler implementation | **The default choice** |
| **Spy** | Records how it was called | You must assert on an interaction |
| **Mock** | A spy with pre-set expectations | Rarely |

```python
# a FAKE: a real implementation, in memory
class InMemoryUserRepo:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
    def save(self, user: User) -> None:
        self._users[user.id] = user
    def get(self, uid: int) -> User | None:
        return self._users.get(uid)

def test_registration_stores_the_user() -> None:
    repo = InMemoryUserRepo()
    service = RegistrationService(repo)
    service.register("ada@example.com")
    assert repo.get(1).email == "ada@example.com"     # asserts an OUTCOME
```

versus

```python
def test_registration_calls_save() -> None:
    repo = Mock()
    RegistrationService(repo).register("ada@example.com")
    repo.save.assert_called_once()                     # asserts an INTERACTION
```

The mock version passes if `save` is called **with the wrong user**. It also
breaks the moment you rename `save` or call it twice for a good reason. A mock
test is coupled to the implementation; a fake test is coupled to the behaviour.

**Use a mock only when the interaction *is* the requirement** — "an email was
sent", "the audit log recorded it", "the payment gateway was called exactly
once".

### Patching: where, not what

```python
# app/service.py
from app.clients import fetch_user      # a COPY of the reference (Module 06)

# test
patch("app.clients.fetch_user")         # WRONG: service.py's copy is unaffected
patch("app.service.fetch_user")         # RIGHT: patches the name in use
```

**Patch where the name is used, not where it is defined.** This is Module 06's
`from x import y` binding rule, and it accounts for a large share of "the patch
did nothing" confusion.

Better still: do not patch. If the dependency is injected (Module 12), you pass
a fake and no patching is needed. **Heavy patching is a design smell** — it is
usually telling you the code constructs its own dependencies.

---

## 5. Coverage, and what it does not tell you

```bash
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-branch          # branch coverage: much more honest
```

Coverage tells you which lines *ran*. It does not tell you whether anything was
*asserted*:

```python
def test_nothing() -> None:
    process_everything()        # 100% coverage, zero assertions, always passes
```

Use coverage to **find untested code**, never as a quality target. A number
target produces tests written to raise the number, which are worse than no
tests because they take time to run and give false confidence.

Branch coverage is worth enabling: a line with `if x:` counts as covered when
only the true branch ever ran.

**Where to look in a coverage report:** error-handling paths (usually the least
covered and the most dangerous), boundary conditions, and any file with high
coverage and few assertions.

---

## 6. Property-based testing

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_is_idempotent(items: list[int]) -> None:
    assert sorted(sorted(items)) == sorted(items)

@given(st.text())
def test_encode_decode_round_trip(s: str) -> None:
    assert s.encode("utf-8").decode("utf-8") == s

@given(st.decimals(min_value=0, max_value=10**6, places=2), st.integers(1, 100))
def test_money_allocation_is_exact(amount: Decimal, n: int) -> None:
    parts = Money.parse(str(amount)).allocate(n)
    assert sum(parts[1:], parts[0]) == Money.parse(str(amount))
```

You state a **property** and Hypothesis searches for a counterexample, then
**shrinks** it to the smallest failing input. That shrinking is the feature: it
turns "fails on a 400-element list" into "fails on `[0, 0]`".

Properties worth reaching for: round trips (encode/decode, serialise/parse),
invariants (a sort's output is a permutation of its input; a total is
conserved), idempotence, commutativity, and comparison against a slow-but-obvious
implementation.

Property tests find the inputs you would never think to write: empty, one
element, duplicates, `NaN`, surrogate pairs, a 10,000-element list, `-0.0`.

---

## 7. Debugging

```python
breakpoint()                # 3.7+: drops into pdb right here
```

```
n(ext)  s(tep)  c(ontinue)  r(eturn)  u(p)  d(own)
l(ist)  ll      p expr      pp expr   w(here)  interact
b file:line     b file:line, condition
```

`u`/`d` to move up and down the stack, and `p`/`pp` to print, are 80 percent of
practical pdb use. `interact` gives you a full REPL in the current frame.

```bash
pytest --pdb                 # debugger on failure
pytest --trace               # debugger at the start of each test
python -m pdb -c continue app.py    # post-mortem on a crash
```

Two upgrades worth installing: `rich.traceback` (shows locals at every frame)
and `ipdb` (tab completion and syntax highlighting).

**Print debugging is legitimate** and often faster than a debugger. Use
`f"{value=}"` (Module 03) and delete them afterwards — or use `logger.debug`,
which you do not have to delete.

---

## 8. Linting and formatting

```bash
ruff format .            # format (replaces black)
ruff check . --fix       # lint and autofix (replaces flake8, isort, pylint)
mypy .                   # types
pytest -q                # tests
```

```yaml
# .pre-commit-config.yaml -- runs on every commit
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Automate all four in CI. **A style rule that is not enforced by a tool is a
style rule that will be argued about in code review forever**, and that time is
worth more than the rule.

---

## 9. Designing for testability

The strongest signal that code is well designed is that it is easy to test. The
five habits, each of which you have already met:

1. **Inject dependencies** (Module 12). Constructing your own database
   connection makes a test impossible without one.
2. **Separate computation from I/O** (Module 01). A pure function is testable
   with `assert f(x) == y` and nothing else.
3. **Take the clock, the random source and the id generator as parameters**
   (Module 08). This is what turns flaky tests into deterministic ones.
4. **Return data, render separately** (Module 07). Asserting on a data structure
   is stable; asserting on formatted text breaks whenever the format changes.
5. **Make invalid states unrepresentable** (Module 11). Every state you cannot
   construct is a test you do not have to write.

**If a test is hard to write, the difficulty is nearly always in the code, not
the test.** That feedback is the most useful thing testing gives you, and it
arrives before the bug does.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Mocks everywhere | Tests break on every refactor | Fakes; assert on outcomes |
| Patching the definition site | The patch does nothing | Patch where the name is used |
| Session-scoped mutable fixtures | Passes alone, fails in the suite | Function scope, or immutable state |
| Coverage as a target | Assertion-free tests | Use it to find gaps |
| `pytest.raises` without `match` | Passes on the wrong error | Always `match=` |
| Testing implementation details | Refactoring breaks tests | Test the public behaviour |
| Real clock / random / network | Flaky tests | Inject them |
| A loop inside one test | One failure hides the rest | `parametrize` |
| Interdependent tests | Order-dependent failures | Each test sets up its own state |
| Slow tests | Nobody runs them | Fakes, markers, `-n auto` |
| No test for the error path | The dangerous code is untested | Test failures explicitly |

---

## Self-check quiz

1. Why does pytest use a plain `assert`, and what does it do to it?
2. Why must `pytest.raises` be given `match=`?
3. When is `scope="session"` appropriate and when is it a trap?
4. Give the concrete difference between a fake and a mock, with a bug the mock
   test misses.
5. Why does `patch("app.clients.fetch_user")` fail when the module used
   `from app.clients import fetch_user`?
6. What does coverage measure, and name two things it cannot tell you.
7. What is shrinking, and why is it the point of property testing?
8. Name three properties worth testing, with an example of each.
9. Give five habits that make code testable.
10. Why is "hard to test" a statement about the code rather than the test?

---

## Exercises

1. **[`ex01_pytest.py`](exercises/ex01_pytest.py)** — Convert twelve
   `unittest`-style tests to idiomatic pytest with fixtures and parametrize.
2. **[`ex02_doubles.py`](exercises/ex02_doubles.py)** — One service, tested with
   mocks and with fakes. Refactor the implementation and see which suite breaks.
3. **[`ex03_hypothesis.py`](exercises/ex03_hypothesis.py)** — Find six real bugs
   in provided functions using property tests. All six are findable.
4. **[`ex04_testable.py`](exercises/ex04_testable.py)** — An untestable class.
   Make it testable without changing its behaviour, in seven refactoring steps.

---

## Going deeper

- [pytest documentation](https://docs.pytest.org/) — the fixtures and parametrize pages especially
- [Hypothesis](https://hypothesis.readthedocs.io/) — read "What you can generate and how"
- Martin Fowler, "Mocks Aren't Stubs" — the definitive article on test doubles
- Gary Bernhardt, "Boundaries" — functional core, imperative shell, in 30 minutes

---

**Next:** [Module 19 — The Standard Library, Files, and Serialization](../19-stdlib-files-serialization/README.md)
