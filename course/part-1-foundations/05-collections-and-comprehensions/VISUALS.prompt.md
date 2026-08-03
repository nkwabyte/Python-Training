# NotebookLM Visual Prompts — Module 05: Collections and Comprehensions

---

## Sources to add

| Source | Type |
|---|---|
| `05-collections-and-comprehensions/README.md` | Upload |
| `course/appendix/cheatsheets.md` | Upload |
| https://wiki.python.org/moin/TimeComplexity | Website |
| https://docs.python.org/3/library/collections.html | Website |
| https://docs.python.org/3/howto/sorting.html | Website |

---

## 1. Cinematic Video Overview

**Format:** Explanation
**Visual style:** Paper Craft, or Custom with this description:

```
Layered physical objects on a dark background. Arrays drawn as rows of physical
slots. Pointers drawn as literal arrows leaving a slot and landing on an object
elsewhere. Hash tables drawn as a sparse rack of pigeonholes next to a dense
stack of entries. Monospace type for all code and complexities.
```

**Steering prompt (paste this whole block):**

```
Audience: a programmer who uses lists, dicts and sets daily and has never seen
what they are made of, and who therefore cannot predict which one will be fast.

Thesis: every complexity in the table falls out of one physical layout. Show
the layout, and the table becomes something you can derive rather than
memorise.

1. LIST AS AN ARRAY OF POINTERS. Draw a list as a contiguous row of slots, each
   holding an ARROW to an object living elsewhere. Emphasise that the list does
   not contain the objects. Then derive, visually:
     - lst[i] is one jump: O(1)
     - append writes into a spare slot: O(1)
     - append into a FULL array allocates a bigger row and copies every arrow:
       show this happening, then show it NOT happening for the next several
       appends. That is what "amortized" means, and it should be shown, not
       stated.
     - pop(0) shifts every arrow left by one: O(n). Animate the shift.
     - `x in lst` walks the row comparing: O(n).
   Finish this section with the memory consequence: a million ints as a million
   scattered objects plus a million arrows, versus a NumPy array as one solid
   block. Keep this image; Module 29 depends on it.

2. DICT AS TWO ARRAYS. Draw the compact dict: a SPARSE index rack and a DENSE
   entries stack in insertion order. Animate a lookup: hash the key, mask to an
   index, read the position from the rack, jump to the entry, confirm with ==.
   Then animate an insertion appending to the dense stack, which is why
   iteration order is insertion order and why that is free rather than
   maintained. Animate a collision probing to the next slot.

3. WHY A MUTABLE KEY IS FORBIDDEN. Place a key in the pigeonhole its hash
   selects, then mutate the key so its hash changes, then perform a lookup and
   watch it arrive at a different, empty pigeonhole. The entry is present in
   memory and unreachable. Say that forbidding mutable keys makes this state
   unrepresentable.

4. SET ALGEBRA AS A PICTURE. Show a nested loop comparing two collections --
   every element against every element, n*m arrows -- and then the same result
   as a single intersection operation, n+m hash probes. The point is that the
   set version is not merely shorter, it is a different complexity class.

5. COMPREHENSIONS. Show the reading order as an outside-in unwrap: the
   expression at the front is what comes OUT, the for clauses are the loops in
   the same order you would write them nested, the if is the gate. Animate a
   double-for flatten next to its nested-loop equivalent, with the loop order
   highlighted, because that is the part everyone gets backwards once.
   Then contrast a LIST comprehension building the whole result in memory with
   a GENERATOR expression producing one item at a time on demand, and show a
   short-circuiting any() stopping after the third element of a million.

6. STABLE SORTING. Show equal-keyed elements keeping their original relative
   order through a sort. Then show the two-pass multi-key technique: sort by
   the secondary key, then by the primary, and watch the secondary ordering
   survive inside each primary group. This is the clearest possible
   demonstration of why stability is a feature and not a footnote.

7. DEQUE. Show a list's pop(0) shifting everything, next to a deque's O(1)
   removal from either end, and a bounded deque with maxlen dropping the oldest
   item as a new one arrives.

Do not cover: writing your own classes, iterators/generators as a protocol, or
NumPy. Those are Modules 08, 14 and 29.
```

---

## 2. Mind Map

**Prompt:**

```
Build a mind map titled "Choosing and Using Containers".

Branch 1 "list": array of pointers, amortized append, O(n) insert/pop at the
front, O(n) membership, slicing copies, sort is Timsort and stable.

Branch 2 "dict": compact two-array layout, hashing, average O(1), insertion
order guaranteed since 3.7, views and their set operations, get/setdefault/pop,
merge operators, defaultdict and its read-inserts trap.

Branch 3 "set": hash table without values, the six operations (union,
intersection, difference, symmetric difference, subset, isdisjoint), frozenset,
and the "replace nested loops with set algebra" rule.

Branch 4 "tuple": immutable, hashable, records vs sequences, unpacking forms
including starred and nested.

Branch 5 "comprehensions": list/set/dict/generator forms, reading order, filter
vs conditional expression, multi-for ordering, and the four situations where a
loop is better.

Branch 6 "sorting": key functions, called once per element, stability and
multi-pass sorting, operator.attrgetter/itemgetter, reverse, heapq for top-k.

Branch 7 "collections": Counter, defaultdict, deque with maxlen, ChainMap,
namedtuple -- each with its one-line use case.

Branch 8 "the decision": a two-question flowchart -- how do I look things up,
and where do I add and remove.
```

---

## 3. Study Guide, Quiz, and Flashcards

**Study Guide prompt:**

```
Produce a study guide for someone choosing data structures in code review.

Include the complete complexity table for list, tuple, dict, set and deque,
with the AMORTIZED and AVERAGE-CASE qualifiers stated explicitly where they
apply.

Include a "smell to fix" table: for each of about ten code smells (membership
test against a list inside a loop, pop(0) as a queue, a manual counting dict, a
nested loop comparing two collections, sum(lists, []) to flatten, sorting to
get the top three, reading a defaultdict to test membership, building an index
inside a loop, list comprehension used for side effects, materialising a
generator only to iterate it once) give the fix and the complexity change.

Include a comprehension reading guide with five worked examples, from simple to
a double-for with a condition.

End with a container-selection flowchart driven by access pattern.
```

**Quiz prompt:**

```
Generate 16 questions. Half predict-the-output, half "which container and why".

Required: the multi-for ordering in a flattening comprehension, a list
comprehension with a side effect, a generator consumed twice, dict.setdefault
vs defaultdict behaviour on a missing key, stability exploited for multi-key
sorting, sorted() vs .sort() return values, the result of d.keys() & other, a
deque with maxlen overflowing, and Counter arithmetic.

For each answer, state the mechanism and, where relevant, the complexity of both
the naive and the correct version.
```

**Flashcards prompt:**

```
22 flashcards. Front: an operation or term. Back: complexity and mechanism.

Include: list index, list append, list pop(0), list membership, dict lookup,
dict insertion order, set membership, set intersection, deque appendleft,
heapq.nlargest, amortized, average case, Timsort, stable sort, key function,
attrgetter, defaultdict, Counter.most_common, ChainMap, frozenset, generator
expression, dict.fromkeys.
```

---

## The specific visuals to insist on

1. **The list as arrows, not values.** Everything else in the list section
   derives from this one picture.
2. **The resize-and-copy moment**, followed by several free appends, so
   "amortized" is seen rather than asserted.
3. **`pop(0)` shifting every element**, animated.
4. **The compact dict's two arrays**, with an insertion appending to the dense
   one — making insertion ordering obviously free.
5. **The mutated key landing in the wrong pigeonhole.**
6. **n×m arrows versus n+m probes** for nested loops versus set algebra.
7. **The multi-`for` comprehension next to its nested-loop equivalent**, with
   the loop order highlighted in both.
8. **The stability demonstration**: two-pass sort, secondary order surviving.
9. **A bounded deque** dropping its oldest element as a new one arrives.

---

## Analogies that work

- **A card catalogue** for dict: the hash tells you which drawer, so you never
  walk the shelves. Mutating a key is re-titling a book without refiling its
  card.
- **A row of numbered pigeonholes containing claim tickets** for list: the
  pigeonholes are contiguous and cheap to index, but the parcels themselves are
  scattered in the back room.
- **A conveyor belt with a fixed number of slots** for a bounded deque: put one
  on at the front, one falls off the back.

## Analogies to refuse

- **"A list is like an array in C."** It is an array of *pointers*, and the
  difference is the entire memory and performance story.
- **"A set is a list without duplicates."** That implies a linear scan on
  insert. It is a hash table, and the complexity is the point.
- **"Comprehensions are faster loops."** They are marginally faster, but the
  reason to use them is that they describe a result rather than a procedure.

---

## Accuracy guardrails

```
Accuracy requirements:
- list.append is AMORTIZED O(1). Any single append may be O(n). State the
  qualifier every time.
- dict and set operations are AVERAGE-case O(1), worst case O(n). State the
  qualifier.
- dict insertion ordering became a LANGUAGE guarantee in 3.7; in 3.6 it was a
  CPython implementation detail. Name the version.
- The compact-dict two-array layout is a CPython implementation detail, not a
  language requirement. Label it.
- Do not state CPython's list growth factor as a language rule. It is
  implementation-specific and has changed.
- Reading a missing key from a defaultdict INSERTS it. This must be stated
  explicitly, it is a common bug.
- A generator expression can be consumed only ONCE. Do not show one being
  iterated twice as if it worked.
- key= functions are called once per element, not per comparison.
- Sorting is O(n log n); Python's sort is Timsort and is stable. Do not claim
  it is quicksort.
- Do not claim tuples are "faster" than lists in general. They are more compact
  and hashable.
```

---

## After watching, you should be able to

- [ ] Derive `list.pop(0)` being O(n) from the picture, without recalling a
      table.
- [ ] Explain "amortized O(1)" using the resize event.
- [ ] Describe the compact dict's two arrays and say why ordering is free.
- [ ] Explain why a mutable object cannot be a dict key, using buckets.
- [ ] Convert a nested loop over two collections into a set operation, and
      state the complexity change.
- [ ] Read a double-`for` comprehension aloud in the right order.
- [ ] Use sort stability to sort by two keys, and say which pass comes first.
- [ ] Name the right container for a sliding window, for counting, and for
      top-k.
