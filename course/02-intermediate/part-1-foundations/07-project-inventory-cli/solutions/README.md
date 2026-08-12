# Reference Solution — Inventory CLI

**Do not read this until you have a working Stage 5.** Seeing a finished design
before you have struggled with the decisions removes the entire benefit. The
value is in having made the choices badly first.

```bash
cd inventory-cli
pip install -e .
pytest -q                    # 85 tests
inv --help
```

Or without installing:

```bash
PYTHONPATH=src python -m inventory --help
```

---

## Read it in this order

1. **`errors.py`** — 60 lines, and it determines the shape of everything else.
2. **`models.py`** — where the immutability decision lives.
3. **`operations.py`** — the logic layer, and the module that proves the layers
   are separate.
4. **`cli.py`** — everything the other modules were forbidden to do.
5. **`store.py`** — the atomic write.
6. **`tests/`** — particularly `test_store.py::test_save_is_atomic_under_failure`
   and `test_serialization.py::test_csv_round_trip`.

---

## The eight decisions worth arguing about

### 1. Items are immutable

Operations return a *new* `Item` rather than mutating. Four consequences:

- The change history falls out for free — you have the before and the after,
  both intact, with no bookkeeping to forget.
- Every operation is testable with one equality assertion and no setup.
- Module 02's aliasing bugs become *unrepresentable*. An item handed to two
  parts of the program cannot change underneath either.
- Items are hashable and usable in sets and as dict keys.

The cost is an allocation per change. For 10⁴–10⁶ items that is irrelevant; at
10⁸ it would not be. Know which regime you are in.

The `Store` is the one mutable thing in the package. Confining mutation to a
single named place is most of what makes a program reasonable to debug.

### 2. Validation lives in `__post_init__`

An invalid `Item` cannot exist. That is the highest-value habit in domain
modelling: **if the type cannot hold a bad value, no downstream code needs to
check for one.** Compare with validating in the CLI, which leaves every other
caller — the importer, a future HTTP handler, a test fixture — free to construct
garbage.

### 3. Exit codes live on the exception

`InventoryError.exit_code` is a class attribute, not a lookup table in `cli.py`.
Adding a new error type *cannot* forget to add its code. `cli.py` has exactly
one `except InventoryError` clause and maps everything through it.

### 4. `main(argv, env)` takes both as parameters

This single choice is why `test_cli.py` uses no subprocesses and no
monkeypatching. `sys.argv` and `os.environ` are process-global mutable state
shared by every test in the run; a test that mutates one and fails before
cleanup poisons everything after it.

Same principle applies to the clock: `dead_stock(store, days, now=...)` takes
its `now`. **Any function whose behaviour depends on the clock should take the
clock as an argument.** That test cannot become flaky at midnight or across a
DST boundary.

### 5. Reports return data, not text

`reporting.py` returns `LowStockRow` and `ValueRow` objects. `cli.py` renders
them. That is why `--json` is a two-line addition rather than a rewrite: the
same function feeds both the human table and the machine output.

### 6. `plan_import` is pure

It parses and diffs without mutating anything, producing an `ImportPlan`. So
`--dry-run` and the real import run *identical code* — the dry run cannot
diverge from what would actually happen, which is the only property that makes
a dry run worth having.

It also collects **all** row errors rather than stopping at the first. Someone
importing a 5,000-row CSV wants the full list, not one error per attempt.

### 7. Tags are joined with `;` in CSV, not `,`

A one-character format decision that means a tag list never needs CSV quoting
inside a field, removing a whole class of round-trip bug. Small format decisions
like this are where serialization bugs are prevented rather than fixed.

### 8. The temp file is written in the same directory

```python
tmp = path.with_name(path.name + ".tmp")
tmp.write_text(...)
tmp.replace(path)          # atomic
```

`os.replace` is atomic only **within a filesystem**. Writing the temp file to
`/tmp` and renaming onto a different mount is a copy, not a rename, and is not
atomic. This is a genuinely common bug in code that otherwise looks correct.

And note the limit: this protects against a **crash**. It does not protect
against two concurrent writers — the second save still overwrites the first
entirely. Concurrency needs locking, which is a different problem.

---

## The three tests worth stealing

**`test_save_is_atomic_under_failure`** — saves successfully, makes
serialization raise mid-save, and asserts the original file is byte-identical
afterwards. This is requirement N5 tested for real rather than asserted in a
comment. It fails immediately if anyone "simplifies" the save to
`path.write_text(...)`.

**`test_csv_round_trip`** — export, import into a fresh store, compare. One test
that catches quoting bugs, type-coercion bugs, and dropped fields at once.
Paired with `test_names_containing_commas_and_quotes_survive`, which is the test
that every hand-rolled CSV writer fails in week two of production.

**`test_errors_never_reach_stdout`** — asserts `capsys.readouterr().out == ""`
on a failing command. Without it, someone adds a helpful `print()` and silently
breaks every pipeline the tool is used in.

---

## What is deliberately not here

Things a production version would need, left out so the reference stays
readable. Each is a good extension:

- **Locking.** Two `inv` processes writing concurrently lose one of the writes.
  `fcntl.flock` is the answer on a local filesystem; on NFS it is a harder
  problem than it looks.
- **Migrations.** The `schema_version` field is written and checked, but there
  is no upgrade path from v1 to v2 because there is no v2 yet. The right time
  to add the machinery is when you write the second version.
- **`(sku, location)` as the key.** The current model is one line per SKU, so a
  partial move records the split in history and leaves the remainder in place.
  A warehouse that genuinely holds one SKU in several places needs a different
  key — and noticing that early is exactly what the "merge decision" in the
  brief is for.
- **Structured logging.** `err()` writes plain text. Module 16 covers doing this
  properly.
- **Pagination on `list`.** Fine at 10⁴ items, not at 10⁷.

---

## Verifying the layer rule

```bash
grep -rn "print(\|sys.exit\|argparse\|os.environ" src/inventory/ \
    --include="*.py" | grep -v cli.py
```

Returns nothing. If it ever returns something, the logic layer has grown an
opinion about who is calling it, and the next caller — a web handler, a test, a
scheduled job — will have to work around it.

Worth adding to CI as a real check. Architectural rules that are only in a
document are architectural rules that decay.
