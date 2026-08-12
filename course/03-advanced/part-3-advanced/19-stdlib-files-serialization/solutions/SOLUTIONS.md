# Solutions — Module 19

## Exercise 19.3 — Twelve datetime puzzles

| # | Result | Trap |
|---|---|---|
| q01 | `TypeError` | Naive and aware datetimes cannot be compared |
| q02 | Both give `2026-03-30 00:30+01:00` | Arithmetic on an aware datetime is **wall-clock**, not elapsed |
| q03 | `+01:00`; with `fold=1`, `+00:00` | An ambiguous local time; `fold` disambiguates |
| q04 | Accepted, resolved to `+00:00` | A **non-existent** local time, silently accepted |
| q05 | 13:00 / 08:00 / 21:00 | One instant, three renderings |
| q06 | (b) is wrong | `.replace(tzinfo=)` relabels; it does not convert |
| q07 | `-1 day, 16:00:00`, not equal | Aware subtraction compares real instants |
| q08 | Equal, but `tzinfo` differs | The zone **name** is lost; only the offset survives |
| q09 | `2026-03-02`; `ValueError` | No `timedelta(months=1)`, and for good reason |
| q10 | All similar here | Only `time()` can move backwards |
| q11 | Second depends on the machine | `fromtimestamp` without a tz uses local time |
| q12 | — | See below |

**q02 is the subtlest and most consequential.** `+timedelta(hours=24)` and
`+timedelta(days=1)` give the *same* answer, because arithmetic on an aware
datetime operates on **wall-clock time** within the zone. Across the
spring-forward boundary, "24 hours later" on the clock is only 23 *real* hours.
If you meant elapsed time, convert to UTC, add, and convert back. If you meant
"same time tomorrow", the wall-clock behaviour is correct. **The two are
different operations and Python cannot tell which you meant** — you have to.

**q03 and q04 are the DST pair.** On the clocks-go-back night, 01:30 happens
twice, and `fold=0`/`fold=1` selects which. On the clocks-go-forward night,
01:30 never happens at all — and Python **accepts it silently**, resolving to a
neighbouring offset. A job scheduled at 01:30 local will therefore run twice one
night a year and be skipped another. This is a real class of production
incident, and the reason schedulers store UTC.

**q06(b) is the bug.** `datetime.now().replace(tzinfo=TOKYO)` takes the local
wall-clock time and *relabels* it as Tokyo time, producing a moment that is
wrong by the offset between your machine and Tokyo. `.replace(tzinfo=)` never
converts; `.astimezone()` does. This one-character difference has shipped more
timezone bugs than any other.

**q08 — what is lost.** `isoformat()` preserves the **offset** (`+09:00`) but
not the **zone** (`Asia/Tokyo`). They compare equal because they are the same
instant, but the round-tripped value no longer knows its DST rules, so future
arithmetic on it will be wrong. If the zone matters, store the IANA name
alongside.

**q12 — the answer is: store local time plus the zone name, for future
appointments.** Governments change DST rules with a few months' notice
(Brazil abolished DST in 2019; the EU has repeatedly debated it). If you stored
"2026-10-25T00:30Z" and the rules change, the meeting moves on the user's
calendar. If you stored "2026-10-25 01:30, Europe/London", it stays at 01:30
local, which is what the user meant. Google Calendar stores the local time and
the zone for exactly this reason.

**Rule of thumb: past events and precise instants in UTC; future local
appointments as local time plus zone.**

---

## Exercise 19.4 — Five vulnerabilities

### 1. SQL injection

```python
name = "' OR '1'='1"                            # returns every row
name = "'; DROP TABLE users; --"                # destroys the table
name = "' UNION SELECT id, api_key, '' FROM secrets --"   # reads another table
```

The fix is `conn.execute("... WHERE name = ?", (name,))`. After it, the first
input searches for a user literally named `' OR '1'='1` and returns zero rows.

**Why this is structural, not escaping.** The database parses the statement
first, with a placeholder, and binds the value afterwards. The value never
reaches the parser, so it cannot become syntax no matter what it contains.
Escaping tries to neutralise dangerous characters and fails on the next encoding
edge case; parameterisation removes the category.

Note the third exploit: `DROP TABLE` is the famous one, but a `UNION` attack is
the one that actually happens, because it exfiltrates data silently and leaves
no damage to notice.

### 2. Command injection

```python
pattern = "x'; touch /tmp/pwned; echo '"
```

With `shell=True`, the string is handed to a shell that splits on `;` and runs
both commands. With a list, `subprocess` calls `execve` directly — **there is no
shell**, so `;` is just a character in an argument. Your exploit string becomes
a pattern that matches nothing.

### 3. Path traversal

```python
filename = "../../etc/passwd"
filename = "/etc/passwd"          # and this one is worse -- see below
```

`Path("/base") / "/etc/passwd"` returns `Path("/etc/passwd")`. An absolute
right-hand operand **discards the left entirely**. That is documented and
almost nobody knows it, and it means a `startswith` check on the joined string
does not save you.

The fix must use `resolve()` before checking, because `..` segments and symlinks
are only collapsed then:

```python
target = (base / filename).resolve()
if not target.is_relative_to(base.resolve()):
    raise ValueError("path escapes the base directory")
```

The symlink case is why a string check is insufficient: `safe/link.txt` can
point anywhere, and only resolution reveals it.

### 4. Unsafe deserialization

```python
class Exploit:
    def __reduce__(self):
        return (os.system, ("echo pwned",))
pickle.dumps(Exploit())          # unpickling this RUNS the command
```

**Can you validate the bytes first?** No, and it is worth being able to say why:
the pickle format is a **stack-based virtual machine** with opcodes including
`GLOBAL` (import any name) and `REDUCE` (call it). Deciding whether a program
does something dangerous is the halting problem in general, and even a
restricted `Unpickler` with an allowlist of classes only limits *which* classes
can be constructed — a permitted class with a dangerous `__setstate__` is still
a hole. There is no validation rule that works, which is why the answer is "do
not unpickle untrusted data" rather than "unpickle it carefully".

### 5. Timing attack

`==` on strings **short-circuits at the first differing byte**, so a candidate
matching the first 500 characters takes measurably longer than one differing at
character 0. Over enough trials, an attacker recovers the token one character at
a time — turning a 2²⁵⁶ brute force into a few thousand requests.

`hmac.compare_digest` compares in time proportional to the length, independent
of content.

**Does it hide the length?** **No.** It returns `False` immediately for
different-length inputs, and its runtime depends on the length. That is
acceptable because token length is not usually secret, but it is worth knowing
that "constant time" here means "independent of the *content*", not
"independent of everything".

---

## Exercise 19.2 — What each format loses

| | JSON | CSV | TOML | pickle | SQLite |
|---|---|---|---|---|---|
| `tuple` | → list | → string | → array | preserved | → per-column |
| `set` | **raises** | → string | **unsupported** | preserved | — |
| `Decimal` | **raises** | → string | → float (**lossy**) | preserved | → TEXT or REAL |
| `datetime` | **raises** | → string | **native** | preserved | → TEXT |
| int dict keys | → **strings** | — | → strings | preserved | — |
| `bytes` | **raises** | — | unsupported | preserved | BLOB |
| nested structures | yes | **no** | yes | yes | via joins |
| big ints (>2⁵³) | emitted, but many parsers lose precision | string | yes | yes | INTEGER, 64-bit |
| safe for untrusted input | **yes** | yes | yes | **NO** | yes |

The two entries that cause real incidents: **JSON turning integer dict keys into
strings** (so a round trip silently changes your key type, and lookups start
missing), and **TOML parsing decimals as floats** (so a config file holding a
price loses exactness — Module 03). Store money as a string in every one of
these formats.

---

## Exercise 19.1 — pathlib and traversal

The six attacks the check must reject: `../secret.txt`, `../../etc/passwd`,
`/etc/passwd`, `a/../../secret.txt`, `./../../secret.txt`, and a symlink inside
the base pointing outside it.

The last two are the interesting ones. `a/../../secret.txt` defeats a naive
check for a leading `..`, and the symlink defeats every string-based check
there is. Both are why the check must operate on the **resolved** path and use
`is_relative_to` rather than `startswith` — string prefix matching also has the
`"/base"` versus `"/base-evil"` bug, where the second passes a `startswith`
check on the first.
