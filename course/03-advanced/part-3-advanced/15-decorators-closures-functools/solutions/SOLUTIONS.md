# Solutions — Module 15

---

## Exercise 15.2 — Stacking order

| # | Output | Mechanism |
|---|---|---|
| q01 | `wrap:c, wrap:b, wrap:a` then `enter:a, enter:b, enter:c, body, exit:c, exit:b, exit:a` | Bottom-up wrapping, top-down calling |
| q02 | `['wrap:x']` — once, for three calls | The decorator runs at **definition**; only the wrapper runs per call |
| q03 | `wrapper None` | No `wraps`: name and docstring lost |
| q04 | `(*a, **kw)` vs `(a: int, b: str = 'x') -> None` | `wraps` sets `__wrapped__`; `inspect.signature` follows it |
| q05 | `TypeError: decorator() missing 1 required positional argument: 'fn'` | `@retry` without `()` passed the function as `attempts` |
| q06 | cache-outside: 1 real, 1 logged. log-outside: 1 real, 3 logged | Whichever is outermost sees every call |
| q07 | `/right` blocked; **`/wrong` SERVED** | The registry holds the raw function |
| q08 | `staticmethod` vs `function` | Decorators below `@staticmethod` see the descriptor object |
| q09 | `1 2` — both present | `wraps` copies `__dict__`, carrying the inner attribute out |
| q10 | **3** entries | `_make_key`'s fast path — see 15.3 |

### q07 is the one to remember

Both definitions compile. Both run. A smoke test calling `wrong("ada")` passes.
And `/wrong` serves an unauthenticated request, because `@route` registered the
function it received — the **raw** one — while `require_auth` wrapped a name
that nothing subsequently calls.

**Where would you catch this?** Not in a unit test of the handler, which calls
the decorated name. Only in a test that goes **through the router** with no
credentials. That is the argument for having at least one test per protected
route that asserts a 401, however tedious it looks.

### q06 — which order do you want?

- **Metrics/timing: cache outermost.** You want to measure what the user
  experienced, and a cache hit genuinely was fast.
- **Audit logging: logging outermost.** "Who asked for this record" must record
  every request, including ones served from cache. A cached read is still a
  read, and that distinction matters in a compliance audit.

The general rule: put the decorator whose job is *observation* on the outside of
the one whose job is *avoidance*.

---

## Exercise 15.3 — Cache traps

### Trap 1: the answer is worse than "they collide"

```
f(1)       -> 1 is int
f(1.0)     -> 1.0 is float
f(True)    -> 1.0 is float          <- WRONG ANSWER FROM THE CACHE
f(n=1)     -> 1 is int
entries: 3
```

`f(True)` returns *"1.0 is float"*. The function was never called with `True`;
the cache returned the entry stored for `1.0`, because `True == 1.0` and their
hashes are equal.

The three entries come from `functools._make_key`'s **fast path**: a single
positional argument whose type is `int` or `str` is used directly as the key.
So `f(1)` keys on the bare `1`, while `f(1.0)` and `f(True)` fall through to
the general path and key on `(1.0,)` and `(True,)` — which are equal to each
other and therefore share one slot. `f(n=1)` is a keyword call and gets a third.

**The rule to take away:** if a function's behaviour depends on the *type* of a
numeric argument, do not cache it by that argument. And more generally, a cache
is only as correct as `__eq__` and `__hash__` on its keys (Module 09).

### Trap 2: the method leak

```
created 20, dropped all references, still alive: 20
```

`@cache` on a method puts `self` in the cache key, so the cache holds a strong
reference to every instance it has ever seen. They can never be collected. In a
service where the cached method is on a request or session object, memory grows
without bound for the process lifetime.

Three fixes, and what each costs:

| Fix | Cost |
|---|---|
| `@cached_property` | Per-instance only, no arguments, dies with the instance |
| `@lru_cache(maxsize=N)` | Bounded, but still pins up to N instances |
| Cache on a module-level function keyed by an **id**, not the object | Extra plumbing; correct |

**The standard library's answer for exactly this case is
`functools.cached_property`** — it stores the result in the instance's own
`__dict__` (Module 08), so it lives and dies with the instance and holds nothing.

### Trap 3: unhashable arguments

Raising is the right behaviour: it fails immediately, at the uncacheable call,
rather than silently skipping the cache (hiding a performance cliff) or
stringifying the argument (producing wrong hits for distinct objects with equal
reprs).

Two workarounds:

- **(a) Convert at the boundary** — `process(tuple(items))`. The caller loses
  the ability to pass a mutable sequence, which is a fair trade and makes the
  cacheability visible in the signature.
- **(b) A custom key function** — cheap, and dangerous if the key is not
  *injective*. `key=lambda items: len(items)` "works" and returns the wrong
  cached answer for two different lists of the same length. If you write a key
  function, you are asserting that equal keys mean interchangeable inputs, and
  nothing checks that assertion.

### Trap 4: caching side effects

Three calls, **one** log entry. Obvious with a `print`. The three that are not
obvious in review:

1. **A function that increments a metric or counter.** The dashboard silently
   under-reports, and nobody notices because the number is plausible.
2. **A function that returns a mutable object.** Every caller gets the *same*
   list, and one caller mutating it changes what every future caller sees —
   Module 02's aliasing bug, delivered by the cache.
3. **A function that reads a file or queries a database.** It is "pure" in the
   sense of having no writes, and it silently serves stale data forever. This is
   the most common one in real code.

### Trap 5: `maxsize`

For a service with 10 million users and 50,000 daily actives, `maxsize` should
be sized to the **working set**, not the key space: somewhere around 50,000 to
100,000. At `maxsize=128` the hit rate collapses to near zero because the
working set thrashes; at `maxsize=None` you eventually cache all 10 million.

`maxsize=None` is correct when the key space is genuinely small and bounded —
`@cache` on a function of an enum, a config key, or a recursive function over a
fixed range. It is never correct for anything keyed by user input.

---

## Exercise 15.1 — Eight decorators

The one that teaches the most is **`@validate`**, and the lesson is in the
failure of the naive approach. Mapping arguments by position:

```python
for value, (name, param) in zip(args, sig.parameters.items()):   # BROKEN
```

breaks for keyword arguments, for defaults that were not passed, for `*args`,
and for positional-only parameters. The correct tool is
`inspect.signature(fn).bind(*args, **kwargs)`, which returns a `BoundArguments`
mapping every parameter name to its value, applying defaults via
`.apply_defaults()`. Write the naive version first and watch `add(1, b=2)` fail;
that is what makes the right answer memorable.

**`@synchronized` uses a lock per decorated function, not one global lock**,
because a single global lock serialises unrelated functions against each other —
turning two independent operations into a queue for no reason. Module 21 covers
why that is a scalability disaster and not just inelegant.

**`@rate_limited` should default to raising, not sleeping.** Sleeping hides
backpressure: the caller has no idea it is being throttled, latency silently
climbs, and in an async context a blocking sleep stalls the whole event loop
(Module 22). Raising a `RateLimitExceeded` that the caller can handle — by
backing off, shedding load, or returning a 429 — keeps the decision where the
information is. Offer `sleep=True` as an opt-in for scripts.

**`@memo_ttl` must store the insertion time alongside the value**, and the
interesting design question is *when* to evict. Checking expiry on read is
simple and lets dead entries accumulate; a background sweep costs a thread.
For most uses, check on read plus a bounded `maxsize` is right — which is
roughly what every production cache library does.
