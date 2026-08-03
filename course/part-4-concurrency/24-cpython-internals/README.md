# Module 24 — CPython Internals

**Time budget:** 4 hours lesson, 5 hours exercises
**Prerequisite:** Modules 02, 08, 23

> **Visual companion:** [`VISUALS.prompt.md`](VISUALS.prompt.md)

---

## Why this module

You do not need this to write good Python. You need it to **stop guessing**.
Every "why is this slow", "why does this use so much memory", and "why does
this behave like that" question in the course so far has an answer one level
down, and this module is where you learn to look.

It also closes the loop on Module 01: you have been told there is bytecode. Now
you read it.

---

## 1. `dis`: reading bytecode

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

```
  2   RESUME               0
  3   LOAD_FAST            0 (a)
      LOAD_FAST            1 (b)
      BINARY_OP            0 (+)
      RETURN_VALUE
```

A **stack machine**: push `a`, push `b`, pop two and push their sum, return the
top. The whole instruction set is about 120 opcodes and you need to recognise
perhaps fifteen.

| Opcode | Means |
|---|---|
| `LOAD_FAST` / `STORE_FAST` | A **local** — an array index. Fast. |
| `LOAD_GLOBAL` | A **global** — a dict lookup, then builtins. Slower. |
| `LOAD_CONST` | A constant baked into the code object |
| `LOAD_ATTR` / `STORE_ATTR` | Attribute access — the Module 08 ladder |
| `LOAD_METHOD` / `CALL` | A method call, avoiding a bound-method allocation |
| `BINARY_OP` | Any binary operator, with an operand saying which |
| `COMPARE_OP` | `<`, `==`, etc. |
| `POP_JUMP_IF_FALSE` | A branch |
| `FOR_ITER` | The iterator protocol, in one instruction |
| `MAKE_FUNCTION` | A `def` or `lambda` executing |
| `BUILD_LIST` / `LIST_APPEND` | Comprehension machinery |

**`dis` settles arguments.** Any time two people disagree about what Python does,
disassemble it:

```python
dis.dis("x = 1 + 2")              # LOAD_CONST 3 -- folded (Module 01)
dis.dis("a += 1")                 # LOAD, ADD, STORE -- three ops (Module 21)
dis.dis("[x for x in y]")         # its own code object (Module 04)
dis.dis("f'{x}'")                 # FORMAT_VALUE, not string concatenation
```

---

## 2. Code objects and frames

```python
def outer(a, b=2, *args, **kwargs):
    x = a + b
    def inner(): return x
    return inner

c = outer.__code__
c.co_varnames        # ('a', 'b', 'args', 'kwargs', 'x', 'inner')
c.co_consts          # constants, INCLUDING inner's code object
c.co_names           # global and attribute names referenced
c.co_freevars        # names captured FROM an enclosing scope
c.co_cellvars        # ('x',) -- names captured BY an inner function
c.co_argcount, c.co_flags, c.co_stacksize
```

`co_cellvars` is Module 04's closure cell, made visible. `x` is in it precisely
because `inner` reads it — that is what turns a local into a cell.

A **frame** is created per call and holds the locals array, the value stack, and
a pointer back to the caller. That chain of pointers is what a traceback walks
(Module 01), and what keeps every local alive while an exception is stored
(Module 02).

```python
import sys
frame = sys._getframe()
frame.f_locals, frame.f_back, frame.f_code.co_name
```

---

## 3. Where the memory goes

```python
import sys
sys.getsizeof(0)            # 28   -- an int object, not 8 bytes
sys.getsizeof(1000000)      # 28
sys.getsizeof(2**100)       # 44
sys.getsizeof("")           # 49
sys.getsizeof("a")          # 50   -- 1 byte per ASCII char
sys.getsizeof("é")          # 74   -- switches to a 2-byte representation
sys.getsizeof([])           # 56
sys.getsizeof({})           # 64
sys.getsizeof(object())     # 16
```

**An `int` is 28 bytes** because it is a full object: a refcount, a type
pointer, a size, and then the digits. That is the number behind Module 08's
`__slots__` measurements and Module 23's NumPy argument — a list of a million
ints is a million 28-byte objects plus a million 8-byte pointers, while a NumPy
`int64` array is eight megabytes, contiguous.

**Strings adapt their storage.** PEP 393: pure-ASCII strings use one byte per
character, and the representation widens to two or four bytes only when needed.
This is why `sys.getsizeof("é")` jumps.

**`sys.getsizeof` does not follow references** (Module 08). A list of a million
ints reports about 8 MB — the pointer array — while the actual cost is nearer
36 MB.

**Small objects are cached.** Integers -5 to 256 and short identifier-like
strings are pre-allocated (Module 02). Implementation detail; never depend on it.

---

## 4. How an attribute lookup really resolves

Module 08 gave the ladder. Here is what it costs.

```python
class C:
    def method(self): pass

obj = C()
obj.method
```

1. `type(obj).__mro__` scanned for a **data descriptor** named `method`.
2. `obj.__dict__` checked.
3. The MRO scanned again for any match; a function found here is wrapped into a
   bound method.
4. `__getattr__`, then `AttributeError`.

Steps 1 and 3 walk the MRO, which is why deep hierarchies cost more per
attribute access, and why `__slots__` (a fixed array index) beats a `__dict__`
lookup slightly.

CPython caches type attribute lookups aggressively — a per-type version tag
invalidated whenever the class is modified. **Mutating a class at runtime
invalidates that cache for every instance**, which is one reason monkeypatching
in a hot path is a bad idea.

---

## 5. The specialising adaptive interpreter (3.11+)

This is the biggest change to CPython's execution model in a decade, and it is
why old performance folklore is unreliable.

The interpreter **watches** which types actually flow through each bytecode and
rewrites the instruction in place into a specialised form:

```
BINARY_OP  (generic: check types, dispatch, maybe call __add__)
    ↓ after a few iterations where both operands are always ints
BINARY_OP_ADD_INT  (a direct integer add, with a guard that falls back)
```

Consequences worth carrying:

- **Monomorphic code is faster than polymorphic code.** A loop where a variable
  is always an `int` specialises; one where it is sometimes an `int` and
  sometimes a `str` cannot, and de-optimises.
- **Benchmarks need a warm-up.** The first few iterations run unspecialised.
- **Micro-benchmark folklore from before 3.11 is often wrong now.** Re-measure
  rather than repeating what you read.

3.12 added a JIT-adjacent "Tier 2" IR, and 3.13 shipped an experimental
copy-and-patch JIT. The direction is clear: **the interpreter is getting
smarter, so measure on your actual version** (Module 23).

---

## 6. Reference counting and the cycle collector, one level down

Module 02 covered the behaviour. The mechanism:

- Every object begins with `ob_refcnt` and `ob_type`. `Py_INCREF`/`Py_DECREF`
  are macros the interpreter calls constantly.
- At zero, the deallocator runs immediately.
- The **generational** cycle collector tracks container objects in three
  generations. Generation 0 is collected often, and survivors are promoted.
  Thresholds default to `(700, 10, 10)`.

```python
import gc
gc.get_threshold()      # (700, 10, 10)
gc.get_count()          # objects since the last collection, per generation
gc.freeze()             # move everything to a permanent generation
```

`gc.freeze()` after startup is a real production technique: it moves
long-lived objects out of the collector's way, which matters enormously for a
pre-fork server, where it also stops the collector from touching (and therefore
copy-on-write un-sharing) every page of the parent's heap. Instagram's
well-known memory reduction came largely from this.

---

## 7. Reading CPython's source

Surprisingly approachable. Worth an hour once.

| File | Contains |
|---|---|
| `Objects/listobject.c` | The list, including the growth factor |
| `Objects/dictobject.c` | The compact dict (Module 05), with a long explanatory comment |
| `Objects/longobject.c` | Arbitrary-precision ints |
| `Python/ceval.c` | The eval loop |
| `Python/bytecodes.c` | The opcode definitions (3.12+) |
| `Include/object.h` | `PyObject`, the refcount macros |
| `Lib/functools.py` | `lru_cache` — pure Python (Module 15) |
| `Lib/dataclasses.py` | `@dataclass` — pure Python, and it builds source strings |

Start with `Lib/`. `dataclasses.py` is a genuinely enjoyable read and demystifies
Module 11 completely — it generates `__init__` by building a string and calling
`exec`.

---

## Common mistakes in this module

| Mistake | Symptom | Fix |
|---|---|---|
| Depending on bytecode details | Breaks on the next release | Bytecode is not stable API |
| Depending on small-int caching | Works, then does not | Use `==` (Module 02) |
| `sys.getsizeof` on a container | Off by 5x | It does not follow references |
| Benchmarking without warm-up | Measures unspecialised code | Warm up first (3.11+) |
| Repeating pre-3.11 folklore | Optimising for an old interpreter | Re-measure |
| Monkeypatching in a hot path | Invalidates the type cache | Do it at import |
| Disabling the GC to "go faster" | Cycles leak; usually no gain | `gc.freeze()` instead |
| Assuming `__del__` runs promptly | It may not (Module 02) | Context managers |

---

## Self-check quiz

1. What kind of machine is CPython's VM, and what does `LOAD_FAST` do?
2. Why is `LOAD_GLOBAL` slower than `LOAD_FAST`?
3. What is `co_cellvars`, and which module's concept does it make visible?
4. Why is an `int` 28 bytes, and what does that imply for a million of them?
5. What does `sys.getsizeof` not count?
6. Describe the specialising adaptive interpreter in two sentences.
7. Why is monomorphic code faster than polymorphic code in 3.11+?
8. What are the three GC generations, and what does `gc.freeze()` do?
9. Why does `gc.freeze()` help a pre-fork server specifically?
10. Name two pure-Python files in `Lib/` worth reading, and what each explains.

---

## Exercises

1. **[`ex01_dis.py`](exercises/ex01_dis.py)** — Disassemble fifteen constructs
   and answer a question about each. Several settle arguments from earlier
   modules.
2. **[`ex02_memory.py`](exercises/ex02_memory.py)** — Measure the true size of
   nine structures, and explain each discrepancy with `getsizeof`.
3. **[`ex03_specialise.py`](exercises/ex03_specialise.py)** — Demonstrate
   specialisation by measuring a monomorphic and a polymorphic loop.
4. **[`ex04_source.md`](exercises/ex04_source.md)** — Read four pieces of
   CPython source and answer specific questions about each.

---

## Going deeper

- [`dis`](https://docs.python.org/3/library/dis.html) — keep it open while reading this module
- [CPython Internals](https://realpython.com/products/cpython-internals-book/) — Anthony Shaw's book, the best single treatment
- [Python Developer's Guide](https://devguide.python.org/) — how the interpreter is actually built
- Brandt Bucher, "Inside CPython's specializing adaptive interpreter" — from the author

---

**Next:** [Module 25 — Automation, Scripting, and the OS](../../part-5-applied/25-automation-and-os/README.md)
