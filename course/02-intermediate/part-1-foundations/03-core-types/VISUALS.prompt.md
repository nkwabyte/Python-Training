# NotebookLM Visual Prompts — Module 03: Core Types and Their Behaviour

Generate after your first read, before the exercises.

---

## Sources to add

| Source | Type |
|---|---|
| `03-core-types/README.md` | Upload |
| `course/appendix/cheatsheets.md` | Upload |
| https://docs.python.org/3/tutorial/floatingpoint.html | Website |
| https://docs.python.org/3/howto/unicode.html | Website |
| https://docs.python.org/3/library/stdtypes.html | Website |
| https://wiki.python.org/moin/TimeComplexity | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Custom, with this description:

```
Clean technical schematic on a dark background. Bit patterns shown as literal
rows of coloured cells. Text shown as a row of character glyphs, bytes shown as
a row of two-digit hex values, and the two ALWAYS drawn in visibly different
shapes so they can never be confused. Monospace type throughout. No characters,
no mascots.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who has used strings and numbers in several languages
and assumes they behave the same way in Python. Do not explain what a number or
a string is.

Thesis: the built-in types each have a physical representation, and every
surprising behaviour in this module falls directly out of that representation.

ACT 1 -- NUMBERS.
1. Show a Python int as an object with a header and a variable-length array of
   digits, and contrast it with a fixed 64-bit machine integer. Make the size
   difference physical: 28 bytes for the number 1. Then show a list of a
   million ints as a million separate boxes plus a million pointers, against a
   NumPy array as one contiguous block. This one image explains most of
   Module 29.
2. Show WHY 0.1 cannot be represented in binary. Do it by analogy with 1/3 in
   decimal: an infinite repeating expansion that must be truncated. Then show
   the actual stored value of 0.1 to twenty-odd digits, and 0.1 + 0.2 landing
   just above 0.3. Emphasise that this is IEEE 754, true in every language, and
   Python is merely honest about it in the REPL.
3. Show banker's rounding: a bar of many .5 values, rounding all halves up
   visibly biasing the sum upward, versus round-half-to-even keeping it
   centred.
4. Show Decimal storing digits and an exponent rather than a binary fraction,
   and the difference between Decimal(0.1) -- which copies the float's error in
   -- and Decimal("0.1"), which does not.

ACT 2 -- STR VERSUS BYTES. This is the most important act; give it the most
time.
5. Draw the Unicode sandwich as a literal diagram: the outside world (files,
   sockets, stdin) is bytes; the inside of your program is str; decode on the
   way in, encode on the way out. Draw a program as a box with a decode gate on
   the left and an encode gate on the right.
6. Show the word "eclair" with an accented e, as characters and as UTF-8 bytes
   side by side, with a bracket showing that ONE character occupies TWO bytes.
   Then show len() giving different numbers for the two. Then show a naive
   slice cutting between those two bytes and the resulting mojibake or
   UnicodeDecodeError. That single image is the whole lesson.
7. Show the same bytes decoded as UTF-8 and as cp1252, producing two different
   readable-but-different strings, to make the point that bytes carry no
   encoding and the decoder must be told.

ACT 3 -- CONTAINERS AND LOOKUP.
8. Show `x in list` as a linear walk touching every element, versus `x in set`
   as a hash computation jumping straight to a bucket. Animate both against
   10,000 elements so the difference in work is visible, not merely asserted.
9. Show why a mutable object cannot be a dict key: place a list key in a bucket
   chosen by its hash, then mutate the list, then show the lookup computing a
   NEW hash and arriving at a DIFFERENT, empty bucket -- the entry present in
   memory but unreachable. Say explicitly that forbidding mutable keys is what
   makes this state unrepresentable.
10. Close on slicing: half-open intervals drawn as tick marks between elements
    rather than on them, so that s[:i] + s[i:] == s is visually obvious, and so
    is why s[2:5] has exactly 3 elements.

Do not cover: comprehensions, collections module, or writing your own classes.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "The Built-in Types".

Branch 1 "Numbers": int (arbitrary precision, object overhead, memory), float
(IEEE 754, why 0.1 is inexact, isclose, NaN, inf, banker's rounding), Decimal
(when, and construct-from-string), Fraction, bool as a subclass of int, and the
division operators including floor-toward-negative-infinity.

Branch 2 "Text and data": str as code points, bytes as integers 0-255, the
encode/decode boundary, the Unicode sandwich, always specify encoding, error
handlers (strict, replace, ignore, surrogateescape) and when each is right.

Branch 3 "str methods": grouped by purpose -- trimming, splitting, joining,
testing, replacing, case (lower vs casefold), removeprefix/removesuffix.

Branch 4 "f-strings": the format mini-language grouped into alignment, width,
precision, type codes, thousands separators, percentages, !r, and the =
debugging form.

Branch 5 "Slicing": half-open convention, negative indices, step, reversal,
slice assignment, and the fact that slices never raise IndexError.

Branch 6 "Containers at a glance": a four-way comparison of list, tuple, dict,
set across mutability, ordering, duplicates, and membership complexity.

Branch 7 "Hashability": what it means, which types have it, why mutability
forbids it, and the 1 == 1.0 == True collision.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone about to write code that handles money, user
input, and text files from unknown sources.

Include a decision table for numeric types: given a requirement (currency,
scientific measurement, counting, exact ratios, IDs, coordinates), which type
and why.

Include an encoding troubleshooting table: given a symptom (UnicodeDecodeError,
mojibake, question marks in output, a length that seems wrong, works on Linux
fails on Windows), give the cause and the fix.

Include a container selection table: given an access pattern, which container,
with the complexity that justifies it.

Include the f-string format mini-language as a single reference table with a
worked example for each code.

End with six code fragments that each contain one of this module's traps, with
the fix and the one-line reason.
```

**Quiz prompt:**

```
Generate 18 predict-the-output questions on numbers, text, and containers.

Required inclusions: 0.1 + 0.2, round(2.5) and round(3.5), Decimal(0.1) vs
Decimal("0.1"), nan == nan, -7 // 2, -7 % 3, len of a multi-byte string versus
its UTF-8 bytes, "example.com".strip("moc."), a dict literal containing both 1
and True, "abc"[10:20], sum of a list of booleans, and 1e16 + 1 == 1e16.

For each, give the mechanism in one sentence and name the false intuition that
produces the wrong answer.
```

**Flashcards prompt:**

```
22 flashcards. Front: an expression or term. Back: the result and the
mechanism.

Include: math.isclose, Decimal from string, banker's rounding, IEEE 754, NaN,
float('inf'), encode, decode, UTF-8 variable width, the Unicode sandwich,
errors='replace' vs 'ignore' vs 'surrogateescape', casefold vs lower,
removesuffix, partition, "".join, half-open slicing, s[::-1], hashable,
unhashable type: 'list', set membership complexity, f"{x=}", f"{x!r}".
```

---

## The specific visuals to insist on

1. **28 bytes for the integer 1**, drawn next to an 8-byte machine int, then
   scaled up to a million-element list versus a NumPy array.
2. **0.1 as an infinite binary expansion being truncated**, then the truncated
   value shown to full precision, then the sum landing above 0.3.
3. **The Unicode sandwich** as a program box with a decode gate and an encode
   gate. This should be the image the viewer remembers from the whole module.
4. **One character, two bytes**, with a slice cutting between them and the
   resulting corruption.
5. **The same byte string decoded two ways** producing two different valid-
   looking results.
6. **Linear scan versus hash jump**, animated over enough elements that the
   difference in work is felt rather than stated.
7. **The mutated dict key**, placed in one bucket and later sought in another.
8. **Slice indices drawn as tick marks between elements**, not on them.

---

## Analogies that work

- **1/3 in decimal** for why 0.1 is inexact in binary. Everyone already accepts
  that 0.333... has to be cut off somewhere; this transfers the intuition
  exactly.
- **A shipping container versus its contents** for bytes versus str. The
  container is identical regardless of what is inside; you need the manifest
  (the encoding) to know how to unpack it.
- **A library card catalogue** for hashing: the hash tells you which drawer to
  open, so you never walk the shelves. Mutating a key is re-titling a book
  without refiling the card.

## Analogies to refuse

- **"A float is just a decimal number."** This is the belief the module exists
  to correct.
- **"A string is an array of bytes."** True in C, false in Python 3, and
  believing it is what produces every slicing-corruption bug.
- **Describing encodings as "formats" or "fonts".** An encoding is a mapping
  between code points and byte sequences, nothing else.

---

## Accuracy guardrails

```
Accuracy requirements:
- Floating point imprecision is IEEE 754, not a Python defect. State that it is
  identical in C, Java and JavaScript.
- Python's round() uses round-half-to-even (banker's rounding), which is the
  IEEE 754 default. Do not describe it as a bug or as "wrong".
- str in Python 3 is a sequence of Unicode CODE POINTS, not bytes and not
  characters-as-grapheme-clusters. An emoji with a skin-tone modifier is
  multiple code points and len() reflects that.
- Do not claim UTF-8 uses 2 bytes per character. It is variable width, 1 to 4.
- dict preserving insertion order became a LANGUAGE guarantee in 3.7 (it was a
  CPython implementation detail in 3.6). Say which.
- Set and dict membership is average-case O(1), worst case O(n). Include the
  qualifier.
- Do not say tuples are "faster than lists" as a general claim. They are more
  memory-compact and can be hashed; that is the real difference.
- bool is a subclass of int. True == 1 and hash(True) == hash(1), which is why
  they collide as dict keys.
- Do not present the CPython string-concatenation-in-a-loop optimisation as
  something to rely on. It is refcount-dependent and implementation-specific.
```

---

## After watching, you should be able to

- [ ] Explain 0.1 + 0.2 to someone else using the 1/3 analogy, in under a minute.
- [ ] State the rule for money in Python and give two acceptable implementations.
- [ ] Draw the Unicode sandwich from memory.
- [ ] Explain why `len()` differs between a string and its UTF-8 encoding.
- [ ] Say what `open(path)` uses for its encoding and why that is a bug.
- [ ] Give the membership complexity of list, set and dict, and say at roughly
      what size the difference becomes visible.
- [ ] Explain why a list cannot be a dict key, in terms of buckets.
- [ ] Predict `{1: "a", True: "b"}` and justify it.
