# NotebookLM Visual Prompts — Module 15: Decorators and functools

---

## Sources to add

| Source | Type |
|---|---|
| `15-decorators-closures-functools/README.md` | Upload |
| `04-control-flow-and-functions/README.md` | Upload |
| https://docs.python.org/3/library/functools.html | Website |
| https://docs.python.org/3/library/contextlib.html | Website |
| https://peps.python.org/pep-0318/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Functions drawn as labelled
boxes. A decorated function drawn as NESTED SHELLS -- the original function
visible at the centre, each decorator a concentric ring around it. A call
animated as a token travelling inward through every ring and back out.
Monospace type for all code. No characters, no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who uses @decorators from frameworks daily and treats
the @ symbol as magic. They may have written one decorator and got the
argument form wrong.

Thesis: a decorator is a function that takes a function and returns a function.
The @ is sugar for one line of assignment, it runs ONCE at definition time, and
every framework decorator they have ever used is this one mechanism.

1. THE DESUGARING. Open with @decorator above def f transforming into
   f = decorator(f), letter by letter. Then emphasise WHEN: show the module
   being imported and the decorator running at that instant, once, before any
   call happens. Show three calls to f afterwards and the decorator NOT running
   again -- only the wrapper does. Definition-time versus call-time is the
   distinction people get wrong.

2. THE NESTED SHELLS. Draw a decorated function as concentric rings with the
   original at the centre. Animate a call: the token enters the outermost ring,
   passes through each wrapper's "before" code, reaches the centre, and returns
   back out through each "after" code in reverse. This picture makes stacking
   order obvious and should be established before stacking is discussed.

3. WRAPS. Show the wrapper REPLACING the original, and the metadata going with
   it: __name__ becomes 'wrapper', __doc__ becomes None, the signature becomes
   (*args, **kwargs). Then show four concrete downstream failures, on screen:
   help() printing nothing useful, a profiler reporting 'wrapper' for twelve
   different functions, pytest failing to resolve a fixture because it reads
   parameter names, and FastAPI generating an empty request schema because it
   reads the signature. Then apply functools.wraps and show the metadata being
   copied across, including __wrapped__ as the pointer that lets
   inspect.signature see through.

4. THE THREE LEVELS. Draw the factory-decorator-wrapper structure as three
   nested boxes, and label what each RECEIVES: the factory receives the
   decorator's arguments, the decorator receives the function, the wrapper
   receives the call's arguments. Then show the classic mistake: @retry without
   parentheses, with the FUNCTION arriving where `attempts` was expected, and
   the confusing error that produces several frames away.

5. STACKING ORDER. Using the shells picture: with @a @b @c, animate the wrapping
   happening BOTTOM-UP at definition (c wraps first, so it is innermost) and the
   call travelling TOP-DOWN (a's code runs first). Then the money shot: the
   @app.route / @require_auth pair in both orders. In the correct order, show
   the framework's registry holding the authenticated wrapper. In the wrong
   order, show it holding the RAW function, and a request arriving and reaching
   the handler with no authentication -- while the wrapped version sits in a
   variable nobody calls. Emphasise that this version runs fine and passes a
   smoke test.

6. LRU_CACHE, AND ITS TRAPS. Show the cache as a dict from arguments to
   results, with hits short-circuiting the call. Then three traps, each as a
   picture:
     - f(1), f(1.0) and f(True) all landing in ONE slot, because they are equal
       and hash equally.
     - f(1) and f(x=1) landing in TWO slots for the same logical call.
     - @cache on a METHOD: show `self` becoming part of the key, and every
       instance ever passed being held alive by the cache forever, with the
       memory meter climbing and never falling. That is the leak.

7. SINGLEDISPATCH AND THE CLOSING POINT. Show an isinstance chain that a third
   party cannot extend without editing it, next to singledispatch where a
   third-party module registers a handler for its own type from outside. Close
   on the observation that decorators are how Python does aspect-oriented
   programming, and that every framework the viewer uses -- Flask, FastAPI,
   pytest, Celery, Click -- is this single mechanism.

Do not cover: async decorators or typing of decorators. Those are Modules 22
and 17.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Decorators and functools".

Branch 1 "The mechanism": @ as sugar, definition-time execution, the wrapper,
*args/**kwargs, and rebinding the name.

Branch 2 "functools.wraps": what it copies, __wrapped__, and the four concrete
things that break without it.

Branch 3 "Arguments": the three levels, the missing-parentheses mistake, and
the pattern for supporting both @deco and @deco(...).

Branch 4 "Stacking": bottom-up wrapping vs top-down calling, and four ordering
rules with the reason for each (registration outermost, caching outside
logging, staticmethod outermost, auth beneath routing).

Branch 5 "functools": lru_cache/cache with its five caveats, partial and its
three advantages over lambda, singledispatch, cached_property,
total_ordering, reduce and why to avoid it.

Branch 6 "contextlib": contextmanager, suppress, ExitStack, closing,
nullcontext -- each with the problem it solves.

Branch 7 "Class-based decorators": when state or extra methods justify one, and
the descriptor problem on methods.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to write a decorator that other people
will use.

Include a decorator template section with four complete, correct templates: no
arguments; with arguments; supporting both forms; class-based with state. Each
fully wraps-correct.

Include a stacking-order reference: for six common pairs (route+auth,
cache+log, staticmethod+anything, retry+timeout, transaction+retry,
validate+cache), the correct order and what goes wrong in the other one.

Include an lru_cache safety checklist: hashable arguments, the 1/1.0/True
collision, positional vs keyword keys, strong references and the method leak,
purity, and how to choose maxsize.

Include a debugging section: how to tell you are looking at a decorated
function in a traceback, how to reach the original via __wrapped__, and why a
profiler shows twelve functions all called 'wrapper'.

End with five broken decorators, each with the symptom, the cause and the fix.
```

**Quiz prompt:**

```
Generate 16 questions.

At least five must be stacking-order puzzles where the wrong order produces a
plausible-looking but broken result. Include the route/auth case specifically.

At least four must be lru_cache traps: an unhashable argument, the 1 versus
True collision, f(1) versus f(x=1), and a cached method leaking instances.

Include: a decorator without wraps and a test that inspects __name__; @retry
used without parentheses; a decorator that runs a print at definition time,
asking how many times it appears for three calls; and a class-based decorator
applied to a method.

For each answer, say whether the effect happens at DEFINITION time or CALL
time, because that distinction explains most of them.
```

**Flashcards prompt:**

```
20 flashcards. Front: a term or fragment. Back: what it does and its gotcha.

Include: @ desugaring, definition-time execution, functools.wraps, __wrapped__,
decorator factory, the three levels, stacking order, lru_cache, cache,
cache_info, maxsize, partial, singledispatch, cached_property, total_ordering,
reduce, contextmanager, suppress, ExitStack, class-based decorator.
```

---

## The specific visuals to insist on

1. **`@decorator` transforming into `f = decorator(f)`**, letter by letter.
2. **The decorator running once at import**, and not running again for three
   calls.
3. **Concentric shells**, with a call token travelling in and back out.
4. **Four downstream failures from missing `wraps`**, shown as real tool output:
   `help()`, a profiler, pytest, FastAPI.
5. **The three nested boxes** of a decorator factory, each labelled with what it
   receives.
6. **The route/auth pair in both orders**, with the framework registry holding
   the raw function in the wrong one, and a request sailing past authentication.
7. **`f(1)`, `f(1.0)` and `f(True)` landing in one cache slot**, and `f(1)` /
   `f(x=1)` landing in two.
8. **The cached-method memory meter climbing and never falling.**

---

## Analogies that work

- **Gift wrapping.** The present is unchanged; each layer of paper is added
  from the inside out. To open it you remove the outermost first. That is the
  wrap order and the call order in one image.
- **A middleware pipeline.** Anyone who has used web middleware already has the
  right intuition: each layer sees the request going in and the response coming
  out, and the order of registration decides who sees it first.
- **A luggage tag with the original's details copied onto it** for
  `functools.wraps` — the wrapper is a different bag, and without copying the
  tag nobody downstream can tell what is inside.

## Analogies to refuse

- **"A decorator modifies a function."** It does not modify anything; it
  returns a *different* function and rebinds the name. That distinction explains
  why `__name__` changes and why `__wrapped__` exists.
- **"Decorators are annotations/attributes"** (as in Java or C#). Those are
  metadata read later by a framework. A Python decorator is executable code that
  runs immediately and can return anything at all.
- **"`@cache` makes it faster."** It makes repeated calls with identical
  arguments faster, and it makes memory usage unbounded. Presenting it as free
  speed is how the method leak gets shipped.

---

## Accuracy guardrails

```
Accuracy requirements:
- A decorator runs ONCE, at definition time, not per call. The wrapper runs per
  call. State this explicitly; most misunderstandings trace back to it.
- functools.wraps copies __name__, __qualname__, __doc__, __module__ and
  __dict__, and sets __wrapped__. It does NOT change the wrapper's actual
  signature -- inspect.signature follows __wrapped__ to report the original.
- Stacking: the decorator NEAREST the def is applied FIRST and is therefore
  INNERMOST. Its wrapper code runs LAST on the way in. Do not state one half
  without the other.
- lru_cache keys include whether arguments were passed positionally or by
  keyword: f(1) and f(x=1) are different entries.
- lru_cache holds strong references to arguments and results. On a method,
  `self` is part of the key, so instances are kept alive indefinitely. Call this
  a memory leak, because it is.
- functools.cache is lru_cache(maxsize=None), added in 3.9.
- singledispatch dispatches on the type of the FIRST argument only.
  singledispatchmethod dispatches on the first argument after self.
- A class-based decorator applied to a method does not bind self automatically;
  it needs __get__.
- contextlib.suppress is one of very few legitimate uses of exception
  suppression, because suppression is its stated single purpose and it is
  scoped to named types.
```

---

## After watching, you should be able to

- [ ] Write `@decorator` without the `@`, and say when it runs.
- [ ] Name four things that break without `functools.wraps`.
- [ ] Draw the three levels of a decorator factory and say what each receives.
- [ ] Predict `@a @b @c` wrapping order and call order.
- [ ] Explain why `@app.route` must be above `@require_auth`.
- [ ] Give three `lru_cache` traps without looking.
- [ ] Explain the cached-method memory leak in terms of the cache key.
- [ ] Say when a class-based decorator is warranted.
