# Solutions — Module 18

## Exercise 18.2 — The experiment

| Change | Suite A (mocks) | Suite B (fakes) | A real bug? |
|---|---|---|---|
| 1. Rename `save` → `persist` | **RED** | GREEN | No |
| 2. Call `save` twice | **RED** | GREEN | No |
| 3. Save the wrong user (lowercased, id 0) | GREEN | **RED** | **Yes** |
| 4. Email a hardcoded address | GREEN | **RED** | **Yes** |

The mock suite is wrong in **both directions**, and that is the finding:

- **False positives** on changes 1 and 2. A harmless rename and a harmless
  restructure both turn it red. The team learns that red means "someone
  refactored", and stops reading failures carefully.
- **False negatives** on changes 3 and 4. `save` *was* called once, so
  `assert_called_once()` passes — while the wrong user is persisted and the
  welcome email goes to the wrong person. The suite is green and the feature is
  broken.

**Which failure mode costs more?** False negatives, by a wide margin. A false
positive costs ten minutes of annoyance. A false negative ships a bug and, worse,
consumes the trust that makes the suite worth running at all. A suite with
frequent false positives eventually produces false negatives too, because people
stop investigating red.

**When a mock IS the right tool.** When the *interaction itself* is the
requirement and there is no observable outcome to assert on:

```python
def test_payment_gateway_is_charged_exactly_once() -> None:
    gateway = Mock()
    service.checkout(cart, gateway=gateway)
    gateway.charge.assert_called_once_with(card, Money.parse("59.97"))
```

"The card was charged once, not twice" is not visible in any state you own — it
lives in someone else's system. That is a genuine interaction requirement, and a
fake cannot express it. Note that even here, `assert_called_once_with` (checking
the arguments) is far stronger than `assert_called_once`.

**The clock test** is the smallest lesson and one of the most useful. With `now`
injected, `test_created_timestamp_is_exact` asserts equality against a fixed
datetime. With `datetime.now()` called inside, the best you can assert is "some
time near now", which is weaker and can fail at midnight, across a DST
transition, or on a slow CI machine.

---

## Exercise 18.3 — Six bugs and their shrunk counterexamples

| # | Bug | Typical shrunk example |
|---|---|---|
| 1 | `split(" ")` only splits on spaces | `"\t"` or `"a\nb"` |
| 2 | `range(0, len, 0)` raises for `size=0` | `chunk([], 0)` or `chunk([0], 0)` |
| 3 | Division by zero; also lies for negatives | `percentage(0.0, 0.0)` |
| 4 | `b`'s tail is dropped | `merge_sorted([], [0])` |
| 5 | Negative slice for small limits | `truncate("ab", 1)` |
| 6 | Remainder all on the first part | `split_evenly(5, 2)` |

Two are worth dwelling on.

**Bug 1 is the one nobody finds by hand.** `text.split(" ")` looks correct and
passes every example anyone would write, because people test with spaces.
`str.split()` with *no argument* splits on any whitespace run and drops empties
(Module 03) — a one-character fix that no example-based test would have
motivated. Hypothesis finds it immediately because `st.text()` generates tabs
and newlines within a few dozen examples.

**Bug 5's counterexample is `truncate("ab", 1)`**, which returns `"..."` — three
characters, from a limit of one. `text[:limit - 3]` becomes `text[:-2]`, a
negative slice, which silently does something entirely different rather than
raising. This is Module 03's "slices never raise" property producing a wrong
answer instead of an error.

**Why bug 4 needs two properties.** "Output is sorted" is satisfied by an
implementation that returns `[]`, or `sorted(a)`, or drops half the elements.
Only "output is a permutation of the inputs combined" catches the dropped tail.
**A property that only constrains the shape of the output is usually not enough;
you also need one that constrains its content.** Construct
`return sorted(a)` and watch it pass the first property and fail the second —
that is the exercise's real point.

---

## Exercise 18.1 — unittest to pytest

The mechanical translation is easy: drop the class, drop `self`, replace
`assertEqual(a, b)` with `assert a == b`, replace `setUp` with a fixture.

The two things worth actually changing:

**`setUp` becomes a fixture, and that is an upgrade, not a rename.** `setUp` runs
for every test in the class whether it needs it or not, and there is one of them.
Fixtures are per-test-requested, composable, and can have different scopes — so
the expensive one runs once per session and the cheap one per test.

**Loops become `parametrize`.** A `for` loop inside a test stops at the first
failure and reports one test name for twenty cases. `parametrize` gives twenty
named tests, all of which run, and the report names the failing input.

---

## Exercise 18.4 — Making an untestable class testable

The seven steps, in an order where each one is independently safe:

1. **Inject the constructed dependencies.** Constructor parameters with
   production defaults, so no caller changes (Module 12).
2. **Inject the clock, the random source, and the id generator.** These three are
   what make tests flaky rather than merely slow.
3. **Take `argv` and `env` as parameters** rather than reading globals
   (Module 01).
4. **Separate computation from I/O.** Extract the pure logic into functions that
   take data and return data.
5. **Return data instead of printing.** The caller renders (Module 07).
6. **Replace `sys.exit` calls with raised exceptions or return codes**, so the
   function can be called from a test without killing the process.
7. **Narrow the exception handlers** so a test can assert that a specific
   failure propagates.

Notice that **none of these seven changes the behaviour**, and every one of them
also makes the code better independently of testing. That is the observation the
exercise exists to produce: *designing for testability and designing well are the
same activity*. The test suite is just the fastest way to find out whether you
have done it.
