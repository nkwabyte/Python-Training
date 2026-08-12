# Solutions — Module 11

---

## Exercise 11.1 — Convert five classes

**1. `Coordinate`** → `@dataclass(frozen=True, slots=True)` with validation in
`__post_init__`. Twenty lines become six, and `__eq__`/`__hash__` are now
guaranteed consistent.

**2. `HttpRequest`** → the interesting one. Three separate fixes:

```python
@dataclass
class HttpRequest:
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)   # was a shared {}
    body: bytes = b""
    timeout: int = 30
    created: datetime = field(default_factory=datetime.now)
    content_length: int = field(init=False)                  # derived

    def __post_init__(self) -> None:
        self.method = self.method.upper()
        self.content_length = len(self.body)
```

`default_factory` for the mutable default, `field(init=False)` for the derived
value, and `__post_init__` for normalisation. Note that the original's
`headers=None` sentinel dance disappears entirely.

**3. `Money`** → `@dataclass(frozen=True, order=True)`. But note the behaviour
change: the hand-written `__lt__` *raised* on mismatched currencies, while
`order=True` compares `(cents, currency)` as a tuple and does not. If raising
matters, keep the hand-written `__lt__` and use `order=False`. This is exactly
the "generated ordering may not be your ordering" trap.

**4. `CacheEntry`** → `created` and `hit_count` need `field(compare=False)`.
They are metadata *about* the entry, not part of its identity. Without that,
two logically identical entries created a microsecond apart are unequal, which
breaks every cache-comparison test. Note `hit_count` mutates, so this one stays
unfrozen — and therefore unhashable, which is correct.

**5. `ConnectionPool` should NOT be a dataclass.** Four reasons, and together
they form a general rule:

- `__eq__` on a connection pool is meaningless. Two pools with the same DSN are
  not interchangeable — they hold *different live connections*.
- `__repr__` would print the connection list, including credentials in the DSN.
- `asdict()` would try to recurse into a `threading.Lock` and into live socket
  objects. It fails, or worse, produces something misleading.
- A `Lock` in the constructor is the tell: this type **manages** something. It
  has a lifecycle, identity, and invariants that outlive any snapshot of its
  fields.

> **The rule: dataclasses are for types that ARE data. Types that MANAGE
> something — connections, files, threads, caches with eviction, anything with
> a lifecycle — are entities, and their identity is not their contents.**

---

## Exercise 11.2 — Choosing a record type

The eight scenarios, with the reasoning that generalises:

| Scenario | Choice | Why |
|---|---|---|
| JSON body from an HTTP request | **Pydantic** | Crosses a trust boundary: needs runtime validation and coercion |
| Returning (x, y) from a helper | **NamedTuple** | Unpackable, zero cost, callers can ignore the type |
| Row from a CSV with unknown columns | **dict** | The keys genuinely are dynamic |
| An existing API returns/accepts dicts | **TypedDict** | Static checking without changing the runtime type |
| Internal domain object with methods | **dataclass** | The default |
| A cache key made of several values | **frozen dataclass** or **NamedTuple** | Must be hashable |
| Config loaded from a TOML file | **Pydantic** | A boundary; a typo in the file should fail at startup |
| A node in a parse tree, millions of them | **dataclass(frozen=True, slots=True)** | Memory matters at that count (Module 08) |

The organising idea: **these are not competitors, they are positions in a
pipeline.** The same payload is a `dict` on the wire, a Pydantic model at the
boundary where it is validated, and a frozen dataclass in the domain logic. Each
conversion is a place where you learn something about the data, and after the
Pydantic step everything downstream can trust its types.

---

## Exercise 11.3 — Enums

The four bugs and what enums do about them:

**Bug 1 — typo'd status.** `VALID_TRANSITIONS["pendng"]` raises `KeyError` far
from its cause. With an `Enum`, `Status.PENDNG` is an `AttributeError` at the
point of the typo, and `Status("pendng")` is a `ValueError` at the boundary with
a message listing valid values.

**Bug 2 — permission strings.** `Flag` makes a permission *set* a single value,
so `Permission.READ | Permission.WRITE` is one object, membership is
`Permission.WRITE in perms`, and an invalid permission is unconstructible.
`can_edit` drops from a compound boolean to one expression.

**Bug 3 — the silent `.get(..., 0)`.** A typo'd `"urgnet"` scores 0 and sorts
*last*, which is the opposite of what was intended. Nothing fails; the wrong
thing quietly happens. `IntEnum` makes it a `ValueError` at parse time and makes
`sorted(orders, key=lambda o: o.priority)` work with no lookup table at all.

**`IntEnum` is justified for `Priority` and not for `Status`** because priority
*is* ordinal — comparison is meaningful and the integer is part of the domain.
Status is nominal; `Status.PAID < Status.SHIPPED` would be an accident of
declaration order and a bug waiting to be relied on.

**Bug 4 — the if/elif chain.** With `match` over an enum, mypy reports a missing
case *if there is no wildcard*. Removing the `case _:` is what turns the check
on — the wildcard makes every match exhaustive by definition. That is the trade:
exhaustiveness checking costs you the convenient catch-all, and buys you a
compile-time error every time someone adds a status and forgets a branch.

**Where should string-to-enum conversion happen?** At the boundary, and in
exactly one place per boundary: the HTTP deserializer, the DB row mapper, the
CLI argument parser. Inside the program, values are already enums and no
conversion is needed. Conversion scattered through the codebase means every
call site is a place a typo can slip past.

---

## Exercise 11.4 — Value objects

See [`ex04_value_objects_solution.py`](ex04_value_objects_solution.py). Four
decisions worth defending:

**Email validation should be minimal.** The RFC 5322 grammar allows quoted local
parts, comments and IP-literal domains; the famous "correct" regex is ~6000
characters and still rejects valid addresses. Meanwhile a syntactically perfect
address may not exist and an odd-looking one may work. So check the handful of
certainly-wrong cases and then **prove the address by sending a confirmation
email**. Delivery is the only real validation, and every minute on the regex is
a minute not spent on the confirmation flow.

**The 75-versus-0.75 confusion is prevented structurally.** The constructor takes
exactly one interpretation; the other is a named classmethod. You cannot write
`from_fraction(75)` by accident, because 75 is out of range for a fraction and
raises with a message naming the likely intent.

**`Percentage.__add__` is refused.** "50% + 30%" may mean 80% (shares of one
base) or a 95% compounded increase, and the syntax cannot say which. An operator
whose meaning a reader must guess is worse than no operator, so the solution
provides `plus_points()` and `compounded_with()` instead.

**Half-open date ranges, for the same reason as Python's slices.** Adjacent
ranges tile with no gap and no overlap: `[Jan 1, Feb 1) + [Feb 1, Mar 1)` is
exactly `[Jan 1, Mar 1)`. With inclusive ends you write Jan 31 and remember which
months have 30 days, and every such boundary is a bug waiting for February.
Length is `end - start` with no `+1` anywhere.

And a design decision worth copying: **`Money` sorts across currencies but
refuses to add across them.** Raising from `__lt__` makes `sorted()` explode
halfway through a mixed list, leaving a confusing traceback and a partially
consumed iterator. Sorting USD next to EUR by amount is meaningless but harmless;
*adding* them is meaningful-looking and wrong. Put the loud failure where the
silent bug would be, not where it merely inconveniences a sort.
