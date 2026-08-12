# NotebookLM Visual Prompts — Module 14: Iterators and Generators

**One of the three highest-value visual sets in the course.** A suspended
function frame is impossible to see in source code and obvious in a picture.

---

## Sources to add

| Source | Type |
|---|---|
| `14-iterators-and-generators/README.md` | Upload |
| `09-dunder-and-data-model/README.md` | Upload |
| https://docs.python.org/3/library/itertools.html | Website |
| https://peps.python.org/pep-0380/ | Website |
| https://docs.python.org/3/reference/expressions.html#yield-expressions | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. A function is drawn as a FRAME
-- a box containing its local variables and a marker showing which line is
executing. A suspended frame is drawn greyed but INTACT, with the marker
resting on the yield line, so that "paused, not finished" is unmistakable.
Pipelines drawn as connected pipes with a single item visible travelling
through them. Monospace type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has used generators without understanding them, and
who writes list comprehensions where a generator expression belongs. They can
read `yield` but could not say what it does to the function's frame.

Thesis: `yield` SUSPENDS a function -- freezing its locals and its position --
rather than returning from it. Everything about generators, itertools, and
eventually async follows from that one fact.

1. THE FOR LOOP DESUGARED. Open by showing `for x in things:` transforming into
   the explicit iter()/next()/try-StopIteration loop. Two protocol methods, and
   the rest of the video is built on them. Show StopIteration being raised and
   CAUGHT by the loop -- it is a signal, not an error, and viewers who have seen
   it in a traceback need that said.

2. THE SUSPENDED FRAME. This is the central image; give it the most time.
   Call a generator function and show that NOTHING RUNS -- a frame is created
   and immediately paused before its first line, with a print statement in the
   body visibly not printing. Then call next() and animate the frame waking,
   executing to the first yield, handing out a value, and FREEZING with its
   locals intact and the marker resting on the yield line. Call next() again and
   show it resuming from exactly that marker with the same locals.
   Contrast with an ordinary function's frame being DESTROYED on return. Paused
   versus finished is the distinction the whole module depends on.

3. ITERABLE VERSUS ITERATOR, AND THE SILENT EMPTY LOOP. Draw an iterable as a
   FACTORY that produces a fresh cursor on request, and an iterator as a single
   cursor with a position. Then run two consecutive list() calls over a
   generator and show the second returning empty -- with no error, no warning,
   nothing. Hold on that silence. Then show __iter__ written as a generator
   function, with LOCAL state, producing a fresh cursor per call and both loops
   working.

4. THE PIPELINE. The payoff. Set up four chained generator stages over a 50 GB
   file. First show that constructing the pipeline runs NOTHING -- all four
   frames created and paused. Then show the consumer asking for one item, and
   animate the PULL travelling backwards up the chain to the file, and one line
   travelling forward through all four stages. Then show the memory meter: one
   line resident, regardless of file size.
   Now the eager version beside it: each stage materialising a full list, the
   memory meter climbing, the process dying before stage two completes.
   Finally, show a `break` after ten results, and everything upstream stopping
   immediately -- the file read stops at line 900 of a 50 GB file.

5. GROUPBY. Show groupby walking a sequence and cutting a new group every time
   the key CHANGES. Then run it on unsorted input and show the same key
   producing five separate groups. Emphasise that this is not an error -- it is
   a wrong answer that looks like a right one, which is worse.

6. TEE. Show tee(it, 2) with one branch racing ahead and the internal buffer
   growing to hold the gap. Then show both branches advancing together and the
   buffer staying small. The lesson is that tee's cost depends on consumer
   behaviour, not on the data.

7. SEND, AND THE BRIDGE TO ASYNC. Show yield as a TWO-WAY door: a value going
   out, and send() pushing a value back in to become the result of the yield
   expression. Then show @contextmanager as the everyday application -- the
   generator suspends at yield, the with-block runs in the caller, and the
   generator is resumed to run its finally.
   Close by noting that this is where async/await came from: an awaiting
   coroutine is a suspended frame, exactly like the one from section 2, and
   Module 22 is this picture with a scheduler attached.

Do not cover: asyncio itself, or decorators. Those are Modules 22 and 15.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Lazy Evaluation in Python".

Branch 1 "The protocol": __iter__, __next__, StopIteration as a signal, the
desugared for loop, iterable vs iterator, and the one-shot consequence.

Branch 2 "Generator functions": yield suspends, calling one runs nothing,
frames preserved across suspensions, __iter__ written as a generator, yield
from and what it forwards beyond iteration.

Branch 3 "Generator expressions": syntax, when parentheses can be omitted, and
the list-vs-generator decision.

Branch 4 "Pipelines": stages, laziness, constant memory, early termination,
composability, and the `with`-inside-a-generator resource trap.

Branch 5 "itertools": grouped by purpose -- combining (chain, zip_longest),
slicing (islice, takewhile, dropwhile), grouping (groupby and its sorted
requirement), combinatorics (product, permutations, combinations),
accumulating (accumulate, pairwise), and duplicating (tee and its buffering
cost).

Branch 6 "Coroutines": yield as an expression, send/throw/close, priming, and
@contextmanager as the everyday use.

Branch 7 "When NOT to be lazy": needing len, two passes, indexing, small data,
feeding a C library, and the debugging cost.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to process a file larger than their
machine's memory.

Include a decision table: given a requirement (need the length, need to iterate
twice, need item 500, data is 50 GB, stream is infinite, will stop after the
first match, feeding NumPy, fewer than 100 items), choose list or generator and
give the reason.

Include an itertools reference organised by the QUESTION being asked ("how do I
join two sequences", "how do I take the first N", "how do I stop at the first
failure", "how do I group by a key", "how do I get a running total", "how do I
look at consecutive pairs"), each with the function and a worked example.

Include a laziness debugging section: why a traceback points at the consumption
site, why a generator shows nothing in a debugger, how to temporarily
materialise a stage, and how to detect an accidentally exhausted iterator.

End with five pipelines described in prose, each with the generator chain that
implements it and its memory profile.
```

**Quiz prompt:**

```
Generate 16 questions on iterators and generators.

Required predict-the-output cases: calling a generator function with a print on
the first line, iterating a generator twice, len() on a generator, groupby on
unsorted input, sum(lists, []) versus chain.from_iterable, a generator with a
return statement, send() without priming, zip on unequal lengths, islice over
an infinite count(), and a for-else over a generator.

Include two questions that give a memory constraint and a data size and ask
whether a given implementation will survive.

For each answer, describe what happened to the FRAME -- created, suspended,
resumed, exhausted -- not merely what was printed.
```

**Flashcards prompt:**

```
22 flashcards. Front: a term, function, or fragment. Back: what it does and its
one gotcha.

Include: __iter__, __next__, StopIteration, generator function, generator
expression, yield, yield from, send, throw, close, priming, iterable vs
iterator, exhaustion, islice, chain.from_iterable, groupby (sorted!), tee
(buffering!), takewhile, dropwhile, accumulate, pairwise, @contextmanager.
```

---

## The specific visuals to insist on

1. **The generator call that runs nothing** — a `print` on line one visibly not
   printing.
2. **The suspended frame with locals intact and the marker on the `yield`
   line**, next to an ordinary function's frame being destroyed on return.
3. **The silent second `list()` returning empty.** Hold on the silence; no
   error appears.
4. **The pull travelling backwards up a four-stage pipeline**, and one item
   travelling forward.
5. **Two memory meters side by side** over a 50 GB file: flat versus climbing
   until the process dies.
6. **A `break` after ten results stopping the file read at line 900.**
7. **`groupby` on unsorted input producing five groups for one key** — a wrong
   answer that looks right.
8. **`tee`'s buffer growing to the gap between two consumers.**
9. **`yield` as a two-way door**, with `send()` pushing a value back in.

---

## Analogies that work

- **A conveyor belt versus a warehouse.** The eager version unloads the entire
  truck into a warehouse before anyone looks at the first box. The lazy version
  puts one box on a belt when someone asks for it. The warehouse needs to be as
  big as the truck; the belt does not.
- **A bookmark, not a photocopy.** A suspended generator is a book with a
  bookmark in it — the book is intact, the position is remembered, and reading
  resumes exactly there. It is not a copy of the pages read so far.
- **Pulling, not pushing.** The consumer pulls; nothing upstream runs until
  something downstream asks. This immediately explains why `break` stops the
  file read.

## Analogies to refuse

- **"A generator is a list that computes items as you go."** It is not a list at
  all — it has no length, no indexing, and no second pass. The list framing is
  exactly what produces the exhaustion bug.
- **"`yield` is like `return`."** `return` destroys the frame; `yield` freezes
  it. That is the entire difference and the analogy erases it.
- **"Generators are faster."** They use less memory. For small data they are
  often *slower* than a list, and saying otherwise sends people optimising in
  the wrong direction.

---

## Accuracy guardrails

```
Accuracy requirements:
- Calling a generator function executes NONE of its body. It creates a
  generator object. Demonstrate with a print on the first line.
- yield SUSPENDS the frame, preserving locals and position. It does not return
  and discard the frame. Say this in those terms.
- StopIteration is a signal that the for loop catches, not an error condition.
  Since PEP 479, a StopIteration raised inside a generator body becomes a
  RuntimeError rather than silently ending iteration -- mention this if raising
  it manually comes up.
- A generator can be iterated ONCE. A second pass yields nothing and raises
  NOTHING. The silence is the hazard.
- itertools.groupby groups CONSECUTIVE equal keys and requires sorted input for
  the usual meaning. Unsorted input produces a wrong answer, not an error.
- itertools.tee buffers. Its memory cost equals the gap between the fastest and
  slowest consumer, and is unbounded if one branch is not consumed.
- A generator is not faster than a list in general. Its advantage is memory and
  early termination. For small collections a list is usually faster.
- A `with` block inside a generator holds its resource for as long as the
  generator is alive and unclosed. Under CPython refcounting this is usually
  immediate at abandonment, but it is not guaranteed and is not true on PyPy.
- A generator's `return value` is not yielded; it is attached to
  StopIteration.value and is retrievable via yield from.
```

---

## After watching, you should be able to

- [ ] Describe what happens to the frame at `yield`, in one sentence.
- [ ] Explain why calling a generator function prints nothing.
- [ ] Say why the second `list()` over a generator is empty and silent.
- [ ] Draw a four-stage pipeline and describe the pull direction.
- [ ] Explain why `break` after ten results stops the file read early.
- [ ] Say what `groupby` requires and what happens when it does not get it.
- [ ] Say when `tee` is a bad idea, in terms of consumer behaviour.
- [ ] Name four situations where a list is the correct answer.
