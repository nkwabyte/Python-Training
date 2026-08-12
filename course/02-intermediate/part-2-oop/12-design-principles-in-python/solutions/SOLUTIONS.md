# Solutions — Module 12

---

## Exercise 12.1 — Six patterns, de-patternised

| Pattern | Classes before | After | Replaced by |
|---|---|---|---|
| Strategy | 5 | 0 | A function argument |
| Singleton | 1 + locking | 0 | A module |
| Factory | 4 | 0 (a dict) | A dict of constructors |
| Observer | 4 | 0 (a list) | A list of callables |
| Template Method | 2 | 0 | A function taking hook functions |
| Builder | 2 | 1 | Keyword arguments + `__post_init__` |

```python
# 1 Strategy -> sorted() already takes a key. There is no Sorter.
sorted(data, key=abs)
sorted(data, reverse=True)

# 2 Singleton -> config.py
_settings = load_settings()
def get_settings() -> Settings: return _settings

# 3 Factory -> a dict
ANIMALS = {"dog": Dog, "cat": Cat}
ANIMALS["dog"]()

# 4 Observer -> a list of callables
observers: list[Callable[[str], None]] = [send_email, write_log]
for observe in observers: observe(event)

# 5 Template Method -> a function taking functions
def process(raw, *, parse, transform=lambda d: d, render):
    return render(transform(parse(raw)))

# 6 Builder -> keyword arguments, and required means required
@dataclass(frozen=True)
class Pizza:
    size: str                       # no default -> required, enforced by Python
    toppings: tuple[str, ...] = ()
    extra_cheese: bool = False
```

**Q1 — where the Java version genuinely wins: Strategy.** If a strategy needs
*state* across calls, or several coordinated methods (`encode` and `decode`,
`begin`/`step`/`finish`), then a class is the right answer and the pattern earns
its keep. A single stateless operation is a function; a stateful multi-method
collaborator is an object. The tell is whether the strategy has more than one
method, or any attributes.

**Q2 — Builder exists to enforce required fields before construction.** A
dataclass field with no default is already required, and Python raises
`TypeError` at the call site. What Builder can still do that a dataclass cannot
is **incremental construction across a scope**: accumulating options in a loop,
across several functions, or based on branching logic, before producing an
immutable result. For that, keep a mutable builder or accumulate a dict of
kwargs — but note that `dataclasses.replace` on a frozen instance covers most of
it.

---

## Exercise 12.2 — Descriptors

The critical detail in `__get__`:

```python
def __get__(self, obj, objtype=None):
    if obj is None:
        return self          # accessed on the CLASS, not an instance
    return getattr(obj, self._name)
```

Without the `obj is None` branch, `Product.price` (no instance) raises, and with
it goes `help()`, Sphinx, `inspect`, and every tool that walks class attributes.
Every descriptor needs it.

**`Typed` — when is runtime enforcement worth it?** At a **boundary**: data from
HTTP, a file, a queue, a database column with a loose type. Inside your own
program, after the boundary has validated, a static checker is enough and costs
nothing at runtime. Enforcing types on every internal assignment is paying a
runtime cost forever to catch a bug mypy catches once, at zero cost. Module 17
develops this.

**`Lazy` is the whole point of the exercise.** The trick is one line — *not*
defining `__set__`. That makes it a **non-data** descriptor, which the instance
`__dict__` beats. So writing the computed value into `obj.__dict__[name]` on
first access means every later access is caught at rung 2 of the lookup ladder
and the descriptor never runs again.

**And what breaks if you add a `__set__` that raises?** It becomes a *data*
descriptor, which now takes priority over the instance dict — so the cached
value in `__dict__` is never reached, and the computation runs on **every**
access. The caching silently stops working with no error at all. That is exactly
why `functools.cached_property` has no `__set__`, and it is the cleanest
demonstration in the language of why the data/non-data distinction matters.

**When a descriptor beats a property:** the same logic on three or more
attributes, or across several classes. Below that, `@property` is clearer and a
reader does not have to learn a new mechanism.

---

## Exercise 12.3 — Plugin registries, four ways

| Approach | Registration | Discovery | Best for |
|---|---|---|---|
| Manual dict | Explicit at one site | Trivial | Small, closed sets |
| Decorator | At the definition | Import-time | In-repo plugins |
| `__init_subclass__` | Automatic on subclassing | Import-time | Class-based plugins you own |
| Entry points | In `pyproject.toml` | Across installed packages | Third-party plugins |

The trap shared by the middle two: **a plugin registers only if its module is
imported.** A decorator or `__init_subclass__` in a file nobody imports does
nothing at all, silently. That is why real plugin systems either import a
package eagerly at startup, or use entry points (`importlib.metadata`), which
work across distributions without importing anything until needed.

The manual dict is underrated. If the set of plugins is known and small, an
explicit dict is greppable, has no import-order surprises, and needs no
mechanism at all.

---

## Exercise 12.4 — Dependency inversion

**The five dependencies, and which is hardest to spot:**

1. The database connection — obvious.
2. The payment gateway — obvious.
3. The SMTP connection — obvious.
4. `uuid.uuid4()` — usually missed.
5. `datetime.now()` and `random.random()` — almost always missed.

**4 and 5 are the ones that make tests flaky rather than merely slow.** A test
that asserts on an order ID or a timestamp cannot be written at all while those
are generated internally; you end up asserting only on the shape of the output,
which is a much weaker test. Injecting a counting ID generator and a fixed clock
turns "the result has some id" into "the result is exactly this".

**Prefer fakes over mocks.** A fake repository storing orders in a dict lets you
assert on the *outcome* — "the order is in the repository with this total". A
mock only lets you assert that `save` was called, which passes even when `save`
stores the wrong thing. Module 18 argues this at length.

**The mail-failure question has no single right answer, and that is the point.**
The charge succeeded; the customer's money has moved. Rolling it back because a
confirmation email failed is worse than not sending the email. The correct
production answer is neither "roll back" nor "swallow": it is to **record the
order as placed and queue the notification for retry**, which is Module 33's
subject. Note that this is the same shape as Module 08's transfer problem — two
operations that cannot be made atomic, where the question is which failure is
least bad.

**What a DI framework would add:** wiring by type annotation, scope management
(request-scoped, singleton), and lazy construction. What it costs: a
configuration language, a startup graph nobody can read in a traceback, and
errors that occur at wiring time rather than at the call site. For a service with
five dependencies, constructor parameters with defaults win on every axis. The
calculus changes at a few hundred wired components — which most Python
applications never reach.

**Is a five-parameter constructor worse than the original one-parameter one?**
For the *caller*, marginally — though defaults mean production code still writes
`OrderService()`. For the *reader*, much better: the dependencies were always
there, and now they are visible in the signature instead of buried in the body.
For the *tester*, transformatively better. **A constructor's parameter list
should tell the truth about what the object needs.** The original one was
hiding four things.
