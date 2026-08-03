# Solutions — Module 10

---

## Exercise 10.1 — MRO predictions

| # | MRO | Output |
|---|---|---|
| q01 | `D B C A object` | `D->B->C->A` |
| q02 | `D2 C B A object` | `D2->C->B->A` |
| q03 | `Bottom Middle Left Right Base object` | `Bottom Middle Left Right Base` |
| q04 good | `GoodOrder UpperMixin Widget object` | `WIDGET` |
| q04 bad | `BadOrder Widget UpperMixin object` | `widget` |
| q05 | `Gamma Alpha Beta Root object` | `['Beta', 'Alpha', 'Gamma']` |
| q06 | `Z(X, Y)` raises; `Z(Y, X)` works | — |
| q07 | `RuntimeError: super(): no arguments` | — |
| q08 | `T->R` | — |

**q01 is the whole module in one line.** `B.greet`'s `super()` reached `C`. `B`'s
only base is `A`; `C` appears nowhere in `B`'s definition. `super()` is a
position on the *instance's* MRO, not an edge in the class graph.

**q02** shows the order of bases changing the MRO and therefore the behaviour of
code in `B` and `C` that neither class can see.

**q04** is the mixin rule, demonstrated rather than asserted. In `BadOrder`,
`Widget.render` is found first and never calls `super()`, so `UpperMixin` is on
the MRO and permanently unreachable. **Mixins first, or they do nothing.**

**q05** is the cooperative-chain failure. `Root` is missing from the result:
`Beta` did not call `super().__init__()`, so `Root.__init__` never ran. And note
what the exercise asks — *could `Beta` have known?* No. `Beta`'s bases are just
`Root`; that `Gamma` would place it before `Root` in an MRO is invisible from
`Beta`'s source. **That invisibility is the argument for keeping multiple
inheritance to stateless mixins.**

**q06.** `class Z(X, Y)` where `Y` already inherits `X` cannot be linearised: bases
must appear in written order (X before Y), but a class must precede its bases
(Y before X). Python raises at **class creation**, which is much better than
resolving arbitrarily at call time.

**q07.** The zero-argument `super()` is compiler magic. When it sees `super()`
inside a method body, the compiler adds an implicit `__class__` cell to the
function's closure. A nested function has its own code object without that cell,
so `super()` raises `RuntimeError: super(): no arguments`. Check
`Q.hello.__code__.co_freevars` — it contains `'__class__'` in the method and not
in the inner function. Inside a nested function, use the explicit
`super(Q, self)`.

**q08.** `super(S, self)` means "start after `S` on `self`'s MRO". Called from
`T`, it skips `S` entirely and lands on `R`. This is the mechanism the
zero-argument form uses with the *current* class filled in automatically — and
writing it explicitly with the wrong class is a way to silently skip a level.

---

## Exercise 10.2 — Five levels, three violations

**Violation 1 — `ReadOnlyDocument` raises where the base did not.** `edit` and
`save` are part of `Document`'s contract. A function holding a `Document` may
call `save` and reasonably expect it to work. Raising narrows the contract: the
subclass accepts fewer situations than the base promised, which is precisely the
Liskov violation. The caller experiences it as an unhandled exception from a
call that is valid according to the type they were given.

**Violation 2 — `EncryptedDocument.word_count` changes the return type**, `int`
to `str`. Every caller doing arithmetic on the result breaks with a
`TypeError` far from the cause. mypy flags this immediately, which is one of
the best arguments for Module 17.

**Violation 3 — `EncryptedDocument.__init__` changes the signature
incompatibly**, requiring `key` and dropping `style`. Any factory that
constructs documents uniformly from `(title, body, style)` now fails on this one
type.

**The refactoring.** `Content` (data) + `Renderer` (a Protocol) + `Store` (a
Protocol) + optional `History`, composed into `DocumentV2`.

**And the interesting question:** why is `ReadOnlyStore.save()` raising
acceptable, when `ReadOnlyDocument.save()` raising was a violation?

Because the **contract is different**. `ReadOnlyStore` is not claiming to be a
substitutable `Store` for every purpose — a caller *chose* it, deliberately,
when constructing the document. The type says "this document has a read-only
store", and the failure is a documented behaviour of that explicit choice.
`ReadOnlyDocument`, by contrast, claimed to be a `Document`, and functions
written against `Document` never opted into anything.

The general principle: **an exception is a violation when it surprises a caller
who only knows the base type. It is a feature when the caller selected the
component that raises.** Composition makes the choice visible at the
construction site; inheritance hides it behind a type name.

**The counting exercise is the real argument.** To add "encrypted AND versioned
AND saveable" to the inherited version you need a new class, and the diamond it
sits in gets worse with each combination — n features means up to 2ⁿ classes. In
the composed version you construct
`DocumentV2(content, EncryptedRenderer(), FileStore(), History())` and write no
new class at all. That combinatorial difference is why "favour composition" is
advice rather than taste.

---

## Exercise 10.3 — Three ways to build a plugin system

The five pressures, and how each approach handles them:

| | ABC | Protocol | Duck typing |
|---|---|---|---|
| **P1** third-party type | **Impossible** without a wrapper | Works, zero code | Works, zero code |
| **P2** missing method | At instantiation | At type-check time | At call time |
| **P3** wrong signature | Not caught at all | At type-check time | At call time |
| **P4** shared code | Free, inherited | Must be a function or a separate mixin | Must be a function |
| **P5** test fake | Must inherit the ABC | Any object with the method | Any object |

**P1 is decisive.** `VendorSlugifier` already has exactly the right method and
has never heard of your ABC. With a Protocol it just works. With an ABC you must
write an adapter class, and then maintain it. Any system that must accept types
you do not control should use a Protocol.

**P3 is the one to remember.** `@runtime_checkable` `isinstance` checks only that
the *attribute names* exist — not their signatures, not their types. A class with
`transform(self, text, extra)` passes `isinstance` and fails at call time. Static
checking catches it; the runtime check does not. Do not rely on
`runtime_checkable` for correctness.

**P4 is the ABC's real advantage.** `apply_twice` is inherited free. With a
Protocol, shared behaviour must live in a module-level function taking the
transformer as a parameter — which is arguably better anyway, since it works for
third-party types too.

**The recommendation:** `Protocol` to describe what you *accept*; ABC for a
family of types you *own* and want to share implementation between. In a plugin
system, where the whole point is that others write the plugins, `Protocol`.

---

## Exercise 10.4 — Mixins

The four that compose cleanly are stateless: they define methods, hold no
attributes, and depend on a small documented interface (`_key()`, `to_dict()`,
`__dict__`). Any host class satisfying that interface gets the behaviour, and
their order among themselves does not matter.

The one that does not is the stateful one: a mixin with its own `__init__`
setting attributes. It now requires cooperative `__init__` from every class in
the MRO, its keyword arguments must not collide with any other class's, and it
breaks silently if the host forgets `super().__init__(**kwargs)` — the exact
failure from exercise 10.1 q05. The host class cannot see the requirement from
its own source.

**The rule this justifies:** a mixin that needs state is a sign you wanted
composition. Hold the object instead of mixing it in — `self._logger` rather
than `class X(LoggerMixin)`. You lose nothing and the dependency becomes visible
at the construction site.
