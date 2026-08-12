# NotebookLM Visual Prompts — Module 19: Standard Library, Files, Serialization

---

## Sources to add

| Source | Type |
|---|---|
| `19-stdlib-files-serialization/README.md` | Upload |
| `03-core-types/README.md` (encodings) | Upload |
| https://docs.python.org/3/library/pathlib.html | Website |
| https://docs.python.org/3/library/sqlite3.html | Website |
| https://docs.python.org/3/howto/regex.html | Website |
| https://owasp.org/www-project-top-ten/ | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Data drawn as a labelled
structure that visibly LOSES parts of itself as it passes through a
serialization boundary. Attacks drawn as a malicious string travelling into a
system and being either interpolated (dangerous) or bound as a parameter
(safe). Monospace type for all code, paths and queries. No characters.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who uses os.path, json and string formatting, and has
never had a security incident -- yet.

Thesis: the standard library already contains a correct, tested solution for
almost everything in this module, and the hand-rolled alternative that looks
simpler is usually the one with the vulnerability.

1. SERIALIZATION LOSES THINGS. Build one Python object containing a tuple, a
   set, a Decimal, a datetime, an int-keyed dict and a large integer. Send it
   through json.dumps and back, and animate each piece CHANGING OR VANISHING:
   the tuple returning as a list, the int keys becoming strings, the Decimal
   raising, the datetime raising, and the large integer losing precision in a
   consumer that parses into a float64. Then do the same through CSV, where
   EVERYTHING becomes a string. The point is that a round trip is a lossy
   transformation, not an identity, and you must know what each format drops.

2. SQL INJECTION, ANIMATED. This is the most important 90 seconds in the
   module. Show an f-string query being built character by character with the
   input "'; DROP TABLE users; --", and show the resulting statement being
   parsed by the database as TWO statements. Then show the parameterised
   version: the query is parsed FIRST, with a placeholder, and the value is
   bound to a slot afterwards -- so the value can never become syntax, whatever
   it contains. Make it clear that this is a structural property, not
   escaping: there is nothing to escape because the value never touches the
   parser.

3. COMMAND INJECTION. The same shape. Show shell=True with a string handing
   "; rm -rf ~" to a shell that dutifully splits it into two commands. Then
   show a list of arguments going directly to execve with no shell involved,
   so there is no metacharacter interpretation at any point.

4. PATH TRAVERSAL. Show a web server joining a base directory with user input
   "../../../etc/passwd", and the resulting path escaping the base. Animate
   resolve() collapsing the '..' segments so the escape becomes VISIBLE, then
   is_relative_to rejecting it. Emphasise that the check is impossible before
   resolution, because the string looks harmless until the '..' are collapsed.

5. PICKLE. Show unpickling as EXECUTION rather than parsing: a payload
   containing a __reduce__ that runs a command, and the command running with
   the process's privileges. State plainly that there is no safe mode, no
   validation and no sandbox, and that this is why JSON is the answer for
   anything crossing a trust boundary.

6. NAIVE DATETIMES. Show two timestamps from different servers, both naive,
   being compared -- and the comparison being meaningless because neither
   carries an offset. Then a DST transition: a naive local time that occurs
   TWICE on the clocks-go-back night and NEVER on the clocks-go-forward night.
   Show a scheduled job either running twice or being skipped. Then the same in
   UTC, with a single unambiguous instant converted only for display.

7. TIME.TIME VERSUS PERF_COUNTER. Show a duration measured with wall-clock time
   across an NTP correction, producing a NEGATIVE duration. Then perf_counter,
   monotonic by construction.

8. CATASTROPHIC BACKTRACKING. Show the regex engine trying exponentially many
   partitions of a long run of 'a' against (a+)+b, with the attempt counter
   climbing past a million. Then the linear alternative. Name it as ReDoS and
   note it is reachable from any endpoint that regexes user input.

Close on the theme: every safe version in this video is SHORTER than the unsafe
one. Correctness here is not a trade-off against convenience.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "The Standard Library at Work".

Branch 1 "pathlib": construction with /, the name/stem/suffix family,
resolve vs absolute, atomic writes, glob vs rglob, and the traversal check.

Branch 2 "Files": modes including x, text vs binary, encoding always, newline=""
for csv, and lazy line iteration.

Branch 3 "json": what round-trips and what does not (tuple, set, int keys,
Decimal, datetime, NaN, big ints), custom encoders, ensure_ascii, sort_keys.

Branch 4 "csv": DictReader/DictWriter, dialects, the BOM from Excel, and why
str.split is never acceptable.

Branch 5 "sqlite3": parameters not formatting, `with conn` being a transaction
not a close, row_factory, and foreign keys being off by default.

Branch 6 "pickle": arbitrary code execution, the three acceptable uses, class
fragility, and what to use instead.

Branch 7 "datetime": aware vs naive, UTC for storage, zoneinfo, isoformat,
timedelta vs calendar arithmetic, and perf_counter vs time.

Branch 8 "re": compile once, finditer over findall, named groups, the flags,
raw strings, and catastrophic backtracking.

Branch 9 "subprocess": list not string, check, timeout, and why shell=True is
the vulnerability.

Branch 10 "Security kit": secrets vs random, hmac.compare_digest, hashlib for
digests vs scrypt for passwords, and archive path traversal.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone writing a data-processing service that reads
untrusted files and writes to a database.

Include a serialization comparison table: JSON, CSV, TOML, pickle, SQLite. For
each -- what types survive, what is lost, whether it is safe for untrusted
input, human readability, and the situation it is right for.

Include a security checklist with the vulnerable pattern and the safe one, side
by side, for: SQL injection, command injection, path traversal, unsafe
deserialization, timing attacks on token comparison, ReDoS, zip-slip in
archives, and predictable tokens.

Include a datetime decision guide: when to use naive (almost never), aware, UTC,
zoneinfo, timedelta, relativedelta, perf_counter, monotonic, and time.

Include a "which stdlib module" index: given a task in one line, the module and
the single function that does it, for about thirty tasks.

End with five code fragments, each containing one vulnerability, with the
exploit and the fix.
```

**Quiz prompt:**

```
Generate 16 questions.

At least five must present a code fragment and ask "what is the vulnerability
and what is the exploit input". Cover SQL injection, command injection, path
traversal, pickle, and a timing attack.

At least four on serialization round trips: what comes back from json for a
tuple, a set, an int-keyed dict, a Decimal, and NaN.

Include: csv without newline="", a naive datetime compared across servers, a
duration measured with time.time across a clock adjustment, `with
sqlite3.connect(...)` being assumed to close the connection, and a regex with
nested quantifiers against a long input.

For each answer, give the concrete consequence -- the data lost, the row
deleted, the file read -- not just the rule.
```

**Flashcards prompt:**

```
22 flashcards. Front: a task or fragment. Back: the correct stdlib answer and
the trap.

Include: Path.resolve, is_relative_to, atomic write, open modes, newline="",
json non-round-trippable types, custom JSONEncoder, csv.DictReader, sqlite
parameters, `with conn` semantics, PRAGMA foreign_keys, pickle danger,
tomllib binary mode, datetime.now(UTC), zoneinfo, isoformat, perf_counter,
monotonic, secrets.token_urlsafe, hmac.compare_digest, subprocess list form,
shlex.quote, re raw strings, finditer, ReDoS.
```

---

## The specific visuals to insist on

1. **One object losing pieces at each serialization boundary** — tuple, set,
   int keys, Decimal, datetime, big int.
2. **The f-string query being parsed as two statements**, next to the
   parameterised version where the value is bound after parsing.
3. **`shell=True` splitting a string into two commands**, next to a list going
   straight to `execve`.
4. **`..` segments collapsing under `resolve()`**, making the escape visible.
5. **A pickle payload executing rather than parsing.**
6. **A DST night where one local time occurs twice**, and a scheduled job
   running twice.
7. **A negative duration from `time.time()`** across an NTP correction.
8. **The backtracking counter climbing past a million** on `(a+)+b`.

---

## Analogies that work

- **A form with typed fields versus a sentence.** A parameterised query is a
  form: the database reads the structure first and then fills in fields, so a
  field's contents can never become structure. String interpolation writes the
  sentence and hopes the reader stops where you intended.
- **A shipping manifest** for serialization: the container arrives, but only
  what was on the manifest survives. JSON's manifest has six types on it.
- **A postal address with "go back two streets" in it.** Nobody can tell where
  it points until you actually walk it. That is `resolve()`.

## Analogies to refuse

- **"Escape the input to prevent SQL injection."** Escaping is the fragile
  answer; parameterisation is the structural one. Teaching escaping teaches a
  technique that fails on the next encoding edge case.
- **"pickle is like JSON but for Python objects."** JSON parses data; pickle
  executes instructions. That difference is the entire security story.
- **"Just use UTC everywhere"** without explaining display conversion — it
  produces systems that show users the wrong time, which is a different bug.

---

## Accuracy guardrails

```
Accuracy requirements:
- Parameterised queries are safe because the value never reaches the SQL
  parser. This is structural, not escaping. Do not describe it as "escaping
  quotes".
- Unpickling untrusted data allows ARBITRARY CODE EXECUTION. There is no safe
  mode. State it without hedging.
- `with sqlite3.connect(...) as conn:` commits or rolls back the transaction.
  It does NOT close the connection. This surprises almost everyone.
- SQLite has foreign key enforcement OFF by default; it needs
  PRAGMA foreign_keys = ON per connection.
- json.dumps emits NaN and Infinity by default, which are NOT valid JSON and
  are rejected by many other parsers. allow_nan=False makes it raise instead.
- json converts non-string dict keys to strings; a round trip does not restore
  them.
- tomllib is read-only and requires a file opened in BINARY mode.
- datetime.now() returns a NAIVE datetime. datetime.now(UTC) is aware. Use
  datetime.now(timezone.utc) on versions before UTC was exported from datetime.
- time.time() is wall-clock and can move backwards. perf_counter and monotonic
  cannot.
- random is NOT cryptographically secure. secrets is. Never use random for
  tokens, passwords, or session ids.
- Comparing secrets with == is vulnerable to timing attacks; use
  hmac.compare_digest.
- Plain sha256 is not a password hash. Use scrypt, bcrypt, argon2, or
  pbkdf2_hmac with a high iteration count.
- shell=True passes the string to a shell, which interprets metacharacters. A
  list of arguments does not involve a shell at all.
```

---

## After watching, you should be able to

- [ ] Name four Python types that do not survive a JSON round trip.
- [ ] Explain why parameterised queries are structurally safe, without the word
      "escape".
- [ ] Give the exploit input for an f-string query and for `shell=True`.
- [ ] Say why a traversal check must come after `resolve()`.
- [ ] State what unpickling untrusted data allows.
- [ ] Explain what goes wrong with naive datetimes on a DST night.
- [ ] Say why `time.time()` can report a negative duration.
- [ ] Name the correct tool for tokens, for comparing them, and for hashing
      passwords.
