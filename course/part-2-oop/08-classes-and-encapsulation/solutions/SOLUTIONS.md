# Solutions — Module 08

---

## Exercise 08.1 — The attribute lookup ladder

| # | Output | Rung | Mechanism |
|---|---|---|---|
| q01 | `['x']` | 3 | One shared list on the class; `append` mutates it |
| q02 | `[] ['x']` | 2 then 3 | Assignment created an instance attribute that shadows the class one |
| q03 | `1 0` | 3 then 2 | `+=` *reads* the class value, then *assigns*, creating an instance attribute |
| q04 | `base None` | 3 | Found on the class; the instance dict is empty |
| q05 | `computed sneaky` | 1 | The property is a **data descriptor** and beats the instance dict |
| q06 | `AttributeError` | 1 | A property with no setter refuses assignment |
| q07 | ran once | 1 then 2 | `cached_property` writes into `__dict__`; later reads stop at rung 2 |
| q08 | `function method` | — | The class holds a plain function; lookup through an instance binds it |
| q09 | `shadowed from Base` | 2 / explicit | A **non**-data descriptor (a plain function) loses to the instance dict |
| q10 | `instance <generated anything_at_all>` | 2 then 4 | `__getattr__` runs only after the normal search fails |
| q11 | `computed` | 1 | The property is found normally, so `__getattr__` never runs |
| q12 | `['_Mangled__hidden'] secret` | — | Mangling happens at compile time, inside the class body only |

### The three that teach the most

**q05 versus q09** is the whole point of the exercise. Both put a name in the
instance `__dict__` that also exists on the class. In q05 the class version wins;
in q09 the instance version wins. The difference is **data descriptor versus
non-data descriptor**:

| Kind | Defines | Lookup priority |
|---|---|---|
| Data descriptor | `__get__` **and** `__set__` (or `__delete__`) | **Before** the instance dict |
| Non-data descriptor | `__get__` only | **After** the instance dict |

`property` defines both, so it wins. A plain function defines only `__get__`, so
an instance attribute shadows it. And `cached_property` defines only `__get__`
*deliberately* — that is precisely how it works: the first call writes the result
into `self.__dict__`, and every subsequent lookup finds it at rung 2 and never
reaches the descriptor again. Module 12 covers descriptors properly.

**q03** is Module 02's `+=` distinction inside a class. `a.shared_int += 1`
expands to `a.shared_int = a.shared_int + 1`: the read finds the class attribute
(rung 3), and the write creates an **instance** attribute. `Base.shared_int` is
untouched. This is why a class-level counter incremented through `self` silently
does nothing useful.

**q11 has a genuinely nasty follow-up.** If the property's own body raises
`AttributeError`, `__getattr__` is called — because `__getattr__` fires on *any*
`AttributeError` from the normal lookup, regardless of where it came from. So a
bug inside a property gets silently swallowed and replaced by a generated value.
This is one of the hardest bugs to find in Python, and the reason to keep
`__getattr__` bodies extremely narrow, or to raise a different exception type
from inside property bodies.

### The `Tracer` TODO

The recursion trap: `__getattribute__` intercepts **every** attribute access,
including `self._log` inside itself. The fix is
`super().__getattribute__("_log")` — or better, `object.__getattribute__`.

**Why `__getattribute__` is almost never right in production:** it runs on every
single access, including internal ones, so the overhead is unavoidable and
global. It is also very easy to break in ways that produce infinite recursion or
break `copy`, `pickle`, and debuggers. `__getattr__` (fallback only) or a
descriptor is nearly always the right tool.

---

## Exercise 08.2 — Delete the getters

See [`ex02_properties_solution.py`](ex02_properties_solution.py). Eight
getter/setter pairs became three validating properties, one read-only property,
three computed properties, and three plain attributes — and
`existing_callers()` runs unchanged against both versions.

That is the demonstration: **in Python, promoting a plain attribute to a
property breaks nothing**, because both use identical syntax. Writing getters
"in case you need validation later" is importing a habit that solves a problem
Python does not have.

**Why `days_until_restock` is a method, not a property.** A property looks like
an attribute, and readers assume attributes are cheap *and stable*. This value
changes without anyone touching the object — read it twice across midnight and
it differs. Parentheses signal "a computation whose result depends on when you
asked".

**And why it takes `today` as a parameter.** With `date.today()` inside, testing
"the day before restock" requires freezing the system clock. With the parameter
it is one line, and the test cannot go flaky at midnight or across a DST
boundary. **Any function whose behaviour depends on the clock should take the
clock as an argument.** The same principle appears in Module 07's
`dead_stock(store, days, now=...)`.

---

## Exercise 08.3 — Six leaks

See [`ex03_encapsulation_solution.py`](ex03_encapsulation_solution.py).

| # | Leak | Fix |
|---|---|---|
| 1 | Getter returned the internal list | Return a tuple of `MappingProxyType` views |
| 2 | Constructor stored the caller's list | Copy on the way **in** |
| 3 | Mutable **class** attribute + leaking getter | Move to `__init__`; return a read-only view |
| 4 | `__repr__` and `to_dict` exposed a token | Redact both; never hand the token out |
| 5 | `[[0.0]*cols]*rows` | Comprehension for the outer dimension |
| 6 | `clear_after_export` gave away the whole history | `export()` without clearing |

Four points worth extracting.

**Leak 2 is the one people miss.** Everyone finds the leaking getter; far fewer
find the constructor storing the caller's list. Copy on the way *in* is as
important as copying on the way out.

**Leak 1 needs two levels.** `tuple(self._items)` protects the sequence but
still hands out mutable dicts — Module 02's shallow-copy trap, one level down.
The fix wraps each dict in a `MappingProxyType`.

**Leak 3 has two independent bugs.** `_handlers` was a class attribute, so all
instances shared one dict; and because `self._handlers[name] = handler`
*mutates* rather than rebinds, it never creates an instance attribute to fix the
problem accidentally. Module 02's mutation-versus-rebinding distinction, in a
class.

**Leak 6 contains a deliberate non-bug.** `since()` returns a new list, and
mutating that list is harmless. Noticing that **not every returned collection
needs defending** is part of the exercise — defensive copying everywhere is its
own cost. The real bug is `clear_after_export`, which hands out the internal
list *and* rebinds `self._events`, leaving the caller owning the only reference
to the entire history. An "append-only" log that a caller can empty is not
append-only, and the docstring is a lie no type checker can catch.

**Leak 4 is the one that becomes a security incident.** `__repr__` is called by
code you did not write — logging, tracebacks, debuggers, and error-reporting
services that ship your stack traces to a third party. Anything sensitive in a
`repr` is effectively public.

---

## Exercise 08.4 — Does `__slots__` matter?

See [`ex04_slots_bench_solution.py`](ex04_slots_bench_solution.py).
Representative results (CPython 3.10, x86-64):

```
single instance
  PointDict   object  48 + __dict__ 104 = 152 bytes
  PointSlots  object  56 + no dict      =  56 bytes     63% saving

at scale (tracemalloc)
     count    dict MB   slots MB   saved MB   saved %
     1,000       0.18       0.08       0.09      53%
   100,000      17.54       8.39       9.15      52%
   500,000      87.90      42.12      45.78      52%

access speed (ns/op)
  read attribute        9.0       9.5      0.95x
  write attribute      12.3       9.6      1.28x
  create instance      89.1      72.2      1.23x
```

**The measurement trap.** `sys.getsizeof(obj)` does not follow references. Report
only the object size and `__slots__` appears to save 8 bytes; the `__dict__` is
where the weight is.

**What it still misses, and this is the more important point.** `x`, `y` and `z`
are *pointers* to heap floats, each about 24 bytes. Neither version stores the
numbers inline. `__slots__` removes the per-instance dict; it does not remove
the boxing. For a million 3-D points the floats outweigh everything else, and
the real answer is a NumPy array (Module 29), not `__slots__`.

**Speed is not a reason on its own.** Reads and writes differ by nanoseconds.
*Creation* differs most, because the dict version allocates and initialises a
hash table per instance. So `__slots__` helps most in exactly the workload where
you also care about memory — creating very many short-lived objects. Memory is
the reason; speed comes along with it.

**What breaks:** new attributes, `__dict__`, `weakref` (unless `'__weakref__'`
is in the slots), `cached_property` (no dict to cache into), and multiple
inheritance from two classes with non-empty slots (`multiple bases have instance
lay-out conflict`).

**Whether that matters:**

- **A `Point` in a physics engine** — `__slots__` is right. Millions of
  instances, fixed shape, no weakrefs, no caching. The canonical case.
- **A `User` in a web app** — `__slots__` is wrong. Hundreds of instances, so
  the saving is invisible; meanwhile ORMs, serializers and mocking libraries all
  set attributes dynamically, and `cached_property` is exactly what you want for
  a computed permission set.
- **A `Node` in a parser** — `__slots__`, with a caveat. Millions of nodes,
  fixed shape: ideal. But parse trees usually want *parent* pointers, and a
  strong parent reference creates a cycle (Module 02). Weak parent references
  require adding `'__weakref__'` to the slots explicitly.

**And the modern answer:** `@dataclass(slots=True)` produces identical memory in
fewer lines, and throws in `__init__`, `__repr__` and `__eq__`. Before 3.10,
`@dataclass` could not generate `__slots__`, so you had to choose. Since 3.10
there is no trade — write the dataclass (Module 11).

---

## Exercise 08.5 — The Account class

See [`ex05_bank_solution.py`](ex05_bank_solution.py). Five decisions worth
defending:

**Read-only `balance` is the entire class.** If a caller can write
`self.balance`, the invariant "the balance changes only through recorded
transactions" is unenforceable, the history is untrustworthy, and the class is a
namespace with ceremony. Making it read-only costs nothing: callers who wanted
to change it were always going to call `deposit` or `withdraw`.

**Rejecting negative amounts is not pedantry.** A negative deposit is a
withdrawal that skips the overdraft check. That exact bug is a real category.

**The transfer failure decision.** Withdraw first, roll back by hand if the
deposit raises. The two operations are not atomic and cannot be made so without
a transaction manager, so the question is which failure is worse. Depositing
first and failing on the withdrawal **creates money** — the worst outcome in a
ledger. Withdrawing first and failing destroys money, which is bad but
recoverable, and the compensating action makes even that unlikely.

The rollback is **recorded in the history**, because a silent compensation is
almost as bad as none. And the honest caveat: this is not correct under
concurrency or across a crash between the two lines. A real system makes the
whole transfer one database transaction (Module 27).

**`cls`, not `Account`, in `open_joint`.** `Savings.open_joint(...)` returns a
`Savings`. Hardcoding the class silently downgrades the type and breaks every
subclass-specific call afterwards.

**`__slots__`: no.** A banking system holds thousands of `Account` objects, not
millions — accounts live in a database and only the working set is materialised.
At 10³–10⁴ instances the saving is under a megabyte, which is not a reason to do
anything, and against it you have ORM attribute management, serialization, and
subclasses inheriting a layout restriction for no benefit. Save `__slots__` for
the Points and the parse Nodes.

**One more, in the exception.** `InsufficientFunds` carries `requested` and
`available` as attributes rather than only a message. An exception with only a
string forces every handler to parse English to react; carrying the numbers lets
a caller decide what to do and lets the presentation layer render it however it
likes, including as JSON. Module 16 makes this a rule.
