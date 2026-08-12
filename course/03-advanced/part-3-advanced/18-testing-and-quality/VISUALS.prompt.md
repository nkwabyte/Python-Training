# NotebookLM Visual Prompts — Module 18: Testing, Debugging, Quality

---

## Sources to add

| Source | Type |
|---|---|
| `18-testing-and-quality/README.md` | Upload |
| `12-design-principles-in-python/README.md` | Upload |
| https://docs.pytest.org/en/stable/how-to/fixtures.html | Website |
| https://hypothesis.readthedocs.io/en/latest/data.html | Website |
| https://martinfowler.com/articles/mocksArentStubs.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. A system under test drawn as a
box with its dependencies as adjacent boxes. Test doubles drawn as SWAPPED-IN
replacements with a visibly different fill. A refactoring shown as the inside
of the box changing while its outer edges stay identical. Monospace type for
all code and test output. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who writes some tests, mostly with unittest.mock, and
whose test suite breaks every time they refactor. They suspect this is normal.
It is not.

Thesis: a test suite that breaks when you refactor is testing the wrong thing.
Tests should be coupled to BEHAVIOUR, not to implementation -- and the main way
people couple them to implementation is by asserting on interactions instead of
outcomes.

1. THE REFACTORING TEST. Open with the demonstration that frames everything.
   Show one service, two test suites. Suite A uses a Mock and asserts
   repo.save.assert_called_once(). Suite B uses an in-memory fake and asserts
   that the user is actually in the repository afterwards.
   Now refactor the service -- rename save() to persist(), or batch two saves
   into one -- WITHOUT changing what the system does. Show suite A going red
   and suite B staying green. Then the reverse: introduce a real bug where the
   wrong user object is saved. Show suite A staying GREEN -- save was called
   once, after all -- and suite B going red.
   That double demonstration is the whole argument, and it should come first.

2. THE TEST DOUBLE SPECTRUM. Draw five boxes -- dummy, stub, fake, spy, mock --
   ordered by how much they know about the caller. Under each, one sentence on
   when it is right. Emphasise that a FAKE is a real implementation and
   therefore cannot drift from the interface it fakes, while a mock is a
   recording device that will happily record calls to a method that no longer
   exists.

3. WHERE TO PATCH. Reuse Module 06's from-x-import-y diagram exactly. Show a
   module importing a name, creating its OWN reference. Then show patching the
   ORIGINAL module and the copy remaining untouched, with the test passing for
   the wrong reason. Then patch the using module and show the copy replaced.
   Say the rule on screen: patch where the name is used, not where it is
   defined. Then say the better rule: if the dependency were injected, there
   would be nothing to patch.

4. FIXTURE SCOPE. Show four tests and a session-scoped fixture holding a mutable
   list. Test 1 appends to it. Tests 2, 3 and 4 now see the appended item.
   Show test 3 passing when run alone and failing when run after test 1 --
   then show it PASSING again when the suite runs in a different order.
   That is the "passes alone, fails in CI, passes on retry" pattern, and seeing
   its cause once is worth an hour of future confusion.

5. COVERAGE LIES. Show a function with four branches and a test that calls it
   with no assertions at all. Show the coverage report reading 100 percent.
   Then show the same function with a bug in one branch, still 100 percent
   covered, still passing. Then turn on BRANCH coverage and show the untaken
   else path appearing. State the rule: use coverage to find gaps, never as a
   target, because a target produces exactly the assertion-free test just
   shown.

6. SHRINKING. Property-based testing, and this is where the visual earns its
   keep. Show Hypothesis generating a 400-element list that fails, then
   iteratively halving and simplifying it -- 200, 50, 10, 3, 2 elements -- until
   it reports the minimal counterexample [0, 0]. Show the developer's experience
   of each: a 400-element failure is unreadable; [0, 0] is a bug you can fix in
   a minute. Shrinking is the feature, not the generation.

7. DESIGNING FOR TESTABILITY. Close with the same class twice. On the left it
   constructs a database connection, calls datetime.now(), and prints -- with
   the test blocked by all three. On the right the three are parameters, and the
   test is four lines. State that the difficulty was never in the test; it was
   in the code, and the test only revealed it.

Do not cover: CI pipelines, or async testing. Those are Modules 30 and 22.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Testing Python".

Branch 1 "pytest mechanics": plain assert and rewriting, raises with match,
approx, the flags worth knowing (-x, -k, --lf, --ff, -vv, --pdb, -n auto).

Branch 2 "Fixtures": yield-based setup and teardown, composition, the four
scopes with the trade each makes, the built-ins (tmp_path, monkeypatch, capsys,
caplog), and conftest.py.

Branch 3 "parametrize": one case per test, ids, xfail, and why a loop inside a
test is worse on two counts.

Branch 4 "Test doubles": the five kinds, fakes as the default, mocks only when
the interaction IS the requirement, and the two failure modes of mock-based
tests.

Branch 5 "Patching": where vs what, the from-import binding rule, and injection
as the alternative that removes the need.

Branch 6 "Coverage": what it measures, what it cannot, line vs branch, and why
a percentage target is harmful.

Branch 7 "Property testing": properties worth asserting (round trip, invariant,
idempotence, oracle), shrinking, and the inputs it finds that you would not.

Branch 8 "Debugging": breakpoint, the pdb commands that matter, --pdb, post
mortem, rich tracebacks, and print debugging done well.

Branch 9 "Designing for testability": the five habits, and the rule that a
hard-to-test function is a design signal.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone inheriting a slow, brittle test suite.

Include a diagnosis table: for each symptom (passes alone but fails in the
suite, fails only in CI, breaks on every refactor, takes 20 minutes, passes
while the feature is broken, flaky roughly one run in ten), the likely cause
and the fix.

Include a test-double decision table: given a dependency (a database, an email
sender, the clock, a random source, a payment gateway, a third-party HTTP API,
a file system), which double to use and why, and what the test should assert.

Include a fixture scope guide with a worked example of the bug each wrong scope
causes.

Include a property-testing starter kit: eight properties that apply to almost
any codebase, with the function shape each applies to.

End with five untestable functions, each with the refactoring that makes it
testable and the number of lines it took.
```

**Quiz prompt:**

```
Generate 16 questions.

At least four must present a test and a refactoring, and ask whether the test
should break -- distinguishing tests coupled to behaviour from tests coupled to
implementation.

At least three must be patching puzzles where the patch target is wrong and the
test passes for the wrong reason.

Include: a session-scoped mutable fixture causing order dependence, a
pytest.raises without match passing on an unintended error, a 100-percent-covered
function with a bug, a mock-based test that passes while the wrong object is
saved, and a test using the real clock that fails at midnight.

For each answer, say what the test was actually asserting, as opposed to what
its author believed it was asserting.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: meaning and the failure it
prevents or causes.

Include: assert rewriting, pytest.raises(match=), approx, fixture, yield
fixture, scope, conftest.py, tmp_path, monkeypatch, capsys, caplog,
parametrize, ids, xfail, dummy, stub, fake, spy, mock, patch target, line vs
branch coverage, shrinking, @given, breakpoint(), --lf.
```

---

## The specific visuals to insist on

1. **The double demonstration**: a harmless refactor breaking the mock suite,
   and a real bug passing it. Both, in that order, before anything else.
2. **The five doubles ordered by coupling**, with fakes highlighted as the
   default.
3. **The patched original and the untouched copy**, reusing Module 06's diagram.
4. **A session-scoped mutable fixture** and the same test passing, failing, then
   passing again under three orderings.
5. **A 100-percent coverage report on an assertion-free test**, then the same
   function with a bug still at 100 percent.
6. **Shrinking animated**: 400 elements down to `[0, 0]`.
7. **The same class with three hidden dependencies and with three parameters**,
   and the test beside each.

---

## Analogies that work

- **A smoke detector, not a fire inspector.** A test tells you something is
  wrong now; it does not prove the design is sound. Coverage is the number of
  rooms with a detector, which says nothing about whether the detectors have
  batteries.
- **A stunt double versus a cardboard cutout.** A fake can actually do the
  stunt; a mock is a cutout that records how many times someone pointed a
  camera at it.
- **Testing the exterior of a machine, not its gears.** You can replace every
  gear inside as long as the same input still produces the same output. Tests on
  the gears prevent you from ever changing them.

## Analogies to refuse

- **"Tests prove the code is correct."** They demonstrate that specific inputs
  produce specific outputs. Property tests widen the sample; nothing here is a
  proof.
- **"100 percent coverage means well tested."** The video should have already
  disproved this on screen; do not let the narration walk it back.
- **"Mocking is how you isolate a unit."** Isolation comes from the dependency
  being injectable. Mocking is one way to supply it, usually the worst one.

---

## Accuracy guardrails

```
Accuracy requirements:
- pytest REWRITES assert statements at import time to produce detailed failure
  output. It is not magic in the assert itself.
- pytest.raises without match= passes for any exception of that type, including
  one raised accidentally by the test's own setup.
- monkeypatch undoes its changes at teardown; a plain setattr does not.
- patch() must target the name in the module WHERE IT IS USED, because
  `from x import y` binds a separate reference (Module 06).
- Coverage measures executed lines (or branches). It cannot tell whether
  anything was asserted, whether the assertions are correct, or whether the
  right inputs were used.
- Hypothesis SHRINKS failing examples to a minimal counterexample. Say that
  shrinking, not generation, is the primary value.
- A session-scoped fixture is created once per test SESSION and shared. Mutable
  session-scoped state creates order-dependent tests.
- Fakes are real implementations and cannot drift from the interface. Mocks
  will happily record calls to methods that no longer exist -- state this,
  because it is the mechanism behind tests that pass while the code is broken.
- Do not claim tests must be fast at all costs. Slow integration tests have
  value; the point is that they must not be the only tests.
```

---

## After watching, you should be able to

- [ ] Explain, with an example, a refactor that should not break a good test.
- [ ] Give a bug a mock-based test misses and a fake-based test catches.
- [ ] Say where to patch, and why the other place fails silently.
- [ ] Name the fixture scope that causes order-dependent tests, and why.
- [ ] Say two things coverage cannot tell you.
- [ ] Explain shrinking and why it is the point of property testing.
- [ ] Name five habits that make code testable.
- [ ] Say what "this is hard to test" is telling you.
